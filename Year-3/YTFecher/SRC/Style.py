
import os, sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from threading import Thread

from SRC.Service import Script, encode

def setIcon(relative:str=r'Icon.ico') -> str:
    if hasattr(sys, '_MEIPASS'):
        return QIcon(os.path.join(sys._MEIPASS, relative))
    return QIcon(os.path.join(os.path.abspath('.'), relative))

def styleApp():
    return '''
    QMainWindow {
        background-color: #252525;
    }

    QMenuBar {
        background-color: #202020;
        color: #e0e0e0;
        border-bottom: 1px solid #404040;
        min-height: 30px;
    }
    QMenuBar::item {
        background: transparent;
        padding: 0px 12px;
        margin: 2px;
        border-radius: 4px;
    }
    QMenuBar::item:selected {
        background: #404040;
        color: #ffffff;
    }
    QMenuBar::item:pressed {
        background: #606060;
        color: #ffffff;
    }
    QMenuBar::item:disabled {
        color: #606060;
        background: #303030;
    }
    QStatusBar {
        background-color: #202020;
        color: #e0e0e0;
        border-top: 1px solid #404040;
        min-height: 30px;

    }
    QStatusBar QWidget {
        background-color: transparent;
        padding: 2px 6px;
        margin: 2px;
        border-radius: 4px;
        color: #e0e0e0;
    }
    QStatusBar QWidget:hover {
        background-color: #404040;
        color: #ffffff;
    }
    QStatusBar QWidget:disabled {
        color: #606060;
        background: #303030;
    }
    QStatusBar::item {
        border: none;
    }

    QTabWidget::pane {
        border: 1px solid #404040;
        border-radius: 4px;
    }
    QTabBar::tab {
        color: #ffffff;
        padding: 2px;
        margin-left: 4px;
        border: 0.5px solid #303030;
        border-top-left-radius: 2px;
        border-top-right-radius: 2px;
        border-bottom: 2px solid #404040;
    }
    QTabBar::tab:selected {
        background-color: #400000;
        border-bottom: 2px solid #404040;
    }
    QTabBar::tab:hover {
        border: 0.5px solid #606060;
        border-bottom: 2px solid #606060;
        background-color: #303030;
    }
    QTabBar::tab:selected:hover {
        border: 0.5px solid #404040;
        border-bottom: 2px solid #404040;
        background-color: #350000;
    }

    QScrollArea {
        background-color: #202020;
        border: 1px solid #404040;
        border-radius: 6px;
        margin: 4px;
        padding: 2px;
    }
    QScrollArea > QWidget {
        background-color: #303030;
        border-radius: 4px;
        margin: 2px;
    }
    QPushButton {
        color: #ffffff;
        background-color: #303030;
        border: 1px solid #404040;
        border-radius: 4px;
        padding: 4px 8px;
    }
    QPushButton:hover {
        background-color: #400000;
        border-color: #505050;
    }
    QPushButton:pressed {
        background-color: #300000;
        border-color: #404040;
    }
    QPushButton:disabled {
        color: #707070;
        border-color: #404040;
    }
    QDialogButtonBox QPushButton {
        min-width: 65px;
    }
    QTextEdit, QLineEdit {
        background-color: #404040;
        border: 0.5px solid #303030;
        border-bottom: 2px solid #606060;
        border-radius: 4px;
        padding: 1.5px;
    }
    QTextEdit:focus, QLineEdit:focus {
        background-color: #404040;
        border: 0.5px solid #505050;
        border-bottom: 2px solid #AAAAAA;
        border-radius: 4px;
        padding: 1.5px;
    }
    QTextEdit:read-only, QLineEdit:read-only {
        background-color: #353535;
        border: 1px solid #353535;
        border-radius: 4px;
        padding: 1.5px;
    }
    QProgressBar {
        border: none;
        border-radius: 20px;
        background: #404040;
    }
    QProgressBar::chunk {
        margin: 0px;
        border-radius: 20px;
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0   #600000,
            stop:1   #200000
        );
    }

    QListWidget {
        background-color: #202020;
        border: 1px solid #404040;
        border-radius: 4px;
        padding: 1px;
        color: #e0e0e0;
        selection-background-color: #400000;
        selection-color: #ffffff;
        outline: 0;
    }

    QListWidget::item {
        background-color: #303030;
        color: #ffffff;
        padding: 4px 8px;
        margin: 2px 0px;
        border-radius: 4px;
    }
    QListWidget::item:hover {
        background-color: #404040;
        color: #ffffff;
    }

    QListWidget::item:selected {
        background-color: #400000;
        color: #ffffff;
    }
    QListWidget::item:selected:hover {
        background-color: #600000;
        color: #ffffff;
    }

    QListWidget::item:disabled {
        background-color: #303030;
        color: #606060;
    }
    QRadioButton {
        spacing: 8px;
        color: #ffffff;
        background-color: transparent;
        padding: 2px 4px;
        border-radius: 8px;
    }
    QRadioButton::indicator {
        width: 16px;
        height: 16px;
        border-radius: 8px;
        border: 2px solid #404040;
        background-color: #303030;
    }
    QRadioButton::indicator:hover {
        border: 2px solid #606060;
        background-color: #404040;
    }
    QRadioButton::indicator:checked {
        border: 2px solid #404040;
        background-color: #400000;
    }
    QRadioButton::indicator:checked:hover {
        border: 2px solid #606060;
        background-color: #600000;
    }

    '''

def styleBox(valid=False):
    if valid:
        return '''
        QTextEdit, QLineEdit {
        background-color: #404040;
        border: 0.5px solid #303030;
        border-bottom: 2px solid #008000;
        border-radius: 4px;
        padding: 1.5px;
        }'''
    return '''
    QTextEdit, QLineEdit {
    background-color: #404040;
    border: 0.5px solid #303030;
    border-bottom: 2px solid #800000;
    border-radius: 4px;
    padding: 1.5px;
    }'''

def styleBtn():
    return '''
    QPushButton {
        color: #ffffff;
        background-color: #400000;
        border: 1px solid #505050;
        border-radius: 4px;
        padding: 4px 8px;
    }

    QPushButton:hover {
        background-color: #350000;
        border-color: #454545;
    }
    QPushButton:pressed {
        background-color: #250000;
        border-color: #353535;
    }
    QPushButton:disabled {
        color: #707070;
        border-color: #404040;
    }'''

def styleTree(video=True):
    if video:
        return '''
        QHeaderView::section {
            background-color: #353535;
            color: white;
            font-weight: bold;
        }
        QTreeWidget {
            alternate-background-color: #252525;
            background-color: #202020; 
            color: #ffffff;
            border: 1px solid #404040;
            show-decoration-selected: 1; 
        }
        QTreeWidget::item {
            padding: 2px 2px;
        }
        QTreeWidget::item:hover {
            background-color: #404040;
            color: #ffffff;
        }
        QTreeWidget::item:selected {
            background-color: #606060;
            color: #ffffff;
        }
        QTreeWidget::item:selected:!active {
            background-color: #505050;
            color: #ffffff;
        }
        QTreeWidget::item:disabled {
            background-color: #303030;
            color: #888888;
        }
        QTreeWidget::item:disabled:hover {
            background-color: #303030;
            color: #888888;
        }
        QTreeWidget::indicator {
            width: 14px;
            height: 14px;
            border: 1px solid #606060;
            border-radius: 3px;
            margin-top: 5px;
            margin-bottom: 5px;
            margin-left: 60px;
            background-color: #303030;
        }
        QTreeWidget::indicator:hover {
            border: 1px solid #909090;
            background-color: #606060;
        }
        QTreeWidget::indicator:checked {
            background-color: #A00000;
            border: 1px solid #606060;
        }
        QTreeWidget::indicator:indeterminate {
            background-color: #808080;
        }'''
    return styleTree().replace('60px', '10px')

# ToDo: ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

def create_separator():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line

def create_image(url:str, image:np.ndarray, download:callable):
    class ImageWidget(QWidget):
        def __init__(self, url: str, matrix: np.ndarray, download: callable):
            super().__init__()
            
            self.url = url
            self.download_thumbnail = download
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            
            self.matrix = cv.cvtColor(matrix, cv.COLOR_BGR2RGB) 
            self.h, self.w, _ = matrix.shape

            self.image = QLabel()
            self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.image.setPixmap(self.pixmap(self.size()))

            self.grid = QGridLayout(self)
            self.grid.setContentsMargins(0, 0, 0, 0)
            self.grid.addWidget(self.image)

        def pixmap(self, size):
            return QPixmap.fromImage(QImage(self.matrix.data, self.w, self.h, self.w * 3, QImage.Format.Format_RGB888)).scaled(
                size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        def resizeEvent(self, event):
            self.image.setPixmap(self.pixmap(self.size()))
            super().resizeEvent(event)

        def mousePressEvent(self, event):        
            menu = QMenu(self)

            open_action = QAction(QIcon.fromTheme('go-up'), 'Open Video URL', self)
            copy_action = QAction(QIcon.fromTheme('edit-copy'), 'Copy Video URL', self)
            download_action = QAction(QIcon.fromTheme('emblem-downloads'), 'Download Thumbnail', self)
            
            copy_action.triggered.connect(lambda: QApplication.clipboard().setText(self.url))
            open_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(self.url)))
            download_action.triggered.connect(lambda: self.download_thumbnail())

            menu.addAction(open_action)
            menu.addAction(copy_action)
            menu.addSeparator()
            menu.addAction(download_action)

            menu.exec(self.mapToGlobal(event.pos()))

    return ImageWidget(url, image, download)

def create_progress():
    class LabeledProgress(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setFixedHeight(28)

            self.layout = QGridLayout(self)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(5)

            self.lbl_l = QLabel('--.-/--.-', self)
            self.lbl_l.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            self.lbl_r = QLabel('--.--%', self)
            self.lbl_r.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            self.lbl_c = QLabel('', self)
            self.lbl_c.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            self.lbl_c.hide()

            self.bar = QProgressBar(self)
            self.bar.setTextVisible(False)
            self.bar.setMaximum(100)
            self.bar.setMinimum(0)
            self.bar.setValue(0)
            self.bar.setFixedHeight(5)

            self.layout.addWidget(self.lbl_l, 0, 0, Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(self.lbl_r, 0, 0, Qt.AlignmentFlag.AlignRight)
            self.layout.addWidget(self.lbl_c, 0, 0, Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.bar, 1, 0, 1, 1)
            self.setLayout(self.layout)

        def set_value(self, now:float, max:float, prefix:str='', postfix:str='', force:bool=False):
            percent = (now / max) * 100 if max else 0
            self.bar.setValue(int(percent))
            self.lbl_r.setText(f'{percent:.2f}%')

            if force:
                self.lbl_l.setText(f'{now}/{max} {postfix}')
            else:
                self.lbl_l.setText(f'{prefix} {round(now, 1):.1f}/{round(max, 1):.1f} {postfix}')

        def set_labels(self):
            self.lbl_c.hide()
            self.lbl_l.show()
            self.lbl_r.show()

        def set_central(self, text:str):
            self.lbl_l.hide()
            self.lbl_r.hide()
            self.lbl_c.show()
            self.lbl_c.setText(f'{text}')
            
    return LabeledProgress()

def create_line(text:str):
    line = QLineEdit()
    line.setReadOnly(True)
    line.setStyleSheet(styleApp())
    line.setText(f'{text}')
    line.setFixedHeight(28)
    return line

def create_text(text:str):
    box = QTextEdit()
    box.setStyleSheet(styleApp())
    box.setText(f'{text}')
    box.setReadOnly(True)
    box.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    box.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    return box

def create_video_table(streams:dict):
    def add_streams(parent_name, data):
        parent = QTreeWidgetItem([parent_name])
        
        for key, value in data.items() if isinstance(data, dict) else enumerate(data):
            if isinstance(data, dict):
                text = f'{key}'
                size = str(value)
            else:
                text = f'{data[key]["abr"]}' if 'abr' in data[key] else str(data[key])
                size = str(data[key]['size'])
                
            item = QTreeWidgetItem([text, size])
            item.setTextAlignment(0, Qt.AlignmentFlag.AlignCenter)
            item.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(2, Qt.CheckState.Unchecked)
            parent.addChild(item)

        tree.addTopLevelItem(parent)
        return parent

    def enforce_selection(item, column):
        if item.parent() == combined_parent and item.checkState(column) == Qt.CheckState.Checked:
            if audio_parent:
                for i in range(audio_parent.childCount()):
                    audio_parent.child(i).setCheckState(2, Qt.CheckState.Unchecked)
            if video_parent:
                for i in range(video_parent.childCount()):
                    video_parent.child(i).setCheckState(2, Qt.CheckState.Unchecked)

        if (item.parent() == audio_parent or item.parent() == video_parent) and item.checkState(column) == Qt.CheckState.Checked:
            if combined_parent:
                for i in range(combined_parent.childCount()):
                    combined_parent.child(i).setCheckState(2, Qt.CheckState.Unchecked)

        parent = item.parent()
        if parent:
            for i in range(parent.childCount()):
                child = parent.child(i)
                if child != item:
                    child.setCheckState(2, Qt.CheckState.Unchecked)
    
    tree = QTreeWidget()
    tree.setStyleSheet(styleTree())
    tree.setColumnCount(3)
    tree.setHeaderLabels(['File Details', 'Size', 'Download'])
    tree.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
    tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    tree.setAlternatingRowColors(True)

    audio_parent = None
    if 'audio' in streams:
        audio_parent = add_streams('Audio Streams', streams['audio'])

    video_parent = None
    if 'video' in streams:
        video_parent = add_streams('Video Streams', streams['video'])

    combined_parent = None
    if 'combined' in streams:
        combined_parent = add_streams('Combined A/V Streams', streams['combined'])

    tree.itemChanged.connect(lambda item, column: enforce_selection(item, column))
    tree.expandItem(combined_parent)
    
    for idx, wid in [(0, 150), (1, 125), (2, 50)]:
        tree.setColumnWidth(idx, wid)
        tree.header().setSectionResizeMode(idx, QHeaderView.ResizeMode.Fixed)

    if combined_parent and combined_parent.childCount() > 0:
        combined_parent.child(0).setCheckState(2, Qt.CheckState.Checked)
    else:
        video_parent.child(0).setCheckState(2, Qt.CheckState.Checked)

    return tree

def get_selected_streams(tree: QTreeWidget) -> list:
    result = []
    for i in range(tree.topLevelItemCount()):
        parent = tree.topLevelItem(i)

        for j in range(parent.childCount()):
            child = parent.child(j)
            if child.checkState(2) == Qt.CheckState.Checked:
                result.append({
                    'mode': parent.text(0),
                    'data': child.text(0),
                    'size': child.text(1),
                })

    return result

def create_playlist_table(videos_titles:list, videos_urls:list, videos_lens:list, videos_views:list):
    tree = QTreeWidget()
    tree.setStyleSheet(styleTree(False))
    tree.setColumnCount(5)
    tree.setHeaderLabels(['Select', 'Title', 'Length', 'Views', 'URL'])
    tree.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
    tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
    tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    tree.setAlternatingRowColors(True)
    
    for idx, wid in [(0, 80), (2, 300), (2, 80), (3, 80), (4, 200)]:
        tree.setColumnWidth(idx, wid)

    for title, length, views, url in zip(videos_titles, videos_lens, videos_views, videos_urls):
        item = QTreeWidgetItem(['', str(title), str(length), str(views), str(url)])
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(0, Qt.CheckState.Checked)

        for i in (0, 1, 2, 3, 4):
            item.setTextAlignment(i, Qt.AlignmentFlag.AlignCenter)

        tree.addTopLevelItem(item)
        
    return tree

def get_selected_items(tree: QTreeWidget) -> list[tuple[str, bool]]:
    result = []
    for i in range(tree.topLevelItemCount()):
        item = tree.topLevelItem(i)
        result.append((item.text(4), item.checkState(0) == Qt.CheckState.Checked))
    return result

def visualize_table(tree: QTreeWidget):
    def shorten(t: str) -> str:
        return (t[:10] + '...') if len(t) > 10 else t

    def to_seconds(s: str) -> int:
        s = str(s).strip()
        if s.isdigit():
            return int(s)
        parts = s.split(':')
        try:
            if len(parts) == 2:
                m, sec = map(int, parts)
                return m * 60 + sec
            elif len(parts) == 3:
                h, m, sec = map(int, parts)
                return h * 3600 + m * 60 + sec
        except Exception:
            pass
        return 0

    titles, lengths, views = [], [], []
    for i in range(tree.topLevelItemCount()):
        item = tree.topLevelItem(i)
        titles.append(item.text(1))
        lengths.append(item.text(2))
        views.append(int(item.text(3)) if item.text(3).isdigit() else 0)

    x = range(len(titles))
    x_labels = [shorten(t) for t in titles]

    fig, (ax_l, ax_v) = plt.subplots(2, 1, figsize=(8, 6))
    fig.patch.set_facecolor('#101010')
    ax_l.set_facecolor('#101010')
    ax_v.set_facecolor('#101010')
    
    ax_l.plot(x, [to_seconds(l) for l in lengths], color='#800000', linewidth=2, marker='o', markersize=4, markerfacecolor='#400000')
    ax_l.set_title('Video Length', color='w', pad=10)

    ax_v.plot(x, views, color='#800000', linewidth=2, marker='o', markersize=4, markerfacecolor='#400000')
    ax_v.set_title('Video Views', color='w', pad=10)

    for ax in [ax_l, ax_v]:
        ax.set_xticks(list(x))
        ax.set_xticklabels(x_labels, ha='right', color='w', fontstyle='normal')
        ax.tick_params(axis='y', colors='w')
        ax.grid(True, color='#252525', linestyle='dotted', linewidth=0.5)

        for spine in ax.spines.values():
            spine.set_color('#AAAAAA')

    fig.tight_layout()
    plt.show()

def create_captions_window(url:str, title:str=''):
    class Window(QWidget):
        def __init__(self, url:str, title:str):
            super().__init__()
            self.url = url
            self.title = title
            
            self.setWindowTitle('Video Captions')
            self.setFixedWidth(750)
            self.setFixedHeight(325)

            self.layout = QGridLayout(parent=self)
            self.layout.setContentsMargins(10, 10, 10, 10)
            self.layout.setSpacing(10)

            self.layout.setRowStretch(0, 2)
            self.layout.setRowStretch(1, 1)
            self.layout.setRowStretch(2, 7)

            self.layout.setColumnStretch(0, 2)
            self.layout.setColumnStretch(1, 1)
            self.layout.setColumnStretch(2, 2)
            self.layout.setColumnStretch(3, 1)

            self.preview_line = create_line('Available Captons:')
            self.layout.addWidget(self.preview_line, 0, 0)

            self.preview_btn = QPushButton('Preview')
            self.preview_btn.setStyleSheet(styleBtn())
            self.preview_btn.clicked.connect(self.preview_caption)
            self.layout.addWidget(self.preview_btn, 0, 1)

            self.captions_list = QListWidget()
            self.layout.addWidget(self.captions_list, 1, 0, 2, 2)

            self.translate_line = create_line('Translate To:')
            self.layout.addWidget(self.translate_line, 0, 2)

            self.translate_btn = QPushButton('Translate')
            self.translate_btn.setStyleSheet(styleBtn())
            self.translate_btn.clicked.connect(self.translate_caption)
            self.layout.addWidget(self.translate_btn, 0, 3)
            
            batch_layout = QHBoxLayout()
            batch_layout.setContentsMargins(1, 0, 3, 0)
            
            self.batch_boxes = [
                QRadioButton('Line-by-Line'),
                QRadioButton('3-Line Batch'),
                QRadioButton('5-Line Batch'),
                QRadioButton('Full Merge')
            ]
            self.batch_boxes[3].setChecked(True)
            for b in self.batch_boxes:
                b.setDisabled(True)

            for radio in self.batch_boxes:
                batch_layout.addWidget(radio)

            self.layout.addLayout(batch_layout, 1, 2, 1, 2)
            
            self.translate_btn.setDisabled(True)

            self.languages_list = QListWidget()
            self.layout.addWidget(self.languages_list, 2, 2, 1, 2)

            self.text_box = create_text(f'\n\t   〈〈〈  Fetching Video Captions  〉〉〉')

            self.save_btn = QPushButton('Save Captions')
            self.save_btn.setStyleSheet(styleBtn())
            self.save_btn.clicked.connect(self.save_captions)            
            self.save_btn.setDisabled(True)
            self.save_btn.setFixedWidth(120)

            for wid in [self.preview_btn, self.translate_btn, self.save_btn]:
                wid.setFixedHeight(28)

            self.fill_lists()

        def fill_lists(self):
            def update_c_line(*args, **kwargs):
                text = self.captions_list.currentItem().text()
                self.preview_line.setText(f'Selected: {text.split(':')[0]}')

            def update_l_line(*args, **kwargs):
                text = self.languages_list.currentItem().text()
                self.translate_line.setText(f'Translate To: {text.split(':')[0]}')

            self.captions_list.addItems(Script.explore(self.url))
            self.languages_list.addItems([
                'Arabic: `AR`',
                'English: `EN`',
                'Spanish: `ES`',
                'Italian: `IT`',
                'French: `FR`',
                'German: `DE`',
                'Lithuanian: `LT`',
            ])

            self.captions_list.setCurrentRow(0)
            self.languages_list.setCurrentRow(0)

            self.captions_list.clicked.connect(update_c_line)
            self.languages_list.clicked.connect(update_l_line)

            if self.captions_list.currentItem() is None:
                self.preview_btn.setDisabled(True)
                self.translate_btn.setDisabled(True)
                self.languages_list.setDisabled(True)
                self.preview_line.setText('Available:  No captions found')
                self.translate_line.setText('Translate To:  None')
            else:
                update_c_line()
                update_l_line()

        def preview_caption(self):
            def load(code):
                self.caption = Script.get(self.url, code)
                self.caption_f = Script.format(self.caption)
                self.loaded = True

            def trace_loading():
                if self.loaded:
                    self.text_box.setText(f'{self.caption_f}')
                    for w in [*self.batch_boxes, self.preview_btn, self.translate_btn, self.save_btn]:
                        w.setEnabled(True)
                    self.preview_lang = self.captions_list.currentItem().text().split(':')[0]
                    return
                QTimer.singleShot(50, trace_loading)

            self.setFixedHeight(400)
            self.layout.setRowStretch(3, 10)
            self.layout.setRowStretch(4, 2)
            
            self.layout.addWidget(self.text_box, 3, 0, 1, 4)
            self.layout.addWidget(self.save_btn, 4, 0, 1, 4, Qt.AlignmentFlag.AlignCenter)

            code = self.captions_list.currentItem().text().split('`')[1].lower()

            self.loaded = False
            self.preview_btn.setDisabled(True)
            self.translate_btn.setDisabled(True)

            Thread(target=lambda: load(code=code), daemon=True).start()
            QTimer.singleShot(50, trace_loading)

        def translate_caption(self):
            def read_batch():
                for b in self.batch_boxes:
                    if b.isChecked():
                        return {'L': 1, '3': 3, '5': 5, 'F': 'ALL'}.get(b.text()[0], 'ALL')

            def callback(now, all, percentage, data):
                self.translate_process = (now, all, percentage, data)
                if self.cancel_flag:
                    raise Exception(f'\n\t   〈〈〈  Translation Canceled  〉〉〉')

            def translate(code):
                try:
                    self.translate_process = (0, 0, 0, ("", ""))
                    self.caption_t = Script.translate_async(script=self.caption, code=code, batch=read_batch(), callback=callback)
                    self.translated = True
                except:
                    self.translated = True

            def trace_translating():
                if self.translated:
                    if not self.cancel_flag:
                        self.text_box.setText(f'{self.caption_t}')
                        self.translate_btn.setText('Translate')
                        self.translate_btn.clicked.connect(self.translate_caption)
                        self.preview_lang = self.languages_list.currentItem().text().split(':')[0]
                        for w in [*self.batch_boxes, self.preview_btn, self.translate_btn, self.save_btn]:
                            w.setEnabled(True)
                    else:
                        self.text_box.setText(f'\n\t   〈〈〈  Translation Canceled  〉〉〉')
                        QTimer.singleShot(2000, lambda: (
                            self.text_box.setText(self.caption_f),
                            self.translate_btn.setText('Translate'),
                            [w.setEnabled(True) for w in [*self.batch_boxes, self.preview_btn, self.translate_btn, self.save_btn]],
                            self.translate_btn.clicked.connect(self.translate_caption),
                            ))
                else:
                    x, y, z, (a, b) = self.translate_process
                    lbl = '〈〈〈  Translating Captions  〉〉〉'
                    bar = "█" * int((z / 100) * 50) + "░" * (50 - int((z / 100) * 50))
                    pre, post = f'[{z:05.2f}%]', f'{x}/{y} Line{'s' if y != 1 else ''} Translated'
                    
                    self.text_box.setText(f'\n\t   {lbl}\n\n   {pre}   {bar}   {post}\n\n{a}\n{b}')
                    QTimer.singleShot(50, trace_translating)

            self.translated = False
            self.translate_process = (0, 0, 0, ("", ""))
            self.cancel_flag = False

            self.preview_btn.setDisabled(True)
            self.save_btn.setDisabled(True)
            self.translate_btn.setText('Cancel')
            self.translate_btn.clicked.connect(self.cancel_translation)

            code = self.languages_list.currentItem().text().split('`')[1].lower()
            Thread(target=lambda: translate(code=code), daemon=True).start()
            QTimer.singleShot(50, trace_translating)

        def cancel_translation(self):
            self.cancel_flag = True

        def save_captions(self):
            text = self.text_box.toPlainText()

            if not text.strip():
                return

            filepath, _ = QFileDialog.getSaveFileName(
                self,
                'Save Captions As',
                f'[Captions-{getattr(self, 'preview_lang', '')}]-{encode(self.title)}.srt',
                'SRT Files (*.srt);',
            )

            if filepath:
                if not filepath.lower().endswith('.srt'):
                    filepath += '.srt'

                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(text)
                except Exception as e:
                    window(
                        self,
                        title='Error',
                        icon='Error',
                        text='The video captions was not saved due to an error:',
                        info_text=f'\n{e}',
                    )

    return Window(url, title)


def window(
    parent=None,
    title: str = 'Message',
    size: tuple = (400, 200),
    icon: str | None = None,
    text: str = '',
    info_text: str | None = None,
    buttons: list[str] = ['ok'],
    default: str = 'ok',
    detailed_text: str | None = None
    ):

    win = QMessageBox(parent)
    win.setWindowTitle(title)
    win.setWindowIcon(setIcon())

    icon_map = {
        'info': QMessageBox.Icon.Information,
        'warn': QMessageBox.Icon.Warning,
        'critical': QMessageBox.Icon.Critical,
        'question': QMessageBox.Icon.Question,
    }
    if icon and icon.lower() in icon_map:
        win.setIcon(icon_map[icon.lower()])

    win.setText(text)
    if info_text:
        win.setInformativeText(info_text)
    if detailed_text:
        win.setDetailedText(detailed_text)

    btn_map = {
        'ok'    : QMessageBox.StandardButton.Ok,
        'yes'   : QMessageBox.StandardButton.Yes,
        'no'    : QMessageBox.StandardButton.No,
        'cancel': QMessageBox.StandardButton.Cancel,
    }

    flags = QMessageBox.StandardButton(0)
    for b in buttons:
        if b.lower() in btn_map:
            flags |= btn_map[b.lower()]

    if flags != 0:
        win.setStandardButtons(flags)

    if default.lower() in btn_map:
        win.setDefaultButton(btn_map[default.lower()])

    return win.exec()
