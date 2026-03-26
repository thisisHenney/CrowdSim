# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'position.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_PositionForm(object):
    def setupUi(self, PositionForm):
        if not PositionForm.objectName():
            PositionForm.setObjectName(u"PositionForm")
        PositionForm.resize(300, 328)
        self.verticalLayout = QVBoxLayout(PositionForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.groupBox = QGroupBox(PositionForm)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setPointSize(8)
        font.setBold(True)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
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
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 12, -1, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")
        font1 = QFont()
        font1.setPointSize(9)
        self.radioButton.setFont(font1)
        self.radioButton.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setFont(font1)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font1)

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_4 = QRadioButton(self.groupBox)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setFont(font1)
        self.radioButton_4.setChecked(True)

        self.horizontalLayout_3.addWidget(self.radioButton_4)

        self.lineEdit_3 = QLineEdit(self.groupBox)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setFont(font1)
        self.lineEdit_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.lineEdit_3)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setFont(font1)

        self.horizontalLayout_3.addWidget(self.pushButton_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.radioButton_5 = QRadioButton(self.groupBox)
        self.radioButton_5.setObjectName(u"radioButton_5")
        self.radioButton_5.setFont(font1)
        self.radioButton_5.setChecked(True)

        self.horizontalLayout_4.addWidget(self.radioButton_5)

        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setFont(font1)

        self.horizontalLayout_4.addWidget(self.comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setContentsMargins(10, -1, -1, -1)
        self.lineEdit_9 = QLineEdit(self.groupBox)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setFont(font1)
        self.lineEdit_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_9, 0, 4, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.lineEdit_10 = QLineEdit(self.groupBox)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setFont(font1)
        self.lineEdit_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_10, 1, 2, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font1)

        self.gridLayout.addWidget(self.label_10, 0, 3, 1, 1)

        self.lineEdit_2 = QLineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setFont(font1)
        self.lineEdit_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_2, 0, 2, 1, 1)

        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font1)

        self.gridLayout.addWidget(self.label_14, 1, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font1)

        self.gridLayout.addWidget(self.label_12, 1, 3, 1, 1)

        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)

        self.gridLayout.addWidget(self.label_13, 0, 1, 1, 1)

        self.lineEdit_11 = QLineEdit(self.groupBox)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setFont(font1)
        self.lineEdit_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_11, 1, 4, 1, 1)

        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font1)

        self.gridLayout.addWidget(self.label_15, 2, 0, 1, 1)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font1)

        self.gridLayout.addWidget(self.label_16, 2, 1, 1, 1)

        self.lineEdit_12 = QLineEdit(self.groupBox)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setFont(font1)
        self.lineEdit_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_12, 2, 2, 1, 1)

        self.label_17 = QLabel(self.groupBox)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font1)

        self.gridLayout.addWidget(self.label_17, 2, 3, 1, 1)

        self.lineEdit_13 = QLineEdit(self.groupBox)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        self.lineEdit_13.setFont(font1)
        self.lineEdit_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_13, 2, 4, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(PositionForm)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_3.setFont(font)
        self.groupBox_3.setStyleSheet(u"QGroupBox {\n"
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
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 12, -1, -1)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.radioButton_1 = QRadioButton(self.groupBox_3)
        self.radioButton_1.setObjectName(u"radioButton_1")
        self.radioButton_1.setFont(font1)
        self.radioButton_1.setChecked(True)

        self.horizontalLayout_5.addWidget(self.radioButton_1)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_7)

        self.lineEdit_5 = QLineEdit(self.groupBox_3)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_5.setFont(font1)
        self.lineEdit_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_5.addWidget(self.lineEdit_5)

        self.label_5 = QLabel(self.groupBox_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.horizontalLayout_5.addWidget(self.label_5)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.radioButton_2 = QRadioButton(self.groupBox_3)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setFont(font1)

        self.horizontalLayout_6.addWidget(self.radioButton_2)

        self.lineEdit_6 = QLineEdit(self.groupBox_3)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_6.setFont(font1)
        self.lineEdit_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.lineEdit_6)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.horizontalLayout_6.addWidget(self.label_6)

        self.horizontalLayout_6.setStretch(2, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.groupBox_3)

        QWidget.setTabOrder(self.radioButton, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.radioButton_4)
        QWidget.setTabOrder(self.radioButton_4, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.pushButton_2)
        QWidget.setTabOrder(self.pushButton_2, self.radioButton_5)
        QWidget.setTabOrder(self.radioButton_5, self.comboBox)
        QWidget.setTabOrder(self.comboBox, self.lineEdit_10)
        QWidget.setTabOrder(self.lineEdit_10, self.lineEdit_9)
        QWidget.setTabOrder(self.lineEdit_9, self.lineEdit_2)
        QWidget.setTabOrder(self.lineEdit_2, self.lineEdit_11)
        QWidget.setTabOrder(self.lineEdit_11, self.lineEdit_12)
        QWidget.setTabOrder(self.lineEdit_12, self.lineEdit_13)
        QWidget.setTabOrder(self.lineEdit_13, self.radioButton_1)
        QWidget.setTabOrder(self.radioButton_1, self.lineEdit_5)
        QWidget.setTabOrder(self.lineEdit_5, self.radioButton_2)
        QWidget.setTabOrder(self.radioButton_2, self.lineEdit_6)

        self.retranslateUi(PositionForm)

        QMetaObject.connectSlotsByName(PositionForm)
    # setupUi

    def retranslateUi(self, PositionForm):
        PositionForm.setWindowTitle(QCoreApplication.translate("PositionForm", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("PositionForm", u"< \ubc30\uce58 \uc601\uc5ed >", None))
        self.radioButton.setText(QCoreApplication.translate("PositionForm", u"STL", None))
        self.lineEdit.setText(QCoreApplication.translate("PositionForm", u"0", None))
        self.pushButton.setText(QCoreApplication.translate("PositionForm", u"\ud30c\uc77c \uc120\ud0dd", None))
        self.radioButton_4.setText(QCoreApplication.translate("PositionForm", u"\ubc00\uc9d1\ub3c4 \ud788\ud2b8\ub9f5", None))
        self.lineEdit_3.setText(QCoreApplication.translate("PositionForm", u"0", None))
        self.pushButton_2.setText(QCoreApplication.translate("PositionForm", u"\ud30c\uc77c \uc120\ud0dd", None))
        self.radioButton_5.setText(QCoreApplication.translate("PositionForm", u"\uae30\ubcf8 \ud615\uc0c1 :", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("PositionForm", u"\uc0ac\uac01\ud615", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("PositionForm", u"\uc6d0", None))

        self.lineEdit_9.setText(QCoreApplication.translate("PositionForm", u"0", None))
        self.label_11.setText(QCoreApplication.translate("PositionForm", u"- \ud68c\uc804 :", None))
        self.lineEdit_10.setText(QCoreApplication.translate("PositionForm", u"0", None))
        self.label_10.setText(QCoreApplication.translate("PositionForm", u"Y", None))
        self.lineEdit_2.setText(QCoreApplication.translate("PositionForm", u"0", None))
        self.label_14.setText(QCoreApplication.translate("PositionForm", u"X", None))
        self.label_9.setText(QCoreApplication.translate("PositionForm", u"- \uc704\uce58 :", None))
        self.label_12.setText(QCoreApplication.translate("PositionForm", u"Y", None))
        self.label_13.setText(QCoreApplication.translate("PositionForm", u"X", None))
        self.lineEdit_11.setText(QCoreApplication.translate("PositionForm", u"0", None))
        self.label_15.setText(QCoreApplication.translate("PositionForm", u"- \ud68c\uc804 :", None))
        self.label_16.setText(QCoreApplication.translate("PositionForm", u"X", None))
        self.lineEdit_12.setText(QCoreApplication.translate("PositionForm", u"0", None))
        self.label_17.setText(QCoreApplication.translate("PositionForm", u"Y", None))
        self.lineEdit_13.setText(QCoreApplication.translate("PositionForm", u"0", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("PositionForm", u"< \ubc30\uce58 \uc870\uac74 >", None))
        self.radioButton_1.setText("")
        self.label_7.setText(QCoreApplication.translate("PositionForm", u"\uc601\uc5ed \ub0b4", None))
        self.lineEdit_5.setText(QCoreApplication.translate("PositionForm", u"20", None))
        self.label_5.setText(QCoreApplication.translate("PositionForm", u"(m) \uac3c\uaca9\uc73c\ub85c \uade0\uc77c \ubc30\uce58", None))
        self.radioButton_2.setText("")
        self.lineEdit_6.setText(QCoreApplication.translate("PositionForm", u"10", None))
        self.label_6.setText(QCoreApplication.translate("PositionForm", u"\uba85 \ubc30\uce58", None))
    # retranslateUi

