
import json

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from threading import Thread

from SRC.Style import (
    window, create_captions_window, styleApp, styleBox, styleBtn,
    create_image, create_progress, create_line, create_text,
    create_video_table, get_selected_streams,
    create_playlist_table, get_selected_items,
    create_separator, visualize_table
)
from SRC.Service import Thumbnail, Video, VideosPlaylist as Playlist, Script, encode

class Tab(QWidget):
    def __init__(self, path:callable, index:int, open_in_new_tab:callable, delete_tab:callable):
        super().__init__()

        self.path = path
        self.index = index
        self.delete = delete_tab
        self.send_url = open_in_new_tab

        self.grid = QGridLayout(self)
        self.grid.setSpacing(10)
        self.grid.setContentsMargins(10, 10, 10, 10)

        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 1)
        self.grid.setRowStretch(2, 13)
        self.grid.setColumnStretch(0, 1)

        self.sub_grid_1 = QGridLayout()
        self.grid.addLayout(self.sub_grid_1, 0, 0)

        self.sub_grid_1.setRowStretch(0, 1)
        self.sub_grid_1.setColumnStretch(0, 10)
        self.sub_grid_1.setColumnStretch(1, 1)

        self.title_line = create_line(f'Tab {index+1}:')
        self.sub_grid_1.addWidget(self.title_line, 0, 0)

        self.delete_btn = QPushButton('  Delete Tab')
        self.delete_btn.setIcon(QIcon.fromTheme('window-close'))
        self.sub_grid_1.addWidget(self.delete_btn, 0, 1)

        if delete_tab is not None:
            self.delete_btn.clicked.connect(lambda: delete_tab(index))
        else:
            self.delete_btn.setDisabled(True)

        self.sub_grid_2 = QGridLayout()
        self.grid.addLayout(self.sub_grid_2, 1, 0)

        self.sub_grid_2.setRowStretch(0, 1)
        self.sub_grid_2.setColumnStretch(0, 7)
        self.sub_grid_2.setColumnStretch(1, 1)
        self.sub_grid_2.setColumnStretch(2, 1)
        self.sub_grid_2.setColumnStretch(3, 2)

        self.input_line = QLineEdit()
        self.input_line.textChanged.connect(self.trace_input)
        self.input_line.setPlaceholderText('Enter Video URL')
        self.sub_grid_2.addWidget(self.input_line, 0, 0)

        self.paste_btn = QPushButton('  Paste URL')
        self.paste_btn.setIcon(QIcon.fromTheme('edit-paste'))
        self.paste_btn.clicked.connect(lambda: (self.input_line.clear(), self.input_line.setText(QApplication.clipboard().text())))
        self.sub_grid_2.addWidget(self.paste_btn, 0, 1)

        self.clear_btn = QPushButton('  Clear URL')
        self.clear_btn.setIcon(QIcon.fromTheme('list-remove'))
        self.clear_btn.clicked.connect(lambda: self.input_line.clear())
        self.sub_grid_2.addWidget(self.clear_btn, 0, 2)

        self.fetch_btn = QPushButton('⮞ Fetch Response')
        self.fetch_btn.setStyleSheet(styleBtn())
        self.fetch_btn.clicked.connect(self.fetch)
        self.fetch_btn.setDisabled(True)
        self.sub_grid_2.addWidget(self.fetch_btn, 0, 3)

        for wid in [self.input_line, self.title_line, self.delete_btn, self.paste_btn, self.clear_btn, self.fetch_btn]:
            wid.setFixedHeight(28)

        self.output = QScrollArea()
        self.output.setWidget(QWidget())
        self.output.setWidgetResizable(True)
        self.output.wheelEvent = lambda event: None

        self.grid.addWidget(self.output, 2, 0)

        self.output_grid = QGridLayout(self.output.widget())
        self.output_grid.setContentsMargins(10, 10, 10, 10)
        self.output_grid.setSpacing(10)

        self.row_idx = 0
        for row in list(range(10)):
            self.output_grid.setRowStretch(row, 1)
            self.output_grid.setRowMinimumHeight(row, 250)
            if row < 9:
                self.output_grid.addWidget(create_separator(), row, 0, 2, 1, Qt.AlignmentFlag.AlignVCenter)

        self.id = 100
        self.widgets = []
        self.id_widgets = {}
        
    def trace_input(self):
        url = self.input_line.text()
        if url:
            if 'playlist' in url:
                state = Playlist.verify(url)
                self.input_line.setStyleSheet(styleBox(state))
            else:
                state = Video.verify(url)
                self.input_line.setStyleSheet(styleBox(state))
        else:
            state = False
            self.input_line.setStyleSheet(styleApp())
        self.fetch_btn.setEnabled(state)

    def fetch(self, url=None):
        url = self.input_line.text() if not url else url

        if Video.verify(url):
            try:
                self.fetch_btn.setText('⮞ Fetching Video')
                self.fetch_btn.setDisabled(True)
                self.video_widget(url)
            except Exception as error:
                window(
                    self,
                    title='Error Fetching URL',
                    icon='critical',
                    text=f'An error occurred while fetching \n`{url}`:',
                    info_text=f'{error}',
                )
            else:
                for idx, wid in enumerate(self.widgets, 0):
                    self.output_grid.removeWidget(wid)
                    self.output_grid.addWidget(wid, idx, 0)

                if self.row_idx == 9:
                    self.fetch_btn.setDisabled(True)

            finally:
                self.fetch_btn.setEnabled(True)
                self.fetch_btn.setText('⮞ Fetch Response')

        elif ('playlist' in url) and Playlist.verify(url):
            self.fetch_btn.setText('⮞ Fetching Playlist')
            self.setDisabled(True)
            if self.widgets:
                win = window(
                    self,
                    title='Open In New Tab',
                    icon='question',
                    text='Opening a playlist in an active tab may cause lag or errors.\nWould you like to open it in a new tab instead?',
                    info_text=f'Current tab has {len(self.widgets)} Stream.',
                    buttons=['ok', 'cancel'],
                    default='ok'
                )
                if win == QMessageBox.StandardButton.Ok:
                    self.send_url(url)
                self.setEnabled(True)
                self.fetch_btn.setText('⮞ Fetch Response')
            else:

                self.playlist_vids = Playlist.videos(url)
                self.playlist_lens = len(self.playlist_vids)

                if self.playlist_lens > 9:
                    for row in range(self.playlist_lens):
                        self.output_grid.setRowStretch(row, 1)
                        self.output_grid.setRowMinimumHeight(row, 250)
                        if row < self.playlist_lens:
                            self.output_grid.addWidget(create_separator(), row, 0, 2, 1, Qt.AlignmentFlag.AlignVCenter)

                QTimer.singleShot(500, lambda: self.fetch_playlist(url))

    def fetch_playlist(self, url):
        def _continue(videos, index=0):
            if index < len(videos):
                widget = self.video_widget(videos[index])
                self.output_grid.addWidget(widget, index+1, 0)
                QTimer.singleShot(25, lambda: _continue(videos, index+1))
            else:
                self.setEnabled(True)
                self.input_line.setReadOnly(True)
                self.fetch_btn.setText('⮞ Playlist Fetched')
                for btn in [self.fetch_btn, self.clear_btn, self.paste_btn]:
                    btn.setDisabled(True)

        def trace():
            if self.playlist_info is None:
                QTimer.singleShot(100, trace)
                return

            QTimer.singleShot(100, lambda: self.output_grid.addWidget(self.playlist_widget(url), 0, 0))
            QTimer.singleShot(200, lambda: _continue(self.playlist_vids))

        def load():
            self.playlist_info = Playlist.information(url)
        
        self.playlist_info = None
        Thread(target=load, daemon=True).start()
        trace() 

    def video_widget(self, url):
        widget = QWidget()
        widget.setStatusTip(f'{url}')
        
        info = Video.information(url)
        url  = Video.clean(info["url"])

        self.id += 1

        grid = QGridLayout(widget)
        grid.setContentsMargins(10, 10, 5, 10)
        grid.setSpacing(10)

        grid.setRowStretch(0, 1)
        for (i, w) in [(0, 4), (1, 5), (2, 4)]:
            grid.setColumnStretch(i, w)

        grid.addWidget(create_image(url, Thumbnail.get(url), lambda id=self.id: self.download_thumbnail(id)), 0, 0)

        info_layout = QGridLayout()
        grid.addLayout(info_layout, 0, 1)

        for (i, w) in [(0, 1), (1, 1)]:
            info_layout.setColumnStretch(i, w)

        info_layout.addWidget(create_line(f'{info["title"]}'), 0, 0, 1, 2)
        info_layout.addWidget(create_line(f'Author: {info["author"]}'), 1, 0)
        info_layout.addWidget(create_line(f'Published: {info["date"]}'), 1, 1)
        info_layout.addWidget(create_text(f'Description:\n{info["description"]}'), 2, 0, 3, 2)
        info_layout.addWidget(create_line(f'Views: {info["views_formatted"]} ({info["views"]:,} Views)'), 5, 0)
        info_layout.addWidget(create_line(f'Length: {info["length_formatted"]} ({info["length"]:,} Seconds)'), 5, 1)

        streams_layout = QGridLayout()
        streams_layout.setSpacing(10)
        grid.addLayout(streams_layout, 0, 2)

        for (i, w) in [(0, 4), (1, 2), (2, 2)]:
            streams_layout.setRowStretch(i, w)
        for (i, w) in [(0, 1), (1, 1)]:
            streams_layout.setColumnStretch(i, w)

        streams_table = create_video_table(info["streams"])
        streams_layout.addWidget(streams_table, 0, 0, 1, 2)
        
        captions_window = create_captions_window(url, info["title"])
        progress = create_progress()
        streams_layout.addWidget(progress, 2, 0, 2, 2)
        progress.hide()
        
        downlod_stream_btn = QPushButton('Download Stream')
        downlod_stream_btn.setStyleSheet(styleBtn())
        downlod_stream_btn.clicked.connect(lambda _, x=self.id: self.download_video(id=x))
        streams_layout.addWidget(downlod_stream_btn, 1, 0)

        view_captions_btn = QPushButton('View Captions')
        view_captions_btn.setStyleSheet(styleBtn())
        view_captions_btn.clicked.connect(lambda _, x=self.id: self.view_captions(id=x))
        streams_layout.addWidget(view_captions_btn, 1, 1)
        
        title_line = QLineEdit()
        title_line.setPlaceholderText(f'Save As: `{encode(info["title"])}`')
        streams_layout.addWidget(title_line, 2, 0, 1, 2)

        title_line.setMinimumHeight(28)
        for wid in [downlod_stream_btn, view_captions_btn]:
            wid.setFixedHeight(28)
            wid.setFixedWidth(200)

        self.id_widgets[self.id] = {
                'url': url,
                'info': info,

                'captions_btn' : view_captions_btn,
                'stream_btn': downlod_stream_btn,
                'title_line': title_line,
                'streams_table': streams_table,
                'captions_window': captions_window,
                'progress': progress,

                'state': 0,
                'process': [0, 0],
        }

        self.row_idx += 1
        self.widgets.insert(0, widget)
        
        return widget

    def playlist_widget(self, url):
        widget = QWidget()
        widget.setStatusTip(f'{url}')

        grid = QGridLayout(widget)
        grid.setContentsMargins(10, 10, 0, 10)
        grid.setSpacing(10)

        for (i, w) in [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]:
            grid.setRowStretch(i, w)

        for (i, w) in [(0, 5), (1, 5), (2, 5),     (3, 15)]:
            grid.setColumnStretch(i, w)

        info = self.playlist_info

        grid.addWidget(create_line(f'Title: {info["title"]}'), 0, 0, 1, 3)
        
        grid.addWidget(create_line(f'Owner: {info["owner"]}'), 1, 0, 1, 2)
        grid.addWidget(create_line(f'Playlist Videos: {info["videos_number"]} Videos.'), 1, 2)
        
        grid.addWidget(create_text(f'Description:\n{info["description"]}'), 2, 0, 3, 2)
        
        grid.addWidget(create_line(f'Views: {info["views_formatted"]} ({info["views"]:,} Views)'), 2, 2)
        grid.addWidget(create_line(f'Length: {info["length_formatted"]} ({info["length"]} Seconds)'), 3, 2)
        grid.addWidget(create_line(f'Last Modified: {info["last_modified"]}'), 4, 2)
        
        grid.addWidget(create_line(f'{info["url"]}'), 5, 0, 1, 3)

        videos_table = create_playlist_table(
            info["videos_titles"],
            info["videos_urls"],
            info["videos_lens_formatted"],
            info["videos_views"]
        )
        grid.addWidget(videos_table, 0, 3, 4, 1)

        sub_grid = QGridLayout()
        sub_grid.setSpacing(10)
        sub_grid.setContentsMargins(0, 0, 10, 0)
        grid.addLayout(sub_grid, 4, 3, 2, 2)

        for (i, w) in [(0, 1), (1, 1)]:
            sub_grid.setRowStretch(i, w)

        for (i, w) in [(0, 1), (1, 1), (2, 1)]:
            sub_grid.setColumnStretch(i, w)

        progress = create_progress()
        sub_grid.addWidget(progress, 1, 1, 1, 2)
        progress.hide()

        download_playlist_btn = QPushButton('Download Playlist')
        download_playlist_btn.setStyleSheet(styleBtn())
        download_playlist_btn.clicked.connect(lambda: self.download_playlist())

        download_selected_btn = QPushButton('Download Selected')
        download_selected_btn.setStyleSheet(styleBtn())
        download_selected_btn.clicked.connect(lambda: self.download_playlist(selected=True))

        plot_stats_btn = QPushButton('Playlist Statistics')
        plot_stats_btn.setStyleSheet(styleBtn())
        plot_stats_btn.clicked.connect(self.plot_playlist_table)

        save_stats_btn = QPushButton('Save Playlist Table')
        save_stats_btn.setStyleSheet(styleBtn())
        save_stats_btn.clicked.connect(self.save_playlist_table)

        title_line = QLineEdit()
        title_line.setPlaceholderText(f'Save As: `{info["title"]}`')

        sub_grid.addWidget(download_playlist_btn, 0, 0)
        sub_grid.addWidget(download_selected_btn, 1, 0)
        sub_grid.addWidget(plot_stats_btn, 0, 1)
        sub_grid.addWidget(save_stats_btn, 0, 2)
        sub_grid.addWidget(title_line, 1, 1, 1, 2)
        
        for btn in [download_playlist_btn, download_selected_btn, plot_stats_btn, save_stats_btn]:
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        title_line.setMinimumHeight(28)
        for wid in [download_playlist_btn, download_selected_btn, plot_stats_btn, save_stats_btn]:
            wid.setFixedHeight(28)

        #* Let `100` be fixed id for playlist, since each tab can only hold one.
        self.id_widgets[100] = {
                'url': url,
                'videos_url': info["videos_urls"],
                'videos_title': info["videos_titles"],

                'videos_table' : videos_table,
                'playlist_btn': download_playlist_btn,
                'selected_btn': download_selected_btn,
                'plot_stats_btn': plot_stats_btn,
                'save_stats_btn': save_stats_btn,
                'title_line': title_line,
                'progress': progress,

                'state': 0,
                'process': [0, 0],
        }

        self.row_idx += 1
        self.widgets.insert(0, widget)
        
        return widget

    def download_thumbnail(self, id):
        video_wid = self.id_widgets[id]
        try:
            filepath, _ = QFileDialog.getSaveFileName(
                self, 
                'Save Thumbnail',
                f'[Thumbnail]-{encode(video_wid['info']['title'])}.png',
                'Images (*.png *.jpg *.jpeg)'
            )

            if filepath:
                if filepath.split('.')[-1] not in ['png', 'jpg', 'jpeg']:
                    filepath += '.png'

                Thumbnail.download(video_wid['url'], filepath=filepath)

        except Exception as e:
            self.setStatusTip('Downloading Thumbnail')
            window(
                self,
                title='Thumbnail Download Failed',
                icon='critical',
                text=f'Error:\n{e}',
            )
        else:
            self.setStatusTip('Thumbnail Downloaded')

    def download_video(self, id, path=''):
        if not path:
            path = self.path()

        video_wid = self.id_widgets[id]

        url = video_wid["url"]
        line = video_wid["title_line"]
        button = video_wid["stream_btn"]
        progress = video_wid["progress"]
        
        streams = get_selected_streams(video_wid["streams_table"])

        def callback(stream, chunk, bytes_remaining):
            video_wid["process"] = [(stream.filesize - bytes_remaining) / (1024 * 1024), stream.filesize / (1024 * 1024)]

        def after():
            video_wid["state"] = 2

        def merging():
            video_wid["state"] = 3

        def deleting():
            video_wid["state"] = 4

        def trace_download():
            progress.set_value(video_wid["process"][0], video_wid["process"][1], prefix='', postfix='MB')
            if video_wid["state"] == 2:
                button.setText('Download Stream')
                button.setEnabled(True)
                progress.set_labels()
                Tab.swap(line, progress)

                if not getattr(self, 'downloading_playlist', False):
                    window(
                        self,
                        title='Download Complete',
                        icon='info',
                        text='The video was downloaded successfully.',
                        info_text=f'Saved to:\n{path}',
                    )
                else:
                    self.playlist_process += 1
            elif video_wid["state"] == 3:
                progress.set_central('Muxing Streams')
                QTimer.singleShot(25, trace_download)
            elif video_wid["state"] == 4:
                progress.set_central('Deleting Temporary Files')
                QTimer.singleShot(25, trace_download)
            else:
                QTimer.singleShot(50, trace_download)

        try:
            if len(streams) == 1:   # Audio, Video, or Compined
                if not getattr(self, 'downloading_playlist', False):
                    win = window(
                        self,
                        title='Confirm Download',
                        icon='question',
                        text=f'You have selected:\n    - {streams[0]["mode"]}: {streams[0]["data"]}\n        - Size: {streams[0]["size"]} MB.',
                        info_text='Confirm downloading this stream?',
                        buttons=['yes', 'no'],
                        default='yes'
                    )
                    if win != QMessageBox.StandardButton.Yes:
                        return

                button.setText('Downloading...')
                button.setDisabled(True)

                video_wid["state"] = 1
                video_wid["process"] = [0, float(streams[0]["size"])]
                Tab.swap(progress, line)
                
                stream = streams[0]
                if stream["mode"].startswith('C'):
                    abr, res = stream["data"].split('-')
                    Thread(
                        target=lambda: Video.download(url, res, abr, path, line.text(), callback=callback, after=after),
                        daemon=True
                    ).start()
                elif stream["mode"].startswith('A'):
                    abr = stream["data"]
                    Thread(
                        target=lambda: Video.download_audio(url, abr, path, line.text(), callback=callback, after=after),
                        daemon=True
                    ).start()
                elif stream["mode"].startswith('V'):
                    res = stream["data"]
                    Thread(
                        target=lambda: Video.download_video(url, res, path, line.text(), callback=callback, after=after),
                        daemon=True
                    ).start()

                trace_download()

            elif len(streams) == 2: # Audio and Video
                if not getattr(self, 'downloading_playlist', False):
                    win = window(
                        self,
                        title='Confirm Download',
                        icon='question',
                        text=f'You have selected:\
                          \n    - {streams[0]["mode"]}: {streams[0]["data"]}\n        - Size: {streams[0]["size"]} MB.\
                          \n    - {streams[1]["mode"]}: {streams[1]["data"]}\n        - Size: {streams[1]["size"]} MB.\
                          \n\n    Total Size: {(float(streams[0]["size"]) + float(streams[1]["size"])):.2f} MB.',
                        info_text='Confirm downloading and merging these streams?',
                        buttons=['yes', 'no'],
                        default='yes'
                    )
                    if win != QMessageBox.StandardButton.Yes:
                        return
                
                button.setText('Downloading...')
                button.setDisabled(True)

                video_wid["state"] = 1
                video_wid["process"] = [0, float(streams[0]["size"])]
                Tab.swap(progress, line)
                
                Thread(
                    target=lambda: Video.download_and_merge(
                        url=url,
                        id=id,
                        resolution=streams[1]["data"],
                        abr=streams[0]["data"],
                        filepath=path,
                        filename=line.text(),
                        callback=callback,
                        after=after,
                        merging=merging,
                        deleting=deleting
                        ),
                    daemon=True).start()

                trace_download()
            else:
                raise ValueError('No streams was selected to download.')

        except Exception as e:
            window(
                self,
                title='Download Failed',
                icon='critical',
                text='An error occurred while downloading the stream:',
                info_text=f'URL: {url}\nError: {e}',
                detailed_text=f'Stream: {streams}'
            )

    def view_captions(self, id):
        video_wid = self.id_widgets[id]
        btn = video_wid["captions_btn"]
        win = video_wid["captions_window"]

        btn.setDisabled(True)

        try:
            def close(event):
                win.cancel_translation()
                win.hide()
                btn.setEnabled(True)
                event.ignore()
            win.closeEvent = close

            QTimer.singleShot(500, lambda: win.show())
            
        except Exception as e:
            window(
                self,
                title='Some Error Occurred',
                icon='error',
                text='Could not view the video captions due to an error',
                info_text=f'{e}',
            )

    def download_playlist(self, selected=False):
        playlist_wid = self.id_widgets[100]

        url = playlist_wid["url"]
        line = playlist_wid["title_line"]
        table = playlist_wid["videos_table"]
        button = playlist_wid["playlist_btn"] if not selected else playlist_wid["selected_btn"]
        progress = playlist_wid["progress"]

        def trace_download():
            if self.playlist_process == self.playlist_process_len:
                self.id_widgets[100]['state'] = 2
                button.setText(f'Download {"Playlist" if not selected else "Selected"}')
                [btn.setEnabled(True) for btn in (playlist_wid["playlist_btn"], playlist_wid["selected_btn"])]
                Tab.swap(line, progress)
                window(
                    self,
                    title='Download Complete',
                    icon='info',
                    text='The playlist was downloaded successfully.',
                    info_text=f'Saved to:\n{path}',
                )
            else:
                progress.set_value(self.playlist_process, self.playlist_process_len, prefix='', postfix='Videos Downloaded', force=True)
                QTimer.singleShot(500, trace_download)

        if selected: 
            videos = [vid[0] for vid in get_selected_items(table) if vid[1]]
        else:
            videos = playlist_wid["videos_url"]

        map = {url: title for url, title in zip(playlist_wid["videos_url"], playlist_wid["videos_title"])}
        win = window(
            self,
            title='Download Playlist Videos',
            icon='question',
            text=f'You have selected: {"" if selected else "(All Videos)"}\n{"\n".join(f"  - {map[url]}" for url in videos)}',
            info_text='Confirm downloading the selected videos?',
            buttons=['yes', 'no'],
            default='yes'
        )
        if win != QMessageBox.StandardButton.Yes:
            return

        path = Playlist.make_directory(url, self.path(), line.text())

        button.setText('Downloading...')
        [btn.setDisabled(True) for btn in (playlist_wid["playlist_btn"], playlist_wid["selected_btn"])]
        
        Tab.swap(progress, line)

        self.playlist_process = 0
        self.downloading_playlist = True
        if not selected:
            self.playlist_process_len = len(playlist_wid["videos_url"])

            for url in playlist_wid["videos_url"]:
                for id, vid in self.id_widgets.items():
                    if vid["url"] == url:
                        self.download_video(id=id, path=path)
                        continue

            trace_download()
        else:
            self.playlist_process_len = [vid[1] for vid in get_selected_items(table)].count(True)
            for (url, select) in get_selected_items(table):
                if select:
                    for id, vid in self.id_widgets.items():
                        if vid["url"] == url:
                            self.download_video(id=id, path=path)
                            continue
            trace_download()

    def plot_playlist_table(self):
        btn = self.id_widgets[100]['plot_stats_btn']
        btn.setDisabled(True)
        visualize_table(self.id_widgets[100]['videos_table'])
        btn.setEnabled(True)

    def save_playlist_table(self):
        url = self.id_widgets[100]['url']
        btn = self.id_widgets[100]['save_stats_btn']
        tree = self.id_widgets[100]['videos_table']
        line = self.id_widgets[100]['title_line']
        
        data, root = [], tree.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            row = {
                'Title': item.text(1),
                'Length': item.text(2),
                'Views': item.text(3),
                'URL': item.text(4)
            }
            data.append(row)

        filename = f'{Playlist.make_directory(url, self.path(), line.text())}-[Table].json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        btn.setText('Playlist Table Saved')
        btn.setDisabled(True)

    @staticmethod
    def swap(to_show: QWidget, to_hide: QWidget, duration=500):
        def after_out():
            to_hide.hide(); to_show.show()
            anim_in = QPropertyAnimation(to_show._effect, b'opacity')
            anim_in.setDuration(duration)
            anim_in.setStartValue(0)
            anim_in.setEndValue(1)
            anim_in.setEasingCurve(QEasingCurve.Type.InOutQuad)
            anim_in.start()
            to_show._anim = anim_in

        for w, start_opacity in ((to_hide, 1), (to_show, 0)):
            if not isinstance(w.graphicsEffect(), QGraphicsOpacityEffect):
                eff = QGraphicsOpacityEffect(w)
                w.setGraphicsEffect(eff)
                w._effect = eff
            w._effect.setOpacity(start_opacity)

        anim_out = QPropertyAnimation(to_hide._effect, b'opacity')
        anim_out.setDuration(duration)
        anim_out.setStartValue(1)
        anim_out.setEndValue(0)
        anim_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_out.finished.connect(after_out)
        anim_out.start()
        to_hide._anim = anim_out

    @property
    def has_process(self):
        states = [video["state"] for video in list(self.id_widgets.values())]
        return (0 in states) or (1 in states) or (3 in states)

    @property
    def sum_process(self):
        states = [video["state"] for video in list(self.id_widgets.values())]
        return states.count(0) + states.count(1)
