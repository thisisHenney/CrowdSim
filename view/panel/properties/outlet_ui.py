# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'outlet.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_OutletForm(object):
    def setupUi(self, OutletForm):
        if not OutletForm.objectName():
            OutletForm.setObjectName(u"OutletForm")
        OutletForm.resize(300, 199)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(OutletForm.sizePolicy().hasHeightForWidth())
        OutletForm.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        OutletForm.setFont(font)
        self.verticalLayout = QVBoxLayout(OutletForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.groupBox_4 = QGroupBox(OutletForm)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(9)
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
        self.verticalLayout_5.setContentsMargins(9, 12, 9, -1)
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_21 = QLabel(self.groupBox_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font)

        self.horizontalLayout_15.addWidget(self.label_21)

        self.comboBox_name = QComboBox(self.groupBox_4)
        self.comboBox_name.setObjectName(u"comboBox_name")
        self.comboBox_name.setFont(font)
        self.comboBox_name.setEditable(True)
        self.comboBox_name.setMaxVisibleItems(10)

        self.horizontalLayout_15.addWidget(self.comboBox_name)

        self.horizontalLayout_15.setStretch(0, 2)
        self.horizontalLayout_15.setStretch(1, 3)

        self.verticalLayout_5.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_3)

        self.pushButton_add = QPushButton(self.groupBox_4)
        self.pushButton_add.setObjectName(u"pushButton_add")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy1)
        self.pushButton_add.setMaximumSize(QSize(60, 16777215))
        self.pushButton_add.setFont(font)

        self.horizontalLayout_12.addWidget(self.pushButton_add)

        self.pushButton_save = QPushButton(self.groupBox_4)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setMaximumSize(QSize(60, 16777215))
        self.pushButton_save.setFont(font)

        self.horizontalLayout_12.addWidget(self.pushButton_save)

        self.pushButton_remove = QPushButton(self.groupBox_4)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMaximumSize(QSize(60, 16777215))
        self.pushButton_remove.setFont(font)

        self.horizontalLayout_12.addWidget(self.pushButton_remove)

        self.horizontalLayout_12.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_12)

        self.line_3 = QFrame(self.groupBox_4)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFont(font)
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radioButton_point = QRadioButton(self.groupBox_4)
        self.radioButton_point.setObjectName(u"radioButton_point")
        font2 = QFont()
        font2.setPointSize(8)
        self.radioButton_point.setFont(font2)
        self.radioButton_point.setChecked(True)

        self.horizontalLayout_7.addWidget(self.radioButton_point)

        self.widget = QWidget(self.groupBox_4)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_16 = QHBoxLayout(self.widget)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_19 = QLabel(self.widget)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font)

        self.horizontalLayout_16.addWidget(self.label_19)

        self.lineEdit_p_x = QLineEdit(self.widget)
        self.lineEdit_p_x.setObjectName(u"lineEdit_p_x")
        self.lineEdit_p_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p_x.setFont(font)
        self.lineEdit_p_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_16.addWidget(self.lineEdit_p_x)

        self.label_14 = QLabel(self.widget)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)

        self.horizontalLayout_16.addWidget(self.label_14)

        self.lineEdit_p_y = QLineEdit(self.widget)
        self.lineEdit_p_y.setObjectName(u"lineEdit_p_y")
        self.lineEdit_p_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p_y.setFont(font)
        self.lineEdit_p_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_16.addWidget(self.lineEdit_p_y)


        self.horizontalLayout_7.addWidget(self.widget)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.radioButton_line = QRadioButton(self.groupBox_4)
        self.radioButton_line.setObjectName(u"radioButton_line")
        self.radioButton_line.setFont(font)

        self.horizontalLayout_8.addWidget(self.radioButton_line)

        self.line_2 = QFrame(self.groupBox_4)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_8.addWidget(self.line_2)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(3)
        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.gridLayout_2.addWidget(self.label_13, 0, 2, 1, 1)

        self.label_15 = QLabel(self.groupBox_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.gridLayout_2.addWidget(self.label_15, 2, 0, 1, 1)

        self.label_17 = QLabel(self.groupBox_4)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)

        self.gridLayout_2.addWidget(self.label_17, 0, 0, 1, 1)

        self.lineEdit_p2_x = QLineEdit(self.groupBox_4)
        self.lineEdit_p2_x.setObjectName(u"lineEdit_p2_x")
        self.lineEdit_p2_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p2_x.setFont(font)
        self.lineEdit_p2_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_p2_x, 2, 1, 1, 1)

        self.label_18 = QLabel(self.groupBox_4)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.gridLayout_2.addWidget(self.label_18, 2, 2, 1, 1)

        self.lineEdit_p1_x = QLineEdit(self.groupBox_4)
        self.lineEdit_p1_x.setObjectName(u"lineEdit_p1_x")
        self.lineEdit_p1_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p1_x.setFont(font)
        self.lineEdit_p1_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_p1_x, 0, 1, 1, 1)

        self.lineEdit_p2_y = QLineEdit(self.groupBox_4)
        self.lineEdit_p2_y.setObjectName(u"lineEdit_p2_y")
        self.lineEdit_p2_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p2_y.setFont(font)
        self.lineEdit_p2_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_p2_y, 2, 3, 1, 1)

        self.lineEdit_p1_y = QLineEdit(self.groupBox_4)
        self.lineEdit_p1_y.setObjectName(u"lineEdit_p1_y")
        self.lineEdit_p1_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p1_y.setFont(font)
        self.lineEdit_p1_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_p1_y, 0, 3, 1, 1)


        self.horizontalLayout_8.addLayout(self.gridLayout_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)


        self.verticalLayout.addWidget(self.groupBox_4)

        QWidget.setTabOrder(self.pushButton_add, self.pushButton_save)
        QWidget.setTabOrder(self.pushButton_save, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.radioButton_point)
        QWidget.setTabOrder(self.radioButton_point, self.lineEdit_p_x)
        QWidget.setTabOrder(self.lineEdit_p_x, self.lineEdit_p_y)
        QWidget.setTabOrder(self.lineEdit_p_y, self.radioButton_line)
        QWidget.setTabOrder(self.radioButton_line, self.lineEdit_p1_x)
        QWidget.setTabOrder(self.lineEdit_p1_x, self.lineEdit_p1_y)
        QWidget.setTabOrder(self.lineEdit_p1_y, self.lineEdit_p2_x)
        QWidget.setTabOrder(self.lineEdit_p2_x, self.lineEdit_p2_y)

        self.retranslateUi(OutletForm)

        QMetaObject.connectSlotsByName(OutletForm)
    # setupUi

    def retranslateUi(self, OutletForm):
        OutletForm.setWindowTitle(QCoreApplication.translate("OutletForm", u"Form", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("OutletForm", u"< Outlet Properties >", None))
        self.label_21.setText(QCoreApplication.translate("OutletForm", u"Name :", None))
        self.pushButton_add.setText(QCoreApplication.translate("OutletForm", u"\ucd94\uac00", None))
        self.pushButton_save.setText(QCoreApplication.translate("OutletForm", u"\uc800\uc7a5", None))
        self.pushButton_remove.setText(QCoreApplication.translate("OutletForm", u"\uc0ad\uc81c", None))
        self.radioButton_point.setText(QCoreApplication.translate("OutletForm", u"\uc810 :", None))
        self.label_19.setText(QCoreApplication.translate("OutletForm", u"\uc2dc\uc791 X :", None))
        self.lineEdit_p_x.setText(QCoreApplication.translate("OutletForm", u"0", None))
        self.label_14.setText(QCoreApplication.translate("OutletForm", u"\uc2dc\uc791 Y :", None))
        self.lineEdit_p_y.setText(QCoreApplication.translate("OutletForm", u"0", None))
        self.radioButton_line.setText(QCoreApplication.translate("OutletForm", u"\uc120 :", None))
        self.label_13.setText(QCoreApplication.translate("OutletForm", u"\uc2dc\uc791 Y :", None))
        self.label_15.setText(QCoreApplication.translate("OutletForm", u"\uc885\ub8cc X :", None))
        self.label_17.setText(QCoreApplication.translate("OutletForm", u"\uc2dc\uc791 X :", None))
        self.lineEdit_p2_x.setText(QCoreApplication.translate("OutletForm", u"0", None))
        self.label_18.setText(QCoreApplication.translate("OutletForm", u"\uc885\ub8cc Y :", None))
        self.lineEdit_p1_x.setText(QCoreApplication.translate("OutletForm", u"0", None))
        self.lineEdit_p2_y.setText(QCoreApplication.translate("OutletForm", u"0", None))
        self.lineEdit_p1_y.setText(QCoreApplication.translate("OutletForm", u"0", None))
    # retranslateUi

