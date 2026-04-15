
from SRC import *

def set_id(id:str):
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(id)
    except:
        pass

def setIcon(relative:str=r'Icon.ico') -> str:
    if hasattr(sys, '_MEIPASS'):
        return QIcon(os.path.join(sys._MEIPASS, relative))
    return QIcon(os.path.join(os.path.abspath('.'), relative))

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.build()
        self.showMaximized()

    def build(self):
        self.setWindowTitle(f'{Title}')
        self.setWindowIcon(setIcon())
        self.setGeometry(200, 200, 950, 650)
        self.setMinimumSize(950, 650)

    #! ----- ----- Menu Bar / Actions ----- ----- ----- ----- ----- ----- ----- -----
    
        self.actions = [
            QAction('Set Downloads Directory', self),
            QAction('View Downloads', self),
            QAction('Updates', self),
            QAction('About', self),
            QAction('Restart', self),
            QAction('Exit', self),
        ]

        functions = [
            self.set_downloads_path,
            self.view_downloads,
            self.check_updates,
            lambda: about_window(self),
            self.restart,
            lambda: QApplication.quit()
            ]
        
        for act, fn in zip(self.actions, functions):
            act.triggered.connect(fn)

        self.menuBar().addActions(self.actions)
        self.actions[2].setEnabled(False)
    
    #! ----- ----- Status Bar ----- ----- ----- ----- ----- ----- ----- -----

        for label in Labels:
            label = QLabel(label)
            label.setContentsMargins(15, 2, 15, 2)
            self.statusBar().addPermanentWidget(label)

        self.connection = QLabel()
        self.connection.setContentsMargins(10, 2, 10, 2)
        self.statusBar().addPermanentWidget(self.connection)
        
        self.check_connection()

    #! ----- ----- Central Widget ----- ----- ----- ----- ----- ----- ----- -----

        self.setCentralWidget(QWidget())
    
        self.tabs = Tabs(self.path)
        self.grid = QGridLayout(self.centralWidget())
        self.grid.setContentsMargins(10, 5, 10, 5)
        self.grid.addWidget(self.tabs)

        self.set_downloads_path('.')

    def check_connection(self, delay_ms=3000):
        def colorize(icon: QIcon, color: str, size: int) -> QPixmap:
            pix = icon.pixmap(size, size)
            colored = QPixmap(pix.size())
            colored.fill(Qt.GlobalColor.transparent)

            painter = QPainter(colored)
            painter.drawPixmap(0, 0, pix)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(colored.rect(), QColor(color))
            painter.end()

            return colored

        try:
            socket.create_connection(('8.8.8.8', 53), timeout=2)
        except OSError:
            icon = QIcon.fromTheme('network-offline')
            self.connection.setPixmap(colorize(icon, '#AA0000', 18))
            self.connection.setToolTip('No Internet')
        else:
            icon = QIcon.fromTheme('network-wireless')
            self.connection.setPixmap(colorize(icon, '#00AA00', 18))
            self.connection.setToolTip('Connected')
        finally:
            QTimer.singleShot(delay_ms, self.check_connection)

    def set_downloads_path(self, folder=None):
        DownloadFolder = 'Downloads_YTF'
        BaseDirectory  = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
        
        if not folder:
            folder = QFileDialog.getExistingDirectory(
                parent=self,
                caption='Select Downloads Folder',
                directory=str(BaseDirectory.resolve())
            )

        ytf_folder = Path(folder) / DownloadFolder if folder else BaseDirectory / DownloadFolder
        ytf_folder.mkdir(parents=True, exist_ok=True)
        
        self.download_path = ytf_folder.resolve()
        self.statusBar().showMessage(f'  Download Path: `{self.download_path}`.', 5000)


    def view_downloads(self):
        folder = Path(self.download_path)
        folder.mkdir(parents=True, exist_ok=True)
        try:
            if sys.platform == 'win32':
                subprocess.run(f'explorer "{folder}"')
            elif sys.platform == 'darwin':
                subprocess.run(['open', folder])
            else: # Linux / Unix
                subprocess.run(['xdg-open', folder])
        except Exception as e:
            window(
                self,
                title='Could Not Open Folder',
                icon='warn',
                text='Could not open the downloads folder due to an error:',
                info_text=f'{e}',
                detailed_text=f'Current Download Path:\n{folder}',
            )

    def check_updates(self):
        ...

    def restart(self):
        def rebuild():
            self.build()
            self.showMaximized()

        if self.can_exit():
            self.hide()
            self.menuBar().deleteLater()
            self.statusBar().deleteLater()
            self.centralWidget().deleteLater()
            QTimer.singleShot(50, rebuild)

    def can_exit(self) -> bool:
        process = []
        for i in range(self.tabs.count()-1):
            tab = self.tabs.widget(i)
            if tab.has_process:
                process.append(tab.sum_process)

        if len(process) != 0:
            win = window(
                self,
                title='Taps In Process',
                icon='question',
                text=f'{len(process)} Taps has a total of {sum(process)} streams that have not been saved.',
                info_text='Are you sure you want to exit?',
                buttons=['yes', 'no'],
                default='yes'
            )
            if win != QMessageBox.StandardButton.Yes:
                return False

        return True

    def closeEvent(self, event):
        if self.can_exit():
            event.accept()
        else:
            event.ignore()

    def path(self):
        return self.download_path

    @staticmethod
    def start():
        set_id(ID)

        app = QApplication(sys.argv)
        app.setWindowIcon(setIcon())
        app.setStyleSheet(styleApp())
        
        App()
        sys.exit(app.exec())
