# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'inlet.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_InletForm(object):
    def setupUi(self, InletForm):
        if not InletForm.objectName():
            InletForm.setObjectName(u"InletForm")
        InletForm.resize(300, 341)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InletForm.sizePolicy().hasHeightForWidth())
        InletForm.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        InletForm.setFont(font)
        self.verticalLayout = QVBoxLayout(InletForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.groupBox_4 = QGroupBox(InletForm)
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
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_16 = QLabel(self.groupBox_4)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_16)

        self.comboBox_name = QComboBox(self.groupBox_4)
        self.comboBox_name.setObjectName(u"comboBox_name")
        self.comboBox_name.setFont(font)
        self.comboBox_name.setEditable(True)
        self.comboBox_name.setMaxVisibleItems(10)

        self.horizontalLayout_11.addWidget(self.comboBox_name)

        self.horizontalLayout_11.setStretch(0, 2)
        self.horizontalLayout_11.setStretch(1, 3)

        self.verticalLayout_5.addLayout(self.horizontalLayout_11)

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

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(3)
        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.lineEdit_p2_y = QLineEdit(self.groupBox_4)
        self.lineEdit_p2_y.setObjectName(u"lineEdit_p2_y")
        self.lineEdit_p2_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p2_y.setFont(font)
        self.lineEdit_p2_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_p2_y, 1, 3, 1, 1)

        self.lineEdit_p2_x = QLineEdit(self.groupBox_4)
        self.lineEdit_p2_x.setObjectName(u"lineEdit_p2_x")
        self.lineEdit_p2_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p2_x.setFont(font)
        self.lineEdit_p2_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_p2_x, 1, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.lineEdit_p1_y = QLineEdit(self.groupBox_4)
        self.lineEdit_p1_y.setObjectName(u"lineEdit_p1_y")
        self.lineEdit_p1_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p1_y.setFont(font)
        self.lineEdit_p1_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_p1_y, 0, 3, 1, 1)

        self.label_12 = QLabel(self.groupBox_4)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1)

        self.lineEdit_p1_x = QLineEdit(self.groupBox_4)
        self.lineEdit_p1_x.setObjectName(u"lineEdit_p1_x")
        self.lineEdit_p1_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p1_x.setFont(font)
        self.lineEdit_p1_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_p1_x, 0, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 0, 2, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.horizontalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(-1, 0, -1, -1)
        self.label_21 = QLabel(self.groupBox_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_21)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, -1, -1, -1)
        self.lineEdit_vel_x = QLineEdit(self.groupBox_4)
        self.lineEdit_vel_x.setObjectName(u"lineEdit_vel_x")
        self.lineEdit_vel_x.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_vel_x.setFont(font)
        self.lineEdit_vel_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_17.addWidget(self.lineEdit_vel_x)

        self.lineEdit_vel_y = QLineEdit(self.groupBox_4)
        self.lineEdit_vel_y.setObjectName(u"lineEdit_vel_y")
        self.lineEdit_vel_y.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_vel_y.setFont(font)
        self.lineEdit_vel_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_17.addWidget(self.lineEdit_vel_y)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_17)

        self.label_15 = QLabel(self.groupBox_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_15)

        self.lineEdit_dx = QLineEdit(self.groupBox_4)
        self.lineEdit_dx.setObjectName(u"lineEdit_dx")
        self.lineEdit_dx.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_dx.setFont(font)
        self.lineEdit_dx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEdit_dx)

        self.label_13 = QLabel(self.groupBox_4)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_13)

        self.lineEdit_interval = QLineEdit(self.groupBox_4)
        self.lineEdit_interval.setObjectName(u"lineEdit_interval")
        self.lineEdit_interval.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_interval.setFont(font)
        self.lineEdit_interval.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEdit_interval)

        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_14)

        self.lineEdit_material_index = QLineEdit(self.groupBox_4)
        self.lineEdit_material_index.setObjectName(u"lineEdit_material_index")
        self.lineEdit_material_index.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_material_index.setFont(font)
        self.lineEdit_material_index.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lineEdit_material_index)

        self.label_17 = QLabel(self.groupBox_4)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_17)

        self.lineEdit_grid = QLineEdit(self.groupBox_4)
        self.lineEdit_grid.setObjectName(u"lineEdit_grid")
        self.lineEdit_grid.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_grid.setFont(font)
        self.lineEdit_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.lineEdit_grid)

        self.label_18 = QLabel(self.groupBox_4)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_18)

        self.lineEdit_outlet_index = QLineEdit(self.groupBox_4)
        self.lineEdit_outlet_index.setObjectName(u"lineEdit_outlet_index")
        self.lineEdit_outlet_index.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_outlet_index.setFont(font)
        self.lineEdit_outlet_index.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.lineEdit_outlet_index)


        self.verticalLayout_5.addLayout(self.formLayout)


        self.verticalLayout.addWidget(self.groupBox_4)

        QWidget.setTabOrder(self.comboBox_name, self.pushButton_add)
        QWidget.setTabOrder(self.pushButton_add, self.pushButton_save)
        QWidget.setTabOrder(self.pushButton_save, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.lineEdit_p1_x)
        QWidget.setTabOrder(self.lineEdit_p1_x, self.lineEdit_p1_y)
        QWidget.setTabOrder(self.lineEdit_p1_y, self.lineEdit_p2_x)
        QWidget.setTabOrder(self.lineEdit_p2_x, self.lineEdit_p2_y)
        QWidget.setTabOrder(self.lineEdit_p2_y, self.lineEdit_vel_x)
        QWidget.setTabOrder(self.lineEdit_vel_x, self.lineEdit_vel_y)

        self.retranslateUi(InletForm)

        QMetaObject.connectSlotsByName(InletForm)
    # setupUi

    def retranslateUi(self, InletForm):
        InletForm.setWindowTitle(QCoreApplication.translate("InletForm", u"Form", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("InletForm", u"< Inlet Properties >", None))
        self.label_16.setText(QCoreApplication.translate("InletForm", u"Type:", None))
        self.pushButton_add.setText(QCoreApplication.translate("InletForm", u"\ucd94\uac00", None))
        self.pushButton_save.setText(QCoreApplication.translate("InletForm", u"\uc800\uc7a5", None))
        self.pushButton_remove.setText(QCoreApplication.translate("InletForm", u"\uc0ad\uc81c", None))
        self.label_11.setText(QCoreApplication.translate("InletForm", u"\uc885\ub8cc X :", None))
        self.lineEdit_p2_y.setText(QCoreApplication.translate("InletForm", u"0.0", None))
        self.lineEdit_p2_x.setText(QCoreApplication.translate("InletForm", u"0.0", None))
        self.label_9.setText(QCoreApplication.translate("InletForm", u"\uc2dc\uc791 X :", None))
        self.lineEdit_p1_y.setText(QCoreApplication.translate("InletForm", u"0.0", None))
        self.label_12.setText(QCoreApplication.translate("InletForm", u"\uc885\ub8cc Y :", None))
        self.lineEdit_p1_x.setText(QCoreApplication.translate("InletForm", u"0.0", None))
        self.label_10.setText(QCoreApplication.translate("InletForm", u"\uc2dc\uc791 Y :", None))
        self.label_21.setText(QCoreApplication.translate("InletForm", u"Velocity :", None))
        self.lineEdit_vel_x.setText(QCoreApplication.translate("InletForm", u"1.4", None))
        self.lineEdit_vel_y.setText(QCoreApplication.translate("InletForm", u"0.0", None))
        self.label_15.setText(QCoreApplication.translate("InletForm", u"dx :", None))
        self.lineEdit_dx.setText(QCoreApplication.translate("InletForm", u"1", None))
        self.label_13.setText(QCoreApplication.translate("InletForm", u"interval :", None))
        self.lineEdit_interval.setText(QCoreApplication.translate("InletForm", u"100", None))
        self.label_14.setText(QCoreApplication.translate("InletForm", u"material_index :", None))
        self.lineEdit_material_index.setText(QCoreApplication.translate("InletForm", u"1", None))
        self.label_17.setText(QCoreApplication.translate("InletForm", u"grid :", None))
        self.lineEdit_grid.setText(QCoreApplication.translate("InletForm", u"1", None))
        self.label_18.setText(QCoreApplication.translate("InletForm", u"outlet_index :", None))
        self.lineEdit_outlet_index.setText(QCoreApplication.translate("InletForm", u"0", None))
    # retranslateUi

