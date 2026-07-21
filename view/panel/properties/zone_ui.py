# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'zone.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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

class Ui_ZoneForm(object):
    def setupUi(self, ZoneForm):
        if not ZoneForm.objectName():
            ZoneForm.setObjectName(u"ZoneForm")
        ZoneForm.resize(300, 420)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ZoneForm.sizePolicy().hasHeightForWidth())
        ZoneForm.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        ZoneForm.setFont(font)
        self.verticalLayout = QVBoxLayout(ZoneForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.groupBox_4 = QGroupBox(ZoneForm)
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
"	padding: 3;\n"
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
        self.label_9 = QLabel(self.groupBox_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

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

        self.lineEdit_p1_y = QLineEdit(self.groupBox_4)
        self.lineEdit_p1_y.setObjectName(u"lineEdit_p1_y")
        self.lineEdit_p1_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p1_y.setFont(font)
        self.lineEdit_p1_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_p1_y, 0, 3, 1, 1)

        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font)

        self.gridLayout.addWidget(self.label_11, 1, 0, 1, 1)

        self.lineEdit_p2_x = QLineEdit(self.groupBox_4)
        self.lineEdit_p2_x.setObjectName(u"lineEdit_p2_x")
        self.lineEdit_p2_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p2_x.setFont(font)
        self.lineEdit_p2_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_p2_x, 1, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox_4)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font)

        self.gridLayout.addWidget(self.label_12, 1, 2, 1, 1)

        self.lineEdit_p2_y = QLineEdit(self.groupBox_4)
        self.lineEdit_p2_y.setObjectName(u"lineEdit_p2_y")
        self.lineEdit_p2_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_p2_y.setFont(font)
        self.lineEdit_p2_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_p2_y, 1, 3, 1, 1)

        self.label_22 = QLabel(self.groupBox_4)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font)

        self.gridLayout.addWidget(self.label_22, 2, 0, 1, 1)

        self.lineEdit_direction_x = QLineEdit(self.groupBox_4)
        self.lineEdit_direction_x.setObjectName(u"lineEdit_direction_x")
        self.lineEdit_direction_x.setEnabled(False)
        self.lineEdit_direction_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_direction_x.setFont(font)
        self.lineEdit_direction_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_direction_x, 2, 1, 1, 1)

        self.label_23 = QLabel(self.groupBox_4)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font)

        self.gridLayout.addWidget(self.label_23, 2, 2, 1, 1)

        self.lineEdit_direction_y = QLineEdit(self.groupBox_4)
        self.lineEdit_direction_y.setObjectName(u"lineEdit_direction_y")
        self.lineEdit_direction_y.setEnabled(False)
        self.lineEdit_direction_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_direction_y.setFont(font)
        self.lineEdit_direction_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_direction_y, 2, 3, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(3, 1)

        self.horizontalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(-1, 0, -1, -1)
        self.label_24 = QLabel(self.groupBox_4)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_24)

        self.lineEdit_length = QLineEdit(self.groupBox_4)
        self.lineEdit_length.setObjectName(u"lineEdit_length")
        self.lineEdit_length.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_length.setFont(font)
        self.lineEdit_length.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEdit_length)

        self.label_25 = QLabel(self.groupBox_4)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_25)

        self.comboBox_zone_type = QComboBox(self.groupBox_4)
        self.comboBox_zone_type.addItem("")
        self.comboBox_zone_type.addItem("")
        self.comboBox_zone_type.setObjectName(u"comboBox_zone_type")
        self.comboBox_zone_type.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboBox_zone_type)

        self.label_26 = QLabel(self.groupBox_4)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_26)

        self.lineEdit_k_avo = QLineEdit(self.groupBox_4)
        self.lineEdit_k_avo.setObjectName(u"lineEdit_k_avo")
        self.lineEdit_k_avo.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_k_avo.setFont(font)
        self.lineEdit_k_avo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEdit_k_avo)

        self.label_27 = QLabel(self.groupBox_4)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_27)

        self.lineEdit_avoid_radius = QLineEdit(self.groupBox_4)
        self.lineEdit_avoid_radius.setObjectName(u"lineEdit_avoid_radius")
        self.lineEdit_avoid_radius.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_avoid_radius.setFont(font)
        self.lineEdit_avoid_radius.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lineEdit_avoid_radius)

        self.label_28 = QLabel(self.groupBox_4)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_28)

        self.lineEdit_outlet_id = QLineEdit(self.groupBox_4)
        self.lineEdit_outlet_id.setObjectName(u"lineEdit_outlet_id")
        self.lineEdit_outlet_id.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_outlet_id.setFont(font)
        self.lineEdit_outlet_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.lineEdit_outlet_id)

        self.label_29 = QLabel(self.groupBox_4)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_29)

        self.lineEdit_grid = QLineEdit(self.groupBox_4)
        self.lineEdit_grid.setObjectName(u"lineEdit_grid")
        self.lineEdit_grid.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_grid.setFont(font)
        self.lineEdit_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.lineEdit_grid)


        self.verticalLayout_5.addLayout(self.formLayout)


        self.verticalLayout.addWidget(self.groupBox_4)

        QWidget.setTabOrder(self.comboBox_name, self.pushButton_add)
        QWidget.setTabOrder(self.pushButton_add, self.pushButton_save)
        QWidget.setTabOrder(self.pushButton_save, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.lineEdit_p1_x)
        QWidget.setTabOrder(self.lineEdit_p1_x, self.lineEdit_p1_y)
        QWidget.setTabOrder(self.lineEdit_p1_y, self.lineEdit_p2_x)
        QWidget.setTabOrder(self.lineEdit_p2_x, self.lineEdit_p2_y)
        QWidget.setTabOrder(self.lineEdit_p2_y, self.lineEdit_direction_x)
        QWidget.setTabOrder(self.lineEdit_direction_x, self.lineEdit_direction_y)
        QWidget.setTabOrder(self.lineEdit_direction_y, self.lineEdit_length)
        QWidget.setTabOrder(self.lineEdit_length, self.comboBox_zone_type)
        QWidget.setTabOrder(self.comboBox_zone_type, self.lineEdit_k_avo)
        QWidget.setTabOrder(self.lineEdit_k_avo, self.lineEdit_avoid_radius)
        QWidget.setTabOrder(self.lineEdit_avoid_radius, self.lineEdit_outlet_id)
        QWidget.setTabOrder(self.lineEdit_outlet_id, self.lineEdit_grid)

        self.retranslateUi(ZoneForm)

        QMetaObject.connectSlotsByName(ZoneForm)
    # setupUi

    def retranslateUi(self, ZoneForm):
        ZoneForm.setWindowTitle(QCoreApplication.translate("ZoneForm", u"Form", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ZoneForm", u"< Zone Properties >", None))
        self.label_16.setText(QCoreApplication.translate("ZoneForm", u"Comment :", None))
        self.pushButton_add.setText(QCoreApplication.translate("ZoneForm", u"\ucd94\uac00", None))
        self.pushButton_save.setText(QCoreApplication.translate("ZoneForm", u"\uc800\uc7a5", None))
        self.pushButton_remove.setText(QCoreApplication.translate("ZoneForm", u"\uc0ad\uc81c", None))
        self.label_9.setText(QCoreApplication.translate("ZoneForm", u"p1 X :", None))
        self.lineEdit_p1_x.setText(QCoreApplication.translate("ZoneForm", u"0.0", None))
        self.label_10.setText(QCoreApplication.translate("ZoneForm", u"p1 Y :", None))
        self.lineEdit_p1_y.setText(QCoreApplication.translate("ZoneForm", u"0.0", None))
        self.label_11.setText(QCoreApplication.translate("ZoneForm", u"p2 X :", None))
        self.lineEdit_p2_x.setText(QCoreApplication.translate("ZoneForm", u"0.0", None))
        self.label_12.setText(QCoreApplication.translate("ZoneForm", u"p2 Y :", None))
        self.lineEdit_p2_y.setText(QCoreApplication.translate("ZoneForm", u"0.0", None))
        self.label_22.setText(QCoreApplication.translate("ZoneForm", u"Dir X :", None))
        self.lineEdit_direction_x.setText(QCoreApplication.translate("ZoneForm", u"0", None))
        self.label_23.setText(QCoreApplication.translate("ZoneForm", u"Dir Y :", None))
        self.lineEdit_direction_y.setText(QCoreApplication.translate("ZoneForm", u"1", None))
        self.label_24.setText(QCoreApplication.translate("ZoneForm", u"length :", None))
        self.lineEdit_length.setText(QCoreApplication.translate("ZoneForm", u"1.0", None))
        self.label_25.setText(QCoreApplication.translate("ZoneForm", u"zone_type :", None))
        self.comboBox_zone_type.setItemText(0, QCoreApplication.translate("ZoneForm", u"avoid_zone", None))
        self.comboBox_zone_type.setItemText(1, QCoreApplication.translate("ZoneForm", u"change_goal_position", None))

        self.label_26.setText(QCoreApplication.translate("ZoneForm", u"K_avo :", None))
        self.lineEdit_k_avo.setText(QCoreApplication.translate("ZoneForm", u"200.0", None))
        self.label_27.setText(QCoreApplication.translate("ZoneForm", u"avoid_radius :", None))
        self.lineEdit_avoid_radius.setText(QCoreApplication.translate("ZoneForm", u"15.0", None))
        self.label_28.setText(QCoreApplication.translate("ZoneForm", u"outlet_id :", None))
        self.lineEdit_outlet_id.setText(QCoreApplication.translate("ZoneForm", u"0", None))
        self.label_29.setText(QCoreApplication.translate("ZoneForm", u"grid :", None))
        self.lineEdit_grid.setText(QCoreApplication.translate("ZoneForm", u"1", None))
    # retranslateUi

