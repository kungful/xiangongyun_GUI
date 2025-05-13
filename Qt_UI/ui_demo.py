# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'demo.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialogButtonBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpinBox,
    QStackedWidget, QStatusBar, QTabWidget, QTextBrowser,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(850, 643)
        MainWindow.setMinimumSize(QSize(0, 30))
        MainWindow.setStyleSheet(u"/* \u4e3b\u7a97\u53e3\uff08QMainWindow\uff09\u7684\u8fb9\u6846\u6837\u5f0f */\n"
"QMainWindow {\n"
"    background-color: #1f232a;  /* \u7a97\u53e3\u80cc\u666f\u8272 */\n"
"    border: 2px solid #3e434c;  /* \u81ea\u5b9a\u4e49\u8fb9\u6846 */\n"
"    border-radius: 8px;         /* \u5706\u89d2\uff08\u53ef\u9009\uff09 */\n"
"    padding: 0;                 /* \u9632\u6b62\u5185\u90e8\u5143\u7d20\u5f71\u54cd\u8fb9\u6846 */\n"
"    margin: 0;\n"
"}\n"
"\n"
"/* \u901a\u7528\u6837\u5f0f\uff08\u5982\u4f60\u7684\u539f\u59cb\u4ee3\u7801\uff09 */\n"
"* {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    background: none;\n"
"    padding: 0;\n"
"    margin: 0;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"/* \u4e2d\u592e\u90e8\u4ef6 */\n"
"#centralwidget {\n"
"    background-color: #1f232a;\n"
"    border-radius: 6px;  /* \u5982\u679c\u4e3b\u7a97\u53e3\u6709\u5706\u89d2\uff0c\u8fd9\u91cc\u53ef\u4ee5\u5c0f\u4e00\u70b9 */\n"
"}\n"
"\n"
"/* \u5de6\u4fa7\u9762\u677f */\n"
"#left {\n"
"    background-color: #42424"
                        "2;\n"
"    border-right: 1px solid #3e434c;  /* \u53f3\u4fa7\u5206\u9694\u7ebf */\n"
"}\n"
"\n"
"/* \u6309\u94ae\u6837\u5f0f */\n"
"QPushButton {\n"
"    text-align: left;\n"
"    padding: 2px 2px;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.left = QWidget(self.centralwidget)
        self.left.setObjectName(u"left")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left.sizePolicy().hasHeightForWidth())
        self.left.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.left)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.left)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.menubtn = QPushButton(self.frame)
        self.menubtn.setObjectName(u"menubtn")
        self.menubtn.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/ico/ico/align-center.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.menubtn.setIcon(icon)
        self.menubtn.setIconSize(QSize(24, 24))

        self.horizontalLayout_2.addWidget(self.menubtn)


        self.verticalLayout_2.addWidget(self.frame, 0, Qt.AlignmentFlag.AlignTop)

        self.frame_2 = QFrame(self.left)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setMidLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.home = QPushButton(self.frame_2)
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/ico/ico/home.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.home.setIcon(icon1)
        self.home.setIconSize(QSize(24, 24))

        self.verticalLayout_3.addWidget(self.home)

        self.shiliBt = QPushButton(self.frame_2)
        self.shiliBt.setObjectName(u"shiliBt")
        self.shiliBt.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/ico/ico/package.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.shiliBt.setIcon(icon2)
        self.shiliBt.setIconSize(QSize(24, 24))

        self.verticalLayout_3.addWidget(self.shiliBt)

        self.jingxiang = QPushButton(self.frame_2)
        self.jingxiang.setObjectName(u"jingxiang")
        self.jingxiang.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/ico/ico/align-justify.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.jingxiang.setIcon(icon3)
        self.jingxiang.setIconSize(QSize(24, 24))

        self.verticalLayout_3.addWidget(self.jingxiang)

        self.jingxiang_2 = QPushButton(self.frame_2)
        self.jingxiang_2.setObjectName(u"jingxiang_2")
        self.jingxiang_2.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        self.jingxiang_2.setIcon(icon3)
        self.jingxiang_2.setIconSize(QSize(24, 24))

        self.verticalLayout_3.addWidget(self.jingxiang_2)


        self.verticalLayout_2.addWidget(self.frame_2, 0, Qt.AlignmentFlag.AlignTop)

        self.frame_4 = QFrame(self.left)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.comfyui = QPushButton(self.frame_4)
        self.comfyui.setObjectName(u"comfyui")
        self.comfyui.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/ico/ico/git-branch.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.comfyui.setIcon(icon4)
        self.comfyui.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.comfyui)

        self.fengzhuang = QPushButton(self.frame_4)
        self.fengzhuang.setObjectName(u"fengzhuang")
        self.fengzhuang.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/ico/ico/box.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fengzhuang.setIcon(icon5)
        self.fengzhuang.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.fengzhuang)

        self.fluxgym = QPushButton(self.frame_4)
        self.fluxgym.setObjectName(u"fluxgym")
        self.fluxgym.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon6 = QIcon()
        icon6.addFile(u":/ico/ico/coffee.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.fluxgym.setIcon(icon6)
        self.fluxgym.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.fluxgym)

        self.shuchu = QPushButton(self.frame_4)
        self.shuchu.setObjectName(u"shuchu")
        self.shuchu.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u":/ico/ico/file-text.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.shuchu.setIcon(icon7)
        self.shuchu.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.shuchu)

        self.quanbu = QPushButton(self.frame_4)
        self.quanbu.setObjectName(u"quanbu")
        self.quanbu.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u":/ico/ico/folder.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.quanbu.setIcon(icon8)
        self.quanbu.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.quanbu)

        self.quanbu_2 = QPushButton(self.frame_4)
        self.quanbu_2.setObjectName(u"quanbu_2")
        self.quanbu_2.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon9 = QIcon()
        icon9.addFile(u":/ico/ico/globe.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.quanbu_2.setIcon(icon9)
        self.quanbu_2.setIconSize(QSize(24, 24))

        self.verticalLayout_5.addWidget(self.quanbu_2)


        self.verticalLayout_2.addWidget(self.frame_4, 0, Qt.AlignmentFlag.AlignHCenter)

        self.frame_3 = QFrame(self.left)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.settings = QPushButton(self.frame_3)
        self.settings.setObjectName(u"settings")
        self.settings.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon10 = QIcon()
        icon10.addFile(u":/ico/ico/settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings.setIcon(icon10)
        self.settings.setIconSize(QSize(24, 24))

        self.verticalLayout_4.addWidget(self.settings)

        self.info = QPushButton(self.frame_3)
        self.info.setObjectName(u"info")
        self.info.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon11 = QIcon()
        icon11.addFile(u":/ico/ico/info.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.info.setIcon(icon11)
        self.info.setIconSize(QSize(24, 24))

        self.verticalLayout_4.addWidget(self.info)

        self.help = QPushButton(self.frame_3)
        self.help.setObjectName(u"help")
        self.help.setStyleSheet(u"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"    border-radius: 10px;\n"
"}")
        icon12 = QIcon()
        icon12.addFile(u":/ico/ico/help-circle.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.help.setIcon(icon12)
        self.help.setIconSize(QSize(24, 24))

        self.verticalLayout_4.addWidget(self.help)


        self.verticalLayout_2.addWidget(self.frame_3, 0, Qt.AlignmentFlag.AlignBottom)


        self.horizontalLayout.addWidget(self.left)

        self.body = QStackedWidget(self.centralwidget)
        self.body.setObjectName(u"body")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.body.sizePolicy().hasHeightForWidth())
        self.body.setSizePolicy(sizePolicy2)
        self.body.setStyleSheet(u"")
        self.zhuye_page1 = QWidget()
        self.zhuye_page1.setObjectName(u"zhuye_page1")
        self.verticalLayout = QVBoxLayout(self.zhuye_page1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_13 = QFrame(self.zhuye_page1)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_13)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.textBrowser = QTextBrowser(self.frame_13)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setStyleSheet(u"QFrame {\n"
"    background-color: transparent;\n"
"    border-radius: 10px;\n"
"}")

        self.verticalLayout_9.addWidget(self.textBrowser)


        self.verticalLayout.addWidget(self.frame_13, 0, Qt.AlignmentFlag.AlignTop)

        self.shouye = QFrame(self.zhuye_page1)
        self.shouye.setObjectName(u"shouye")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.shouye.sizePolicy().hasHeightForWidth())
        self.shouye.setSizePolicy(sizePolicy3)
        self.shouye.setMinimumSize(QSize(0, 0))
        self.shouye.setSizeIncrement(QSize(0, 0))
        self.shouye.setBaseSize(QSize(0, 0))
        self.shouye.setStyleSheet(u"QFrame {\n"
"    background-color: #1b1b1b;\n"
"    border-radius: 10px;\n"
"}")
        self.shouye.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        self.shouye.setFrameShape(QFrame.Shape.StyledPanel)
        self.shouye.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.shouye)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tishi = QLabel(self.shouye)
        self.tishi.setObjectName(u"tishi")

        self.verticalLayout_6.addWidget(self.tishi)

        self.lingpai = QLineEdit(self.shouye)
        self.lingpai.setObjectName(u"lingpai")
        self.lingpai.setMinimumSize(QSize(0, 30))
        self.lingpai.setToolTipDuration(-1)
        self.lingpai.setStyleSheet(u"background-color: #363636;")

        self.verticalLayout_6.addWidget(self.lingpai)

        self.frame_14 = QFrame(self.shouye)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setStyleSheet(u"QPushButton {\n"
"    background-color: #CC9933;\n"
"    border-radius: 10px;\n"
"    font: 10pt \"\u5b8b\u4f53\";\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_16 = QPushButton(self.frame_14)
        self.pushButton_16.setObjectName(u"pushButton_16")
        self.pushButton_16.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_6.addWidget(self.pushButton_16, 0, Qt.AlignmentFlag.AlignLeft)

        self.radioButton = QRadioButton(self.frame_14)
        self.radioButton.setObjectName(u"radioButton")

        self.horizontalLayout_6.addWidget(self.radioButton, 0, Qt.AlignmentFlag.AlignRight)

        self.pushButton_15 = QPushButton(self.frame_14)
        self.pushButton_15.setObjectName(u"pushButton_15")
        self.pushButton_15.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_6.addWidget(self.pushButton_15, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_6.addWidget(self.frame_14)

        self.huoqu = QPushButton(self.shouye)
        self.huoqu.setObjectName(u"huoqu")
        self.huoqu.setStyleSheet(u"QPushButton {\n"
"    background-color: #0088ff;\n"
"    border-radius: 10px;\n"
"    font: 24pt \"\u5b8b\u4f53\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        icon13 = QIcon()
        icon13.addFile(u":/ico/ico/anchor.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.huoqu.setIcon(icon13)
        self.huoqu.setIconSize(QSize(64, 64))

        self.verticalLayout_6.addWidget(self.huoqu)

        self.zhuce = QPushButton(self.shouye)
        self.zhuce.setObjectName(u"zhuce")
        self.zhuce.setStyleSheet(u"QPushButton {\n"
"    background-color: #66CC00;\n"
"    border-radius: 10px;\n"
"    font: 24pt \"\u5b8b\u4f53\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        icon14 = QIcon()
        icon14.addFile(u":/ico/ico/user-plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zhuce.setIcon(icon14)
        self.zhuce.setIconSize(QSize(64, 64))

        self.verticalLayout_6.addWidget(self.zhuce)


        self.verticalLayout.addWidget(self.shouye, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)

        self.coffeekuang = QFrame(self.zhuye_page1)
        self.coffeekuang.setObjectName(u"coffeekuang")
        self.coffeekuang.setFrameShape(QFrame.Shape.StyledPanel)
        self.coffeekuang.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.coffeekuang)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.coffee = QPushButton(self.coffeekuang)
        self.coffee.setObjectName(u"coffee")
        self.coffee.setStyleSheet(u"QPushButton {\n"
"    background-color: #282828;\n"
"    border-radius: 10px;\n"
"    font: 8pt \"\u5b8b\u4f53\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        icon15 = QIcon()
        icon15.addFile(u":/ico/ico/gift.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.coffee.setIcon(icon15)
        self.coffee.setIconSize(QSize(32, 32))

        self.verticalLayout_7.addWidget(self.coffee)


        self.verticalLayout.addWidget(self.coffeekuang, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)

        self.body.addWidget(self.zhuye_page1)
        self.shezhi_page2 = QWidget()
        self.shezhi_page2.setObjectName(u"shezhi_page2")
        self.shezhi_page2.setStyleSheet(u"")
        self.verticalLayout_8 = QVBoxLayout(self.shezhi_page2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.frame_15 = QFrame(self.shezhi_page2)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setStyleSheet(u"QFrame {\n"
"    background-color: #2F4F4F;\n"
"    border-radius: 10px;\n"
"}")
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.frame_15)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_7.addWidget(self.label_6)

        self.dailikuang_2 = QLineEdit(self.frame_15)
        self.dailikuang_2.setObjectName(u"dailikuang_2")
        self.dailikuang_2.setMinimumSize(QSize(0, 30))
        self.dailikuang_2.setStyleSheet(u"    background-color: #363636;")

        self.horizontalLayout_7.addWidget(self.dailikuang_2)

        self.dailiBt_2 = QDialogButtonBox(self.frame_15)
        self.dailiBt_2.setObjectName(u"dailiBt_2")
        self.dailiBt_2.setStyleSheet(u"QPushButton {\n"
"    background-color: #CC9933;\n"
"    border-radius: 10px;\n"
"    font: 16pt \"\u5b8b\u4f53\";\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.dailiBt_2.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_7.addWidget(self.dailiBt_2)


        self.verticalLayout_8.addWidget(self.frame_15)

        self.frame_16 = QFrame(self.shezhi_page2)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setStyleSheet(u"QFrame {\n"
"    background-color: #2F4F4F;\n"
"    border-radius: 10px;\n"
"}")
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_7 = QLabel(self.frame_16)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_8.addWidget(self.label_7)

        self.dailikuang_3 = QLineEdit(self.frame_16)
        self.dailikuang_3.setObjectName(u"dailikuang_3")
        self.dailikuang_3.setMinimumSize(QSize(0, 30))
        self.dailikuang_3.setStyleSheet(u"    background-color: #363636;")

        self.horizontalLayout_8.addWidget(self.dailikuang_3)

        self.dailiBt_3 = QDialogButtonBox(self.frame_16)
        self.dailiBt_3.setObjectName(u"dailiBt_3")
        self.dailiBt_3.setStyleSheet(u"QPushButton {\n"
"    background-color: #CC9933;\n"
"    border-radius: 10px;\n"
"    font: 16pt \"\u5b8b\u4f53\";\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.dailiBt_3.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_8.addWidget(self.dailiBt_3)


        self.verticalLayout_8.addWidget(self.frame_16)

        self.frame_17 = QFrame(self.shezhi_page2)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setStyleSheet(u"QFrame {\n"
"    background-color: #2F4F4F;\n"
"    border-radius: 10px;\n"
"}")
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_8 = QLabel(self.frame_17)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_9.addWidget(self.label_8)

        self.dailikuang_4 = QLineEdit(self.frame_17)
        self.dailikuang_4.setObjectName(u"dailikuang_4")
        self.dailikuang_4.setMinimumSize(QSize(0, 30))
        self.dailikuang_4.setStyleSheet(u"background-color: #363636;")

        self.horizontalLayout_9.addWidget(self.dailikuang_4)

        self.dailiBt_4 = QDialogButtonBox(self.frame_17)
        self.dailiBt_4.setObjectName(u"dailiBt_4")
        self.dailiBt_4.setStyleSheet(u"QPushButton {\n"
"    background-color: #CC9933;\n"
"    border-radius: 10px;\n"
"    font: 16pt \"\u5b8b\u4f53\";\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.dailiBt_4.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_9.addWidget(self.dailiBt_4)


        self.verticalLayout_8.addWidget(self.frame_17)

        self.frame_19 = QFrame(self.shezhi_page2)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setStyleSheet(u"QFrame {\n"
"    background-color: #2F4F4F;\n"
"    border-radius: 10px;\n"
"}")
        self.frame_19.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_10 = QLabel(self.frame_19)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_11.addWidget(self.label_10)

        self.dailikuang_6 = QLineEdit(self.frame_19)
        self.dailikuang_6.setObjectName(u"dailikuang_6")
        self.dailikuang_6.setMinimumSize(QSize(0, 30))
        self.dailikuang_6.setStyleSheet(u"background-color: #363636;")

        self.horizontalLayout_11.addWidget(self.dailikuang_6)

        self.dailiBt_6 = QDialogButtonBox(self.frame_19)
        self.dailiBt_6.setObjectName(u"dailiBt_6")
        self.dailiBt_6.setStyleSheet(u"QPushButton {\n"
"    background-color: #CC9933;\n"
"    border-radius: 10px;\n"
"    font: 16pt \"\u5b8b\u4f53\";\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.dailiBt_6.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_11.addWidget(self.dailiBt_6)


        self.verticalLayout_8.addWidget(self.frame_19)

        self.frame_18 = QFrame(self.shezhi_page2)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setStyleSheet(u"QFrame {\n"
"    background-color: #2F4F4F;\n"
"    border-radius: 10px;\n"
"}")
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_9 = QLabel(self.frame_18)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"font: 12pt \"Microsoft YaHei UI\";")

        self.horizontalLayout_10.addWidget(self.label_9)

        self.dailikuang_5 = QLineEdit(self.frame_18)
        self.dailikuang_5.setObjectName(u"dailikuang_5")
        self.dailikuang_5.setMinimumSize(QSize(0, 30))
        self.dailikuang_5.setStyleSheet(u"background-color: #363636;")

        self.horizontalLayout_10.addWidget(self.dailikuang_5)

        self.dailiBt_5 = QDialogButtonBox(self.frame_18)
        self.dailiBt_5.setObjectName(u"dailiBt_5")
        self.dailiBt_5.setStyleSheet(u"QPushButton {\n"
"    background-color: #CC9933;\n"
"    border-radius: 10px;\n"
"    font: 16pt \"\u5b8b\u4f53\";\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.dailiBt_5.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.horizontalLayout_10.addWidget(self.dailiBt_5)


        self.verticalLayout_8.addWidget(self.frame_18)

        self.body.addWidget(self.shezhi_page2)
        self.xinxi_page3 = QWidget()
        self.xinxi_page3.setObjectName(u"xinxi_page3")
        self.verticalLayout_10 = QVBoxLayout(self.xinxi_page3)
        self.verticalLayout_10.setSpacing(10)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(10, 10, 10, 10)
        self.textBrowser1 = QTextBrowser(self.xinxi_page3)
        self.textBrowser1.setObjectName(u"textBrowser1")
        self.textBrowser1.setStyleSheet(u"background-color: #2d3848;\n"
"    border-radius: 10px;")

        self.verticalLayout_10.addWidget(self.textBrowser1)

        self.textBrowser2 = QTextBrowser(self.xinxi_page3)
        self.textBrowser2.setObjectName(u"textBrowser2")
        self.textBrowser2.setStyleSheet(u"background-color: #2d3848;\n"
"    border-radius: 10px;")

        self.verticalLayout_10.addWidget(self.textBrowser2)

        self.body.addWidget(self.xinxi_page3)
        self.bangzhu_page4 = QWidget()
        self.bangzhu_page4.setObjectName(u"bangzhu_page4")
        self.bangzhu_page4.setStyleSheet(u"    background-color: #6c6c6c;")
        self.verticalLayout_81 = QVBoxLayout(self.bangzhu_page4)
        self.verticalLayout_81.setObjectName(u"verticalLayout_81")
        self.frame_21 = QFrame(self.bangzhu_page4)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setStyleSheet(u"")
        self.frame_21.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_21 = QVBoxLayout(self.frame_21)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.textBrowser_2 = QTextBrowser(self.frame_21)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setStyleSheet(u"background-color: #363636;")

        self.verticalLayout_21.addWidget(self.textBrowser_2)


        self.verticalLayout_81.addWidget(self.frame_21)

        self.body.addWidget(self.bangzhu_page4)
        self.zhanghao_page5 = QWidget()
        self.zhanghao_page5.setObjectName(u"zhanghao_page5")
        self.zhanghao_page5.setStyleSheet(u"")
        self.verticalLayout_82 = QVBoxLayout(self.zhanghao_page5)
        self.verticalLayout_82.setObjectName(u"verticalLayout_82")
        self.zhanghaoapi = QFrame(self.zhanghao_page5)
        self.zhanghaoapi.setObjectName(u"zhanghaoapi")
        sizePolicy3.setHeightForWidth(self.zhanghaoapi.sizePolicy().hasHeightForWidth())
        self.zhanghaoapi.setSizePolicy(sizePolicy3)
        self.zhanghaoapi.setMinimumSize(QSize(0, 0))
        self.zhanghaoapi.setMaximumSize(QSize(16777215, 160))
        self.zhanghaoapi.setStyleSheet(u"QFrame {\n"
"    background-color: #3d5843 ;\n"
"    border-radius: 10px;\n"
"}")
        self.zhanghaoapi.setFrameShape(QFrame.Shape.StyledPanel)
        self.zhanghaoapi.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.zhanghaoapi)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label = QLabel(self.zhanghaoapi)
        self.label.setObjectName(u"label")

        self.verticalLayout_11.addWidget(self.label, 0, Qt.AlignmentFlag.AlignTop)

        self.listWidget = QListWidget(self.zhanghaoapi)
        font = QFont()
        font.setPointSize(12)
        __qlistwidgetitem = QListWidgetItem(self.listWidget)
        __qlistwidgetitem.setFont(font);
        __qlistwidgetitem1 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem1.setFont(font);
        __qlistwidgetitem2 = QListWidgetItem(self.listWidget)
        __qlistwidgetitem2.setFont(font);
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy4)
        self.listWidget.setMinimumSize(QSize(0, 0))

        self.verticalLayout_11.addWidget(self.listWidget, 0, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_82.addWidget(self.zhanghaoapi, 0, Qt.AlignmentFlag.AlignTop)

        self.frame_5 = QFrame(self.zhanghao_page5)
        self.frame_5.setObjectName(u"frame_5")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(10)
        sizePolicy5.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy5)
        self.frame_5.setMinimumSize(QSize(0, 0))
        self.frame_5.setMaximumSize(QSize(16777215, 100))
        self.frame_5.setStyleSheet(u"QFrame {\n"
"    background-color: #3d5843 ;\n"
"    border-radius: 10px;\n"
"}")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_5)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_12.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignTop)

        self.listWidget_2 = QListWidget(self.frame_5)
        __qlistwidgetitem3 = QListWidgetItem(self.listWidget_2)
        __qlistwidgetitem3.setFont(font);
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setMinimumSize(QSize(0, 0))

        self.verticalLayout_12.addWidget(self.listWidget_2, 0, Qt.AlignmentFlag.AlignTop)

        self.pushButton_3 = QPushButton(self.frame_5)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"    background-color: #CCCC33;\n"
"    border-radius: 10px;\n"
"    font: 16pt \"\u5b8b\u4f53\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")

        self.verticalLayout_12.addWidget(self.pushButton_3, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_82.addWidget(self.frame_5)

        self.zhifufangshi = QFrame(self.zhanghao_page5)
        self.zhifufangshi.setObjectName(u"zhifufangshi")
        self.zhifufangshi.setStyleSheet(u"QFrame {\n"
"    background-color: #3d5843 ;\n"
"    border-radius: 10px;\n"
"}")
        self.zhifufangshi.setFrameShape(QFrame.Shape.StyledPanel)
        self.zhifufangshi.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.zhifufangshi)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.label_3 = QLabel(self.zhifufangshi)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_13.addWidget(self.label_3, 0, Qt.AlignmentFlag.AlignTop)

        self.comboBox = QComboBox(self.zhifufangshi)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(146, 30))
        self.comboBox.setStyleSheet(u"background-color: #363636;")

        self.verticalLayout_13.addWidget(self.comboBox, 0, Qt.AlignmentFlag.AlignRight)

        self.spinBox = QSpinBox(self.zhifufangshi)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimumSize(QSize(160, 26))
        self.spinBox.setStyleSheet(u"background-color: #363636;")

        self.verticalLayout_13.addWidget(self.spinBox, 0, Qt.AlignmentFlag.AlignRight)

        self.frame_6 = QFrame(self.zhifufangshi)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setStyleSheet(u"QPushButton {\n"
"    background-color: #CCCC33;\n"
"    border-radius: 10px;\n"
"    font: 24pt \"\u5b8b\u4f53\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_2 = QPushButton(self.frame_6)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    background-color: #CCCC33;\n"
"    border-radius: 10px;\n"
"    font: 20pt \"\u5b8b\u4f53\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.verticalLayout_13.addWidget(self.frame_6, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_82.addWidget(self.zhifufangshi)

        self.frame_7 = QFrame(self.zhanghao_page5)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setStyleSheet(u"QFrame {\n"
"    background-color: #3d5843 ;\n"
"    border-radius: 10px;\n"
"}")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_7)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_4 = QLabel(self.frame_7)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_14.addWidget(self.label_4, 0, Qt.AlignmentFlag.AlignTop)

        self.listWidget_4 = QListWidget(self.frame_7)
        self.listWidget_4.setObjectName(u"listWidget_4")

        self.verticalLayout_14.addWidget(self.listWidget_4)

        self.pushButton_4 = QPushButton(self.frame_7)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setStyleSheet(u"QPushButton {\n"
"    background-color: #CCCC33;\n"
"    border-radius: 10px;\n"
"    font: 16pt \"\u5b8b\u4f53\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")

        self.verticalLayout_14.addWidget(self.pushButton_4)


        self.verticalLayout_82.addWidget(self.frame_7)

        self.body.addWidget(self.zhanghao_page5)
        self.shili_page6 = QWidget()
        self.shili_page6.setObjectName(u"shili_page6")
        self.shili_page6.setStyleSheet(u"")
        self.verticalLayout_83 = QVBoxLayout(self.shili_page6)
        self.verticalLayout_83.setObjectName(u"verticalLayout_83")
        self.scrollArea = QScrollArea(self.shili_page6)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 693, 181))
        self.scrollAreaWidgetContents.setAutoFillBackground(False)
        self.verticalLayout_17 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.frame_9 = QFrame(self.scrollAreaWidgetContents)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_9)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.tabWidget = QTabWidget(self.frame_9)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"background-color: #363636;")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_19 = QVBoxLayout(self.tab)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.listWidget_5 = QListWidget(self.tab)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        QListWidgetItem(self.listWidget_5)
        self.listWidget_5.setObjectName(u"listWidget_5")
        self.listWidget_5.setStyleSheet(u"background-color: #363636;")

        self.verticalLayout_19.addWidget(self.listWidget_5)

        self.frame_11 = QFrame(self.tab)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setStyleSheet(u"QPushButton {\n"
"    background-color: #CC9933;\n"
"    border-radius: 10px;\n"
"    font: 10pt \"\u5b8b\u4f53\";\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_5 = QPushButton(self.frame_11)
        self.pushButton_5.setObjectName(u"pushButton_5")
        icon16 = QIcon()
        icon16.addFile(u":/ico/ico/skip-forward.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_5.setIcon(icon16)

        self.horizontalLayout_4.addWidget(self.pushButton_5)

        self.pushButton_7 = QPushButton(self.frame_11)
        self.pushButton_7.setObjectName(u"pushButton_7")
        icon17 = QIcon()
        icon17.addFile(u":/ico/ico/arrow-down.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_7.setIcon(icon17)

        self.horizontalLayout_4.addWidget(self.pushButton_7)

        self.pushButton_10 = QPushButton(self.frame_11)
        self.pushButton_10.setObjectName(u"pushButton_10")
        icon18 = QIcon()
        icon18.addFile(u":/ico/ico/phone-missed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_10.setIcon(icon18)

        self.horizontalLayout_4.addWidget(self.pushButton_10)

        self.pushButton_9 = QPushButton(self.frame_11)
        self.pushButton_9.setObjectName(u"pushButton_9")
        icon19 = QIcon()
        icon19.addFile(u":/ico/ico/phone-off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_9.setIcon(icon19)

        self.horizontalLayout_4.addWidget(self.pushButton_9)

        self.pushButton_8 = QPushButton(self.frame_11)
        self.pushButton_8.setObjectName(u"pushButton_8")
        icon20 = QIcon()
        icon20.addFile(u":/ico/ico/x.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_8.setIcon(icon20)

        self.horizontalLayout_4.addWidget(self.pushButton_8)

        self.pushButton_13 = QPushButton(self.frame_11)
        self.pushButton_13.setObjectName(u"pushButton_13")
        icon21 = QIcon()
        icon21.addFile(u":/ico/ico/arrow-down-circle.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_13.setIcon(icon21)

        self.horizontalLayout_4.addWidget(self.pushButton_13)

        self.pushButton_11 = QPushButton(self.frame_11)
        self.pushButton_11.setObjectName(u"pushButton_11")
        icon22 = QIcon()
        icon22.addFile(u":/ico/ico/zap-off.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_11.setIcon(icon22)

        self.horizontalLayout_4.addWidget(self.pushButton_11)


        self.verticalLayout_19.addWidget(self.frame_11)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_16.addWidget(self.tabWidget)


        self.verticalLayout_17.addWidget(self.frame_9)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_83.addWidget(self.scrollArea)

        self.body.addWidget(self.shili_page6)
        self.jingxiang_page7 = QWidget()
        self.jingxiang_page7.setObjectName(u"jingxiang_page7")
        self.jingxiang_page7.setStyleSheet(u"")
        self.verticalLayout_84 = QVBoxLayout(self.jingxiang_page7)
        self.verticalLayout_84.setObjectName(u"verticalLayout_84")
        self.frame_8 = QFrame(self.jingxiang_page7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setStyleSheet(u"")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_8)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.label_5 = QLabel(self.frame_8)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"QLabel {\n"
"    background-color: #3F454F;\n"
"    border-radius: 10px;\n"
"    border-radius: 10px;\n"
"}")

        self.verticalLayout_15.addWidget(self.label_5)

        self.listWidget_3 = QListWidget(self.frame_8)
        __qlistwidgetitem4 = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem4.setFont(font);
        __qlistwidgetitem5 = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem5.setFont(font);
        __qlistwidgetitem6 = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem6.setFont(font);
        __qlistwidgetitem7 = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem7.setFont(font);
        __qlistwidgetitem8 = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem8.setFont(font);
        __qlistwidgetitem9 = QListWidgetItem(self.listWidget_3)
        __qlistwidgetitem9.setFont(font);
        self.listWidget_3.setObjectName(u"listWidget_3")
        sizePolicy4.setHeightForWidth(self.listWidget_3.sizePolicy().hasHeightForWidth())
        self.listWidget_3.setSizePolicy(sizePolicy4)
        self.listWidget_3.setMinimumSize(QSize(0, 0))
        self.listWidget_3.setStyleSheet(u"background-color: #363636;")

        self.verticalLayout_15.addWidget(self.listWidget_3)

        self.frame_12 = QFrame(self.frame_8)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setStyleSheet(u"QPushButton {\n"
"    background-color: #CC9933;\n"
"    border-radius: 10px;\n"
"    font: 10pt \"\u5b8b\u4f53\";\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_14 = QPushButton(self.frame_12)
        self.pushButton_14.setObjectName(u"pushButton_14")
        icon23 = QIcon()
        icon23.addFile(u":/ico/ico/x-octagon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_14.setIcon(icon23)

        self.horizontalLayout_5.addWidget(self.pushButton_14, 0, Qt.AlignmentFlag.AlignLeft)

        self.pushButton_6 = QPushButton(self.frame_12)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setStyleSheet(u"font: 10pt \"Microsoft YaHei UI\";")
        icon24 = QIcon()
        icon24.addFile(u":/ico/ico/shopping-bag.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_6.setIcon(icon24)

        self.horizontalLayout_5.addWidget(self.pushButton_6, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_15.addWidget(self.frame_12)

        self.frame_10 = QFrame(self.frame_8)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setStyleSheet(u"QPushButton {\n"
"    background-color: #CCCC33;\n"
"    border-radius: 10px;\n"
"    font: 20pt \"\u5b8b\u4f53\";\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.frame_10)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")

        self.verticalLayout_15.addWidget(self.frame_10)


        self.verticalLayout_84.addWidget(self.frame_8, 0, Qt.AlignmentFlag.AlignTop)

        self.body.addWidget(self.jingxiang_page7)
        self.fengzhuang_page8 = QWidget()
        self.fengzhuang_page8.setObjectName(u"fengzhuang_page8")
        self.fengzhuang_page8.setStyleSheet(u"")
        self.verticalLayout_85 = QVBoxLayout(self.fengzhuang_page8)
        self.verticalLayout_85.setObjectName(u"verticalLayout_85")
        self.body.addWidget(self.fengzhuang_page8)
        self.comfyui_page9 = QWidget()
        self.comfyui_page9.setObjectName(u"comfyui_page9")
        self.comfyui_page9.setStyleSheet(u"")
        self.verticalLayout_86 = QVBoxLayout(self.comfyui_page9)
        self.verticalLayout_86.setObjectName(u"verticalLayout_86")
        self.body.addWidget(self.comfyui_page9)
        self.list_jingxiang = QWidget()
        self.list_jingxiang.setObjectName(u"list_jingxiang")
        self.list_jingxiang.setStyleSheet(u"")
        self.verticalLayout_87 = QVBoxLayout(self.list_jingxiang)
        self.verticalLayout_87.setObjectName(u"verticalLayout_87")
        self.scrollArea_2 = QScrollArea(self.list_jingxiang)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 587, 138))
        self.verticalLayout_22 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.frame_20 = QFrame(self.scrollAreaWidgetContents_2)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.frame_20)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.label_11 = QLabel(self.frame_20)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"background-color: #363636;")

        self.verticalLayout_23.addWidget(self.label_11)

        self.listWidget_7 = QListWidget(self.frame_20)
        QListWidgetItem(self.listWidget_7)
        self.listWidget_7.setObjectName(u"listWidget_7")
        self.listWidget_7.setStyleSheet(u"background-color: #363636;")

        self.verticalLayout_23.addWidget(self.listWidget_7, 0, Qt.AlignmentFlag.AlignTop)

        self.pushButton = QPushButton(self.frame_20)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #CC9933;\n"
"    border-radius: 10px;\n"
"    font: 10pt \"\u5b8b\u4f53\";\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4F6F6F; /* \u6309\u4e0b\u65f6\u7684\u80cc\u666f\u989c\u8272 */\n"
"}\n"
"font: 10pt \"Microsoft YaHei UI\";")
        self.pushButton.setIcon(icon24)

        self.verticalLayout_23.addWidget(self.pushButton)


        self.verticalLayout_22.addWidget(self.frame_20, 0, Qt.AlignmentFlag.AlignTop)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_87.addWidget(self.scrollArea_2)

        self.body.addWidget(self.list_jingxiang)
        self.fluxgym_page11 = QWidget()
        self.fluxgym_page11.setObjectName(u"fluxgym_page11")
        self.fluxgym_page11.setStyleSheet(u"")
        self.verticalLayout_88 = QVBoxLayout(self.fluxgym_page11)
        self.verticalLayout_88.setObjectName(u"verticalLayout_88")
        self.body.addWidget(self.fluxgym_page11)
        self.zanzhu_page12 = QWidget()
        self.zanzhu_page12.setObjectName(u"zanzhu_page12")
        self.zanzhu_page12.setStyleSheet(u"")
        self.verticalLayout_89 = QVBoxLayout(self.zanzhu_page12)
        self.verticalLayout_89.setObjectName(u"verticalLayout_89")
        self.body.addWidget(self.zanzhu_page12)

        self.horizontalLayout.addWidget(self.body)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.body.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u987a\u52bfAI", None))
#if QT_CONFIG(tooltip)
        self.menubtn.setToolTip(QCoreApplication.translate("MainWindow", u"\u4ed9\u5bab\u4e91\u8d26\u53f7", None))
#endif // QT_CONFIG(tooltip)
        self.menubtn.setText(QCoreApplication.translate("MainWindow", u"\u4ed9\u5bab\u4e91\u8d26\u53f7", None))
#if QT_CONFIG(tooltip)
        self.home.setToolTip(QCoreApplication.translate("MainWindow", u"\u4e3b\u9875", None))
#endif // QT_CONFIG(tooltip)
        self.home.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9875", None))
        self.shiliBt.setText(QCoreApplication.translate("MainWindow", u"\u5b9e\u4f8b", None))
#if QT_CONFIG(tooltip)
        self.jingxiang.setToolTip(QCoreApplication.translate("MainWindow", u"\u955c\u50cf", None))
#endif // QT_CONFIG(tooltip)
        self.jingxiang.setText(QCoreApplication.translate("MainWindow", u"\u79c1\u6709\u955c\u50cf", None))
#if QT_CONFIG(tooltip)
        self.jingxiang_2.setToolTip(QCoreApplication.translate("MainWindow", u"\u955c\u50cf", None))
#endif // QT_CONFIG(tooltip)
        self.jingxiang_2.setText(QCoreApplication.translate("MainWindow", u"\u516c\u5171\u955c\u50cf", None))
#if QT_CONFIG(tooltip)
        self.comfyui.setToolTip(QCoreApplication.translate("MainWindow", u"comfyui", None))
#endif // QT_CONFIG(tooltip)
        self.comfyui.setText(QCoreApplication.translate("MainWindow", u"comfyui", None))
#if QT_CONFIG(tooltip)
        self.fengzhuang.setToolTip(QCoreApplication.translate("MainWindow", u"\u5c01\u88c5\u6d41", None))
#endif // QT_CONFIG(tooltip)
        self.fengzhuang.setText(QCoreApplication.translate("MainWindow", u"\u5c01\u88c5\u6d41", None))
#if QT_CONFIG(tooltip)
        self.fluxgym.setToolTip(QCoreApplication.translate("MainWindow", u"fluxgym", None))
#endif // QT_CONFIG(tooltip)
        self.fluxgym.setText(QCoreApplication.translate("MainWindow", u"fluxgym", None))
#if QT_CONFIG(tooltip)
        self.shuchu.setToolTip(QCoreApplication.translate("MainWindow", u"gptsovits", None))
#endif // QT_CONFIG(tooltip)
        self.shuchu.setText(QCoreApplication.translate("MainWindow", u"\u8f93\u51fa\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.quanbu.setToolTip(QCoreApplication.translate("MainWindow", u"gptsovits", None))
#endif // QT_CONFIG(tooltip)
        self.quanbu.setText(QCoreApplication.translate("MainWindow", u"\u5168\u90e8\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.quanbu_2.setToolTip(QCoreApplication.translate("MainWindow", u"gptsovits", None))
#endif // QT_CONFIG(tooltip)
        self.quanbu_2.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8\u5668", None))
#if QT_CONFIG(tooltip)
        self.settings.setToolTip(QCoreApplication.translate("MainWindow", u"\u70b9\u51fb\u8bbe\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.settings.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.info.setToolTip(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e\u8f6f\u4ef6\u7684\u8be6\u7ec6\u4fe1\u606f", None))
#endif // QT_CONFIG(tooltip)
        self.info.setText(QCoreApplication.translate("MainWindow", u"\u4fe1\u606f", None))
#if QT_CONFIG(tooltip)
        self.help.setToolTip(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
#endif // QT_CONFIG(tooltip)
        self.help.setText(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'DeepSeek-CJK-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Noto Sans','Ubuntu','Cantarell','Helvetica Neue','Oxygen','Open Sans','sans-serif'; color:#f8faff; backgrou"
                        "nd-color:#292a2d;\">\u60a8\u7684\u8bbf\u95ee\u4ee4\u724c\u662f\u654f\u611f\u8eab\u4efd\u51ed\u8bc1\uff0c\u7b49\u540c\u4e8e\u8d26\u6237\u5bc6\u7801\u3002\u4e3a\u786e\u4fdd\u5b89\u5168\uff0c\u8bf7\u52a1\u5fc5\u9075\u5faa\u4ee5\u4e0b\u51c6\u5219\uff1a</span></p>\n"
"<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" font-family:'DeepSeek-CJK-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Noto Sans','Ubuntu','Cantarell','Helvetica Neue','Oxygen','Open Sans','sans-serif'; color:#f8faff; background-color:#292a2d;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">\u4e25\u7981\u6cc4\u9732</span>\uff1a\u5207\u52ff\u901a\u8fc7\u804a\u5929\u5de5\u5177\u3001\u90ae\u4ef6\u3001\u4ee3\u7801\u4ed3\u5e93\u6216\u622a\u56fe\u7b49\u65b9\u5f0f\u5171\u4eab\u4ee4\u724c\u3002</li>\n"
"<li style=\" font-family:'DeepSeek-C"
                        "JK-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Noto Sans','Ubuntu','Cantarell','Helvetica Neue','Oxygen','Open Sans','sans-serif'; color:#f8faff; background-color:#292a2d;\" style=\" margin-top:4px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">\u6700\u5c0f\u5316\u7559\u5b58</span>\uff1a\u4f7f\u7528\u540e\u6700\u597d\u7acb\u5373\u901a\u8fc7<span style=\" color:#ff2024;\">\u5b98\u65b9\u63a7\u5236\u53f0\u7684\u8d26\u53f7\u7ba1\u7406</span>\u5220\u9664\u4ee4\u724c\uff0c\u907f\u514d\u957f\u671f\u6709\u6548\u5bfc\u81f4\u98ce\u9669\u3002</li>\n"
"<li style=\" font-family:'DeepSeek-CJK-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Noto Sans','Ubuntu','Cantarell','Helvetica Neue','Oxygen','Open Sans','sans-serif'; color:#f8faff; background-color:#292a2d;\" style=\" margin-top:4px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-i"
                        "ndent:0px;\"><span style=\" font-weight:700;\">\u8f6f\u4ef6\u6700\u597d\u5230\u4f5c\u8005\u4ed3\u5e93\u4e0b\u8f7d</span>\uff1a\u82e5\u8981\u5206\u4eab\u8f6f\u4ef6\u4e00\u5b9a\u8981\u6e05\u9664\u8bbf\u95ee\u4ee4\u724c\u6216\u8005\u9075\u5faa\u4ee5\u4e0a\u7b2c\u4e8c\u70b9\u3002</li></ol>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'DeepSeek-CJK-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Noto Sans','Ubuntu','Cantarell','Helvetica Neue','Oxygen','Open Sans','sans-serif'; color:#f8faff; background-color:#292a2d;\">\u26a0\ufe0f \u82e5\u53d1\u73b0\u4ee4\u724c\u610f\u5916\u66b4\u9732\uff0c\u8bf7\u70b9\u51fb &quot;</span><span style=\" font-family:'DeepSeek-CJK-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Noto Sans','Ubuntu','Cantarell','Helvetica Neue','Oxygen','Open Sans','sans-serif'; color:#ffbf00; background-color:#292a2d;\">\u83b7"
                        "\u53d6\u8bbf\u95ee\u4ee4\u724c</span><span style=\" font-family:'DeepSeek-CJK-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Noto Sans','Ubuntu','Cantarell','Helvetica Neue','Oxygen','Open Sans','sans-serif'; color:#f8faff; background-color:#292a2d;\">&quot;\u6309\u94ae\u8df3\u8f6c\u5230\u5b98\u7f51 \u7acb\u5373\u5220\u9664\u5e76\u91cd\u65b0\u751f\u6210\uff01</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'DeepSeek-CJK-patch','Inter','system-ui','-apple-system','BlinkMacSystemFont','Segoe UI','Roboto','Noto Sans','Ubuntu','Cantarell','Helvetica Neue','Oxygen','Open Sans','sans-serif'; color:#f8faff;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tishi.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:26pt; color:#ffffff;\">\u8f93\u5165\u4ed9\u5bab\u4e91\u8bbf\u95ee\u4ee4\u724c</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.lingpai.setToolTip(QCoreApplication.translate("MainWindow", u"\u63d0\u793a\u8f93\u5165\u6846\u8981\u8f93\u5165\u7684\u5185\u5bb9", None))
#endif // QT_CONFIG(tooltip)
        self.lingpai.setText("")
        self.lingpai.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f93\u5165\u4ed9\u5bab\u4e91\u8bbf\u95ee\u4ee4\u724c", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"\u8bb0\u4f4f\u4ee4\u724c", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"\u786e\u5b9a", None))
        self.huoqu.setText(QCoreApplication.translate("MainWindow", u"\u83b7\u53d6\u8bbf\u95ee\u4ee4\u724c", None))
#if QT_CONFIG(tooltip)
        self.zhuce.setToolTip(QCoreApplication.translate("MainWindow", u"\u6ce8\u518c\u4ed9\u5bab\u4e91\u8d26\u53f7", None))
#endif // QT_CONFIG(tooltip)
        self.zhuce.setText(QCoreApplication.translate("MainWindow", u"\u6ce8\u518c", None))
#if QT_CONFIG(tooltip)
        self.coffee.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bf7\u4f5c\u8005\u548c\u5496\u5561</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.coffee.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u4f5c\u8005\u559d\u5496\u5561", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6ecomfyui\u7aef\u53e3", None))
        self.dailikuang_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba48188", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u5c01\u88c5\u6d41\u7aef\u53e3", None))
        self.dailikuang_3.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba47861", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6efluxgym\u7aef\u53e3", None))
        self.dailikuang_4.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba47860", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u8f93\u51fa\u6587\u4ef6\u7aef\u53e3", None))
        self.dailikuang_6.setText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba48080", None))
        self.dailikuang_6.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u5168\u90e8\u6587\u4ef6\u7aef\u53e3", None))
        self.dailikuang_5.setText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba48081", None))
        self.dailikuang_5.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba47860", None))
        self.textBrowser1.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt;\">\u987a\u52bfAI</span><"
                        "/p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7248\u672c\uff1a1.0-20250401(64\u4f4d)</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2025-2025  hua</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u8f6c\u6362Qt Widgets Designer\u4ee3\u7801\u4e3apython\u7684\u547d\u4ee4\u5982\u4e0b\u793a\u4f8b\uff1a</p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;"
                        " margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; color:#ffffff;\">pyside6-uic demo.ui </span><span style=\" font-family:'Courier New'; color:#81a1c1;\">-o</span><span style=\" font-family:'Courier New'; color:#ffffff;\"> ui_demo.py</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; color:#ffffff;\">pyside6-rcc resources.qrc </span><span style=\" font-family:'Courier New'; color:#81a1c1;\">-o</span><span style=\" font-family:'Courier New'; color:#ffffff;\"> resources_rc.py</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Courier New'; color:#ffffff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;"
                        " text-indent:0px;\">\u57fa\u4e8epyside6 \uff1b<span style=\" font-family:'Menlo','Roboto Mono','Courier New','Courier','monospace','Inter','sans-serif'; font-weight:600; color:#f8faff; background-color:#424242;\">PyQt6; python\u8bed\u8a00</span></p></body></html>", None))
        self.textBrowser2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. \u57fa\u672c\u6761\u6b3e</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u2705 \u672c\u8f6f\u4ef6\u6c38\u4e45\u514d\u8d39\uff0c\u5141\u8bb8\u4e2a\u4eba\u548c\u4f01\u4e1a\u5546\u4e1a\u7528\u9014\u4f7f\u7528\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-blo"
                        "ck-indent:0; text-indent:0px;\">\u274c \u7981\u6b62\u884c\u4e3a\uff1a</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u51fa\u552e\u3001\u51fa\u79df\u6216\u6346\u7ed1\u672c\u8f6f\u4ef6\u76c8\u5229\uff1b</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u4fee\u6539\u8f6f\u4ef6\u5e76\u58f0\u79f0\u81ea\u5df1\u662f\u539f\u4f5c\u8005\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. \u514d\u8d23\u58f0\u660e</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u672c\u8f6f\u4ef6\u6309\u201c\u539f\u6837\u201d\u63d0\u4f9b\uff0c\u4e0d\u627f\u62c5\u56e0\u4f7f\u7528\u5bfc\u81f4\u7684\u4efb\u4f55\u6570\u636e\u4e22\u5931\u3001\u8bbe\u5907\u635f\u574f\u6216\u6cd5\u5f8b\u8d23\u4efb\u3002</p>\n"
"<p style=\""
                        " margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5f00\u53d1\u8005\u65e0\u4e49\u52a1\u63d0\u4f9b\u6280\u672f\u652f\u6301\u6216\u66f4\u65b0\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. \u65e0\u6076\u610f\u4ee3\u7801\u58f0\u660e</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5f00\u53d1\u8005\u90d1\u91cd\u58f0\u660e\uff1a\u672c\u8f6f\u4ef6\u4e0d\u5305\u542b\u4efb\u4f55\u75c5\u6bd2\u3001\u540e\u95e8\u3001\u95f4\u8c0d\u8f6f\u4ef6\u3001\u6316\u77ff\u7a0b\u5e8f\u7b49\u6076\u610f\u4ee3\u7801\u3002</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u7528\u6237\u53ef\u901a\u8fc7[\u7b2c\u4e09\u65b9\u68c0\u6d4b\u5de5\u5177/\u7f51\u5740]\u81ea\u884c\u9a8c\u8bc1\uff08\u53ef\u9009\uff09\u3002</p>\n"
"<p style=\" "
                        "margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. \u4e3e\u62a5\u4e0e\u8d23\u4efb</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u53d1\u73b0\u5012\u5356\u6216\u5b89\u5168\u95ee\u9898\u8bf7\u8054\u7cfb\uff1awechat: KritaBlenderComfyui</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u8fdd\u53cd\u672c\u534f\u8bae\u8005\uff0c\u5f00\u53d1\u8005\u4fdd\u7559\u8ffd\u7a76\u6cd5\u5f8b\u8d23\u4efb\u7684\u6743\u5229\u3002</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px"
                        ";\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-rig"
                        "ht:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; mar"
                        "gin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u95ee\u9898\u53cd\u9988\uff0c\u8bf7\u5bfc\u822a\u5230\u4ed3\u5e93\u5730\u5740\u8fdb\u884c\u53cd\u9988\uff1a</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00ff1e;\">https://github.com/kungful/xiangongyun_GUI.git</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u7528\u6237\u4fe1\u606f</span></p></body></html>", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u" \u6635\u79f0\uff1a", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u" uuid:", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u" \u7535\u8bdd\uff1a", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u8d26\u6237\u4f59\u989d</span></p></body></html>", None))

        __sortingEnabled1 = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        ___qlistwidgetitem3 = self.listWidget_2.item(0)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u" \u4f59\u989d\uff1a", None));
        self.listWidget_2.setSortingEnabled(__sortingEnabled1)

        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u8d26\u6237\u5145\u503c</span></p></body></html>", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"wechat", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"alipay", None))

        self.spinBox.setSpecialValueText(QCoreApplication.translate("MainWindow", u"\u8bf7\u8f93\u5165; \u6700\u5c11\u5145\u503c5\u5143", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u786e\u8ba4\u5145\u503c", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u67e5\u8be2\u8ba2\u5355</span></p></body></html>", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"                             \u67e5\u8be2", None))

        __sortingEnabled2 = self.listWidget_5.isSortingEnabled()
        self.listWidget_5.setSortingEnabled(False)
        ___qlistwidgetitem4 = self.listWidget_5.item(0)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u5b9e\u4f8bID\uff1a", None));
        ___qlistwidgetitem5 = self.listWidget_5.item(1)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u4e2d\u5fc3\u540d\u79f0\uff1a", None));
        ___qlistwidgetitem6 = self.listWidget_5.item(2)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"GPU\u578b\u53f7\uff1a", None));
        ___qlistwidgetitem7 = self.listWidget_5.item(3)
        ___qlistwidgetitem7.setText(QCoreApplication.translate("MainWindow", u"CPU\u578b\u53f7\uff1a", None));
        ___qlistwidgetitem8 = self.listWidget_5.item(4)
        ___qlistwidgetitem8.setText(QCoreApplication.translate("MainWindow", u"CPU\u6838\u5fc3\u6570\uff1a", None));
        ___qlistwidgetitem9 = self.listWidget_5.item(5)
        ___qlistwidgetitem9.setText(QCoreApplication.translate("MainWindow", u"\u5185\u5b58\u5927\u5c0f\uff1a", None));
        ___qlistwidgetitem10 = self.listWidget_5.item(6)
        ___qlistwidgetitem10.setText(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u78c1\u76d8\u5927\u5c0f\uff1a", None));
        ___qlistwidgetitem11 = self.listWidget_5.item(7)
        ___qlistwidgetitem11.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u78c1\u76d8\u5927\u5c0f\uff1a", None));
        ___qlistwidgetitem12 = self.listWidget_5.item(8)
        ___qlistwidgetitem12.setText(QCoreApplication.translate("MainWindow", u"\u53ef\u6269\u5c55\u6570\u636e\u78c1\u76d8\u5927\u5c0f\uff1a", None));
        ___qlistwidgetitem13 = self.listWidget_5.item(9)
        ___qlistwidgetitem13.setText(QCoreApplication.translate("MainWindow", u"\u4e91\u7aef\u50a8\u5b58\u8def\u5f84\uff1a", None));
        ___qlistwidgetitem14 = self.listWidget_5.item(10)
        ___qlistwidgetitem14.setText(QCoreApplication.translate("MainWindow", u"\u6bcf\u5c0f\u65f6\u4ef7\u683c\uff1a", None));
        ___qlistwidgetitem15 = self.listWidget_5.item(11)
        ___qlistwidgetitem15.setText(QCoreApplication.translate("MainWindow", u"ssh_key:", None));
        ___qlistwidgetitem16 = self.listWidget_5.item(12)
        ___qlistwidgetitem16.setText(QCoreApplication.translate("MainWindow", u"ssh_port:", None));
        ___qlistwidgetitem17 = self.listWidget_5.item(13)
        ___qlistwidgetitem17.setText(QCoreApplication.translate("MainWindow", u"ssh_user:", None));
        ___qlistwidgetitem18 = self.listWidget_5.item(14)
        ___qlistwidgetitem18.setText(QCoreApplication.translate("MainWindow", u"password:", None));
        ___qlistwidgetitem19 = self.listWidget_5.item(15)
        ___qlistwidgetitem19.setText(QCoreApplication.translate("MainWindow", u"jupyter_token:", None));
        ___qlistwidgetitem20 = self.listWidget_5.item(16)
        ___qlistwidgetitem20.setText(QCoreApplication.translate("MainWindow", u"jupyter_url:", None));
        ___qlistwidgetitem21 = self.listWidget_5.item(17)
        ___qlistwidgetitem21.setText(QCoreApplication.translate("MainWindow", u"xgcos_token:", None));
        ___qlistwidgetitem22 = self.listWidget_5.item(18)
        ___qlistwidgetitem22.setText(QCoreApplication.translate("MainWindow", u"xgcos_url:", None));
        ___qlistwidgetitem23 = self.listWidget_5.item(19)
        ___qlistwidgetitem23.setText(QCoreApplication.translate("MainWindow", u"\u72b6\u6001\uff1a", None));
        ___qlistwidgetitem24 = self.listWidget_5.item(20)
        ___qlistwidgetitem24.setText(QCoreApplication.translate("MainWindow", u"ssh_domain:", None));
        ___qlistwidgetitem25 = self.listWidget_5.item(21)
        ___qlistwidgetitem25.setText(QCoreApplication.translate("MainWindow", u"web_url:", None));
        ___qlistwidgetitem26 = self.listWidget_5.item(22)
        ___qlistwidgetitem26.setText(QCoreApplication.translate("MainWindow", u"\u955c\u50cfID\uff1a", None));
        ___qlistwidgetitem27 = self.listWidget_5.item(23)
        ___qlistwidgetitem27.setText(QCoreApplication.translate("MainWindow", u"\u955c\u50cf\u7c7b\u578b\uff1a", None));
        ___qlistwidgetitem28 = self.listWidget_5.item(24)
        ___qlistwidgetitem28.setText(QCoreApplication.translate("MainWindow", u"\u955c\u50cf\u4ef7\u683c\uff1a", None));
        ___qlistwidgetitem29 = self.listWidget_5.item(25)
        ___qlistwidgetitem29.setText(QCoreApplication.translate("MainWindow", u"\u955c\u50cf\u4fdd\u5b58\uff1a", None));
        ___qlistwidgetitem30 = self.listWidget_5.item(26)
        ___qlistwidgetitem30.setText(QCoreApplication.translate("MainWindow", u"\u57fa\u7840\u4ef7\u683c\uff1a", None));
        ___qlistwidgetitem31 = self.listWidget_5.item(27)
        ___qlistwidgetitem31.setText(QCoreApplication.translate("MainWindow", u"auto_shutdown:", None));
        ___qlistwidgetitem32 = self.listWidget_5.item(28)
        ___qlistwidgetitem32.setText(QCoreApplication.translate("MainWindow", u"auto_shutdown_action:", None));
        self.listWidget_5.setSortingEnabled(__sortingEnabled2)

        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u" \u5f00\u673a", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\u50a8\u5b58\u955c\u50cf", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"\u5173\u673a\u4fdd\u7559GPU", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\u5173\u673a\u91ca\u653eGPU", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\u5173\u673a\u5e76\u9500\u6bc1", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"\u50a8\u5b58\u5e76\u9500\u6bc1", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"\u9500\u6bc1\u5b9e\u4f8b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u5b9e\u4f8b1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u5b9e\u4f8b2", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u955c\u50cf\u603b\u6570\uff1a", None))

        __sortingEnabled3 = self.listWidget_3.isSortingEnabled()
        self.listWidget_3.setSortingEnabled(False)
        ___qlistwidgetitem33 = self.listWidget_3.item(0)
        ___qlistwidgetitem33.setText(QCoreApplication.translate("MainWindow", u"   \u955c\u50cfID\uff1a", None));
        ___qlistwidgetitem34 = self.listWidget_3.item(1)
        ___qlistwidgetitem34.setText(QCoreApplication.translate("MainWindow", u"\u955c\u50cf\u540d\u5b57\uff1a", None));
        ___qlistwidgetitem35 = self.listWidget_3.item(2)
        ___qlistwidgetitem35.setText(QCoreApplication.translate("MainWindow", u"      \u91c7\u7528\uff1a", None));
        ___qlistwidgetitem36 = self.listWidget_3.item(3)
        ___qlistwidgetitem36.setText(QCoreApplication.translate("MainWindow", u"\u955c\u50cf\u5927\u5c0f\uff1a", None));
        ___qlistwidgetitem37 = self.listWidget_3.item(4)
        ___qlistwidgetitem37.setText(QCoreApplication.translate("MainWindow", u"\u53ef\u7528\u72b6\u6001\uff1a", None));
        ___qlistwidgetitem38 = self.listWidget_3.item(5)
        ___qlistwidgetitem38.setText(QCoreApplication.translate("MainWindow", u"\u662f\u5426\u539f\u4e3b\uff1a", None));
        self.listWidget_3.setSortingEnabled(__sortingEnabled3)

        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"\u9500\u6bc1\u955c\u50cf", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"\u90e8\u7f72\u6b64\u955c\u50cf", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u8f6f\u4ef6\u4f5c\u8005\uff08\u63a8\u8350) : h\u5f00\u53d1\u8005\u7684\u955c\u50cf  \u66f4\u65b0\u4e8e 2025-03-31_160.86GB \u955c\u50cf\u63cf\u8ff0: free\uff1b\u6c38\u4e45\u514d\u8d39\uff0c\u6301\u7eed\u5f00\u53d1", None))

        __sortingEnabled4 = self.listWidget_7.isSortingEnabled()
        self.listWidget_7.setSortingEnabled(False)
        ___qlistwidgetitem39 = self.listWidget_7.item(0)
        ___qlistwidgetitem39.setText(QCoreApplication.translate("MainWindow", u"7b36c1a3-da41-4676-b5b3-03ec25d6e197", None));
        self.listWidget_7.setSortingEnabled(__sortingEnabled4)

        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u90e8\u7f72\u955c\u50cf", None))
    # retranslateUi

