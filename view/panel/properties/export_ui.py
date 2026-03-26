# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_ExportForm(object):
    def setupUi(self, ExportForm):
        if not ExportForm.objectName():
            ExportForm.setObjectName(u"ExportForm")
        ExportForm.resize(300, 413)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExportForm.sizePolicy().hasHeightForWidth())
        ExportForm.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        ExportForm.setFont(font)
        self.verticalLayout = QVBoxLayout(ExportForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.groupBox_4 = QGroupBox(ExportForm)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(True)
        self.groupBox_4.setFont(font1)
        self.groupBox_4.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 12, -1, -1)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.radioButton_5 = QRadioButton(self.groupBox_4)
        self.radioButton_5.setObjectName(u"radioButton_5")
        self.radioButton_5.setFont(font)
        self.radioButton_5.setChecked(True)

        self.horizontalLayout_8.addWidget(self.radioButton_5)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.radioButton_6 = QRadioButton(self.groupBox_4)
        self.radioButton_6.setObjectName(u"radioButton_6")
        self.radioButton_6.setFont(font)
        self.radioButton_6.setChecked(True)

        self.horizontalLayout_9.addWidget(self.radioButton_6)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.widget_2 = QWidget(self.groupBox_4)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setEnabled(True)
        self.verticalLayout_4 = QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(10, -1, -1, -1)
        self.label_5 = QLabel(self.widget_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(True)
        self.label_5.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_5)

        self.lineEdit_5 = QLineEdit(self.widget_2)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.lineEdit_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(10, -1, -1, -1)
        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_7)

        self.lineEdit_12 = QLineEdit(self.widget_2)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_12.setFont(font)
        self.lineEdit_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_11.addWidget(self.lineEdit_12)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)


        self.verticalLayout_5.addWidget(self.widget_2)

        self.line = QFrame(self.groupBox_4)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, -1, -1, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer)

        self.pushButton = QPushButton(self.groupBox_4)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font)

        self.horizontalLayout_12.addWidget(self.pushButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout_12)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_2 = QGroupBox(ExportForm)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_2.setFont(font1)
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid;\n"
"    border-radius: 6;\n"
"    margin-top: 9;\n"
"    border-color : #c8c8c8;\n"
"	padding: 3;   \n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10;\n"
"    padding: 2 3;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 12, -1, -1)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radioButton_1 = QRadioButton(self.groupBox_2)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setFont(font)
        self.radioButton_1.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radioButton_1)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radioButton_4 = QRadioButton(self.groupBox_2)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setFont(font)
        self.radioButton_4.setChecked(True)

        self.horizontalLayout_7.addWidget(self.radioButton_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.widget = QWidget(self.groupBox_2)
        self.widget.setObjectName(u"widget")
        self.widget.setEnabled(True)
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.lineEdit_3 = QLineEdit(self.widget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, -1, -1, -1)
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.lineEdit_4 = QLineEdit(self.widget)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.lineEdit_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addWidget(self.widget)

        self.line_2 = QFrame(self.groupBox_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, -1, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_2)

        self.pushButton_3 = QPushButton(self.groupBox_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setFont(font)

        self.horizontalLayout_13.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.groupBox_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setFont(font)

        self.horizontalLayout_13.addWidget(self.pushButton_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_13)


        self.verticalLayout.addWidget(self.groupBox_2)

        QWidget.setTabOrder(self.radioButton_5, self.radioButton_6)
        QWidget.setTabOrder(self.radioButton_6, self.lineEdit_5)
        QWidget.setTabOrder(self.lineEdit_5, self.lineEdit_12)
        QWidget.setTabOrder(self.lineEdit_12, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.radioButton_1)
        QWidget.setTabOrder(self.radioButton_1, self.radioButton_4)
        QWidget.setTabOrder(self.radioButton_4, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.lineEdit_4)
        QWidget.setTabOrder(self.lineEdit_4, self.pushButton_3)
        QWidget.setTabOrder(self.pushButton_3, self.pushButton_2)

        self.retranslateUi(ExportForm)

        QMetaObject.connectSlotsByName(ExportForm)
    # setupUi

    def retranslateUi(self, ExportForm):
        ExportForm.setWindowTitle(QCoreApplication.translate("ExportForm", u"Form", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ExportForm", u"< \ud574\uc11d \uacb0\uacfc \ub0b4\ubcf4\ub0b4\uae30 >", None))
        self.radioButton_5.setText(QCoreApplication.translate("ExportForm", u"\uc804\uccb4 \uc2dc\uac04", None))
        self.radioButton_6.setText(QCoreApplication.translate("ExportForm", u"\uc2dc\uac04 \uad6c\uac04 \uc124\uc815", None))
        self.label_5.setText(QCoreApplication.translate("ExportForm", u"- \uc2dc\uc791 \uc2dc\uac04(s) :", None))
        self.lineEdit_5.setText(QCoreApplication.translate("ExportForm", u"0", None))
        self.label_7.setText(QCoreApplication.translate("ExportForm", u"- \uc885\ub8cc \uc2dc\uac04(s) :", None))
        self.lineEdit_12.setText(QCoreApplication.translate("ExportForm", u"100", None))
        self.pushButton.setText(QCoreApplication.translate("ExportForm", u"\ub0b4\ubcf4\ub0b4\uae30", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ExportForm", u"< \ub80c\ub354\ub9c1 \ud654\uba74 \ub0b4\ubcf4\ub0b4\uae30 >", None))
        self.radioButton_1.setText(QCoreApplication.translate("ExportForm", u"\uc804\uccb4 \uc2dc\uac04", None))
        self.radioButton_4.setText(QCoreApplication.translate("ExportForm", u"\uc2dc\uac04 \uad6c\uac04 \uc124\uc815", None))
        self.label_3.setText(QCoreApplication.translate("ExportForm", u"- \uc2dc\uc791 \uc2dc\uac04(s) :", None))
        self.lineEdit_3.setText(QCoreApplication.translate("ExportForm", u"0", None))
        self.label_4.setText(QCoreApplication.translate("ExportForm", u"- \uc885\ub8cc \uc2dc\uac04(s) :", None))
        self.lineEdit_4.setText(QCoreApplication.translate("ExportForm", u"100", None))
        self.pushButton_3.setText(QCoreApplication.translate("ExportForm", u"\ub0b4\ubcf4\ub0b4\uae30(\ub3d9\uc601\uc0c1)", None))
        self.pushButton_2.setText(QCoreApplication.translate("ExportForm", u"\ub0b4\ubcf4\ub0b4\uae30(\uc774\ubbf8\uc9c0)", None))
    # retranslateUi

