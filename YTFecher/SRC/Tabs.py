
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from SRC.Tab import Tab, window

class Tabs(QTabWidget):
    def __init__(self, path:callable):
        super().__init__()
        self.path = path
        
        self.addTab(Tab(path, 0, self.open_in_new_tab, None), 'Tab 1'.center(15))
        self.addTab(QWidget(), ' 🞤 ')

        self.tabBarClicked.connect(self.add_tab)
        self.index, self.max = 1, 10

        self.activate()
        
        self.timer = QTimer(self)
        self.timer.setInterval(250)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.activate)

    def activate(self):
        if self.count() <= self.max:
            self.setTabEnabled(self.count() - 1, True)
            self.ready = True

    def deactivate(self):
        self.setTabEnabled(self.count() - 1, False)
        self.ready = True

    def add_tab(self, index:int):
        if index == self.count() - 1 and self.ready:
            self.deactivate()
            self.timer.start()

            self.index += 1
            self.insertTab(self.count() - 1, Tab(self.path, index, self.open_in_new_tab, self.del_tab), f'Tab {self.index}'.center(15))
            self.setCurrentIndex(self.count() - 2)

    def del_tab(self, index:int):
        def del_tab(index):
            self.removeTab(min(self.count() - 2, index))
            self.setCurrentIndex(min(self.count() - 2, index - 1))

            self.index = 0
            for i in range(self.count() - 1):
                self.setTabText(i, f'Tab {i+1}'.center(15))
                self.index += 1

        if self.ready:
            self.deactivate()
            self.timer.start()

            tab = self.widget(min(self.count() - 2, index))
            if tab.has_process:
                win = window(
                    self,
                    title='Confirm Deleting Tab',
                    icon='warn',
                    text=f'This tab contains {tab.sum_process} fetched video(s).\nAre you sure you want to continue?',
                    info_text=f'If you delete it, the content will be permanently removed and cannot be restored unless you fetch it again.',
                    buttons=['ok', 'cancel'],
                    default='no'
                )
                if win == QMessageBox.StandardButton.Ok:
                    del_tab(index)
            else:
                del_tab(index)

    def open_in_new_tab(self, url:str):
        if self.count() <= self.max:
            self.add_tab(self.index)
            self.widget(self.index-1).input_line.setText(url)
            QTimer.singleShot(1000, lambda: self.widget(self.index-1).fetch(url))
        else:
            window(
                self,
                title='Could Not Open New Tab',
                icon='critical',
                text=f'Can not add more than `{self.max}` tabs, try to delete unused ones.',

            )
