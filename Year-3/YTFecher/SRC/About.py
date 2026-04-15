from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

ID = u'com.ytfetcher.asem'
Version = '2.2.1'
Title = 'YTFetcher - YouTube Downloader'

Labels = ['YTFetcher - YouTube Downloader', f'Version: {Version}']

def about_window(parent, app_version=Version):
    dlg = QDialog(parent)
    dlg.setFixedSize(450, 560)
    dlg.setWindowTitle('About YTFetcher')
    dlg.setWindowModality(Qt.WindowModality.ApplicationModal)
    dlg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    dlg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

    box = QFrame()
    box.setObjectName('MainContainer')
    box.setFixedSize(400, 550)
    box.setStyleSheet('''
        #MainContainer {
            background-color: #101010;
            border-radius: 15px;
            border: 1px solid #303030;
        }
        #Header {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #AA0000, stop:1 #200000);
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
        }
        #Title {
            color: white;
            font-size: 28px;
            font-weight: 900;
        }
        #VersionBadge {
            background-color: rgba(0, 0, 0, 0.3);
            color: #ffcccc;
            border-radius: 10px;
            padding: 4px 10px;
            font-size: 11px;
        }
        #BodyText {
            color: #b3b3b3;
            font-size: 13px;
        }
        #DeveloperBox {
            background-color: #1a1a1a;
            border-radius: 12px;
            border: 1px solid #252525;
        }
        QPushButton#CloseBtn {
            background-color: #600000;
            color: white;
            border-radius: 10px;
            padding: 10px 40px;
            font-weight: bold;
        }
        QPushButton#CloseBtn:hover {
            background-color: #800000;
        }
    ''')

    glow = QGraphicsDropShadowEffect()
    glow.setBlurRadius(30)
    glow.setXOffset(0)
    glow.setYOffset(10)
    glow.setColor(QColor(0, 0, 0, 200))
    box.setGraphicsEffect(glow)

    root_layout = QVBoxLayout(box)
    root_layout.setContentsMargins(0, 0, 0, 25)
    root_layout.setSpacing(0)

    head = QFrame()
    head.setObjectName('Header')
    head.setFixedHeight(130)
    head_layout = QVBoxLayout(head)

    lbl_title = QLabel('YTFetcher')
    lbl_title.setObjectName('Title')
    lbl_ver = QLabel(f'Version: {app_version}')
    lbl_ver.setObjectName('VersionBadge')

    head_layout.addStretch()
    head_layout.addWidget(lbl_title, alignment=Qt.AlignmentFlag.AlignCenter)
    head_layout.addWidget(lbl_ver, alignment=Qt.AlignmentFlag.AlignCenter)
    head_layout.addStretch()

    body = QFrame()
    body_layout = QVBoxLayout(body)
    body_layout.setContentsMargins(25, 20, 25, 10)
    body_layout.setSpacing(15)

    txt_desc = QLabel('''
YTFetcher is a powerful YouTube downloader that gives full access to all video and audio streams, \
supports seamless merging, displays detailed video information, handles captions with translation, \
and enables complete playlist downloads with ease.'''[1:])
    
    txt_desc.setObjectName('BodyText')
    txt_desc.setWordWrap(True)
    txt_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

    dev_card = QFrame()
    dev_card.setObjectName('DeveloperBox')
    dev_card.setFixedHeight(180)

    dev_layout = QVBoxLayout(dev_card)
    dev_layout.setContentsMargins(20, 25, 20, 25)
    dev_layout.setSpacing(8)

    lbl_by = QLabel('Crafted By')
    lbl_by.setStyleSheet('color: #909090; font-size: 10px; font-weight: bold; letter-spacing: 3px;')
    lbl_by.setAlignment(Qt.AlignmentFlag.AlignCenter)

    lbl_name = QLabel('Asem Sharif')
    lbl_name.setStyleSheet('font-size: 30px; color: white; font-weight: bold;')
    lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

    lbl_role = QLabel('AI & CV Engineer | Desktop Developer')
    lbl_role.setStyleSheet('color: #909090; font-size: 12px;')
    lbl_role.setAlignment(Qt.AlignmentFlag.AlignCenter)

    links = QHBoxLayout()
    links.setContentsMargins(0, 15, 0, 15)
    links.setSpacing(10)

    def social_btn(text, url, color, extra=''):
        b = QPushButton(text)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setFixedSize(90, 32)
        b.setStyleSheet(f'''
            QPushButton {{
                background-color: #252525;
                color: {color};
                border: 1px solid #333;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color};
                color: white;
                border: 1px solid {color};
            }}
            {extra}
        ''')
        b.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
        return b

    links.addWidget(social_btn('Email', 'mailto:asem.sharif.ai@gmail.com', '#ff4D4D'))
    links.addWidget(social_btn('LinkedIn', 'https://linkedin.com/in/asem-sharif', '#0077B5'))
    links.addWidget(social_btn('Github', 'https://github.com/asem-sharif-ai', '#ffffff', r'QPushButton:hover {color: #000000;}'))

    dev_layout.addWidget(lbl_by)
    dev_layout.addWidget(lbl_name)
    dev_layout.addWidget(lbl_role)
    dev_layout.addStretch()
    dev_layout.addLayout(links)

    btn_close = QPushButton('Dismiss')
    btn_close.setObjectName('CloseBtn')
    btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
    btn_close.clicked.connect(dlg.close)

    root_layout.addWidget(head)
    root_layout.addWidget(body)
    body_layout.addWidget(txt_desc)
    body_layout.addSpacing(10)
    body_layout.addWidget(dev_card)
    body_layout.addSpacing(20)
    body_layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignCenter)

    dlg_layout = QVBoxLayout(dlg)
    dlg_layout.setContentsMargins(0, 0, 0, 0)
    dlg_layout.addWidget(box, alignment=Qt.AlignmentFlag.AlignCenter)

    dlg.exec()
