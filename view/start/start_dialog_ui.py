# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'start_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLayout, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_StartDialog(object):
    def setupUi(self, StartDialog):
        if not StartDialog.objectName():
            StartDialog.setObjectName(u"StartDialog")
        StartDialog.resize(880, 520)
        self.horizontalLayout = QHBoxLayout(StartDialog)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_menu = QVBoxLayout()
        self.verticalLayout_menu.setObjectName(u"verticalLayout_menu")
        self.verticalLayout_menu.setContentsMargins(0, 0, -1, -1)
        self.label_logo_360x160 = QLabel(StartDialog)
        self.label_logo_360x160.setObjectName(u"label_logo_360x160")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_logo_360x160.sizePolicy().hasHeightForWidth())
        self.label_logo_360x160.setSizePolicy(sizePolicy)
        self.label_logo_360x160.setMaximumSize(QSize(420, 280))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_logo_360x160.setFont(font)
        self.label_logo_360x160.setStyleSheet(u"QFrame{\n"
"	border: 1px solid darkgray;\n"
"	border-radius: 4px;\n"
"}\n"
"")
        self.label_logo_360x160.setFrameShape(QFrame.Shape.StyledPanel)
        self.label_logo_360x160.setFrameShadow(QFrame.Shadow.Sunken)
        self.label_logo_360x160.setLineWidth(1)
        self.label_logo_360x160.setScaledContents(True)
        self.label_logo_360x160.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_logo_360x160.setMargin(2)

        self.verticalLayout_menu.addWidget(self.label_logo_360x160)

        self.horizontalLayout_button = QHBoxLayout()
        self.horizontalLayout_button.setSpacing(4)
        self.horizontalLayout_button.setObjectName(u"horizontalLayout_button")
        self.horizontalLayout_button.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_button.setContentsMargins(20, 15, 20, 8)
        self.pushButton_new = QPushButton(StartDialog)
        self.pushButton_new.setObjectName(u"pushButton_new")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_new.sizePolicy().hasHeightForWidth())
        self.pushButton_new.setSizePolicy(sizePolicy1)
        self.pushButton_new.setMinimumSize(QSize(110, 70))
        self.pushButton_new.setMaximumSize(QSize(110, 70))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        font1.setItalic(False)
        font1.setUnderline(False)
        font1.setKerning(False)
        self.pushButton_new.setFont(font1)
        self.pushButton_new.setStyleSheet(u"QPushButton::hover {\n"
"	border: 1px solid darkorange;\n"
"    border-radius: 4px;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,\n"
"                                stop: 0 #FFE5B5, stop: 1 #FCBE4C);\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	border: 2px solid orange;\n"
"    border-radius: 5px;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,\n"
"                                stop: 0 #FCBE4C, stop: 1 #DBB239);\n"
"}")
        self.pushButton_new.setIconSize(QSize(36, 36))

        self.horizontalLayout_button.addWidget(self.pushButton_new)

        self.pushButton_open = QPushButton(StartDialog)
        self.pushButton_open.setObjectName(u"pushButton_open")
        sizePolicy1.setHeightForWidth(self.pushButton_open.sizePolicy().hasHeightForWidth())
        self.pushButton_open.setSizePolicy(sizePolicy1)
        self.pushButton_open.setMinimumSize(QSize(110, 70))
        self.pushButton_open.setMaximumSize(QSize(110, 70))
        self.pushButton_open.setFont(font1)
        self.pushButton_open.setStyleSheet(u"QPushButton::hover {\n"
"	border: 1px solid darkorange;\n"
"    border-radius: 4px;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,\n"
"                                stop: 0 #FFE5B5, stop: 1 #FCBE4C);\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	border: 2px solid orange;\n"
"    border-radius: 5px;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,\n"
"                                stop: 0 #FCBE4C, stop: 1 #DBB239);\n"
"}")
        self.pushButton_open.setIconSize(QSize(36, 36))

        self.horizontalLayout_button.addWidget(self.pushButton_open)

        self.pushButton_exit = QPushButton(StartDialog)
        self.pushButton_exit.setObjectName(u"pushButton_exit")
        sizePolicy1.setHeightForWidth(self.pushButton_exit.sizePolicy().hasHeightForWidth())
        self.pushButton_exit.setSizePolicy(sizePolicy1)
        self.pushButton_exit.setMinimumSize(QSize(110, 70))
        self.pushButton_exit.setMaximumSize(QSize(110, 70))
        self.pushButton_exit.setFont(font1)
        self.pushButton_exit.setStyleSheet(u"QPushButton::hover {\n"
"	border: 1px solid darkorange;\n"
"    border-radius: 4px;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,\n"
"                                stop: 0 #FFE5B5, stop: 1 #FCBE4C);\n"
"}\n"
"\n"
"QPushButton::pressed {\n"
"	border: 2px solid orange;\n"
"    border-radius: 5px;\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,\n"
"                                stop: 0 #FCBE4C, stop: 1 #DBB239);\n"
"}")
        self.pushButton_exit.setIconSize(QSize(36, 36))

        self.horizontalLayout_button.addWidget(self.pushButton_exit)


        self.verticalLayout_menu.addLayout(self.horizontalLayout_button)

        self.label_notice = QLabel(StartDialog)
        self.label_notice.setObjectName(u"label_notice")
        self.label_notice.setMinimumSize(QSize(0, 40))
        self.label_notice.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(False)
        self.label_notice.setFont(font2)
        self.label_notice.setStyleSheet(u"QFrame{\n"
"	border: 1px solid darkgray;\n"
"	border-radius: 4px;\n"
"}\n"
"")
        self.label_notice.setFrameShape(QFrame.Shape.StyledPanel)
        self.label_notice.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_menu.addWidget(self.label_notice)

        self.line = QFrame(StartDialog)
        self.line.setObjectName(u"line")
        self.line.setFont(font2)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.line.setLineWidth(1)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_menu.addWidget(self.line)

        self.label_name = QLabel(StartDialog)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setMaximumSize(QSize(16777215, 20))
        font3 = QFont()
        font3.setPointSize(7)
        font3.setBold(False)
        font3.setItalic(True)
        self.label_name.setFont(font3)
        self.label_name.setStyleSheet(u"")
        self.label_name.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_menu.addWidget(self.label_name)

        self.verticalLayout_menu.setStretch(2, 1)

        self.horizontalLayout.addLayout(self.verticalLayout_menu)

        self.verticalLayout_recent_list = QVBoxLayout()
        self.verticalLayout_recent_list.setObjectName(u"verticalLayout_recent_list")

        self.horizontalLayout.addLayout(self.verticalLayout_recent_list)

        self.horizontalLayout.setStretch(1, 1)

        self.retranslateUi(StartDialog)

        QMetaObject.connectSlotsByName(StartDialog)
    # setupUi

    def retranslateUi(self, StartDialog):
        StartDialog.setWindowTitle(QCoreApplication.translate("StartDialog", u"Project Manager", None))
        self.label_logo_360x160.setText("")
        self.pushButton_new.setText(QCoreApplication.translate("StartDialog", u"New", None))
        self.pushButton_open.setText(QCoreApplication.translate("StartDialog", u"Open", None))
        self.pushButton_exit.setText(QCoreApplication.translate("StartDialog", u"Exit", None))
        self.label_notice.setText("")
        self.label_name.setText(QCoreApplication.translate("StartDialog", u"Massive Crowd Simulation", None))
    # retranslateUi

