# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'particle.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_ParticleForm(object):
    def setupUi(self, ParticleForm):
        if not ParticleForm.objectName():
            ParticleForm.setObjectName(u"ParticleForm")
        ParticleForm.resize(300, 671)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ParticleForm.sizePolicy().hasHeightForWidth())
        ParticleForm.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        ParticleForm.setFont(font)
        self.verticalLayout = QVBoxLayout(ParticleForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.groupBox = QGroupBox(ParticleForm)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(True)
        self.groupBox.setFont(font1)
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
        self.verticalLayout_2.setContentsMargins(9, 12, 9, -1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_16)

        self.comboBox_name = QComboBox(self.groupBox)
        self.comboBox_name.setObjectName(u"comboBox_name")
        self.comboBox_name.setFont(font)
        self.comboBox_name.setEditable(True)
        self.comboBox_name.setMaxVisibleItems(10)

        self.horizontalLayout_11.addWidget(self.comboBox_name)

        self.horizontalLayout_11.setStretch(0, 2)
        self.horizontalLayout_11.setStretch(1, 3)

        self.verticalLayout_2.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_3)

        self.pushButton_add = QPushButton(self.groupBox)
        self.pushButton_add.setObjectName(u"pushButton_add")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy1)
        self.pushButton_add.setMaximumSize(QSize(60, 16777215))
        self.pushButton_add.setFont(font)

        self.horizontalLayout_12.addWidget(self.pushButton_add)

        self.pushButton_save = QPushButton(self.groupBox)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setMaximumSize(QSize(60, 16777215))
        self.pushButton_save.setFont(font)

        self.horizontalLayout_12.addWidget(self.pushButton_save)

        self.pushButton_remove = QPushButton(self.groupBox)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMaximumSize(QSize(60, 16777215))
        self.pushButton_remove.setFont(font)

        self.horizontalLayout_12.addWidget(self.pushButton_remove)

        self.horizontalLayout_12.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_12)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.groupBox_4 = QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMaximumSize(QSize(16777215, 16777215))
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
        self.checkBox_two_dimensional = QCheckBox(self.groupBox_4)
        self.checkBox_two_dimensional.setObjectName(u"checkBox_two_dimensional")
        self.checkBox_two_dimensional.setFont(font)
        self.checkBox_two_dimensional.setChecked(True)

        self.verticalLayout_5.addWidget(self.checkBox_two_dimensional)

        self.checkBox_domain_general = QCheckBox(self.groupBox_4)
        self.checkBox_domain_general.setObjectName(u"checkBox_domain_general")
        self.checkBox_domain_general.setFont(font)
        self.checkBox_domain_general.setChecked(True)

        self.verticalLayout_5.addWidget(self.checkBox_domain_general)

        self.checkBox_pwb = QCheckBox(self.groupBox_4)
        self.checkBox_pwb.setObjectName(u"checkBox_pwb")
        self.checkBox_pwb.setFont(font)
        self.checkBox_pwb.setChecked(True)

        self.verticalLayout_5.addWidget(self.checkBox_pwb)

        self.groupBox_path_field = QGroupBox(self.groupBox_4)
        self.groupBox_path_field.setObjectName(u"groupBox_path_field")
        self.groupBox_path_field.setCheckable(True)
        self.groupBox_path_field.setChecked(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_path_field)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.checkBox_is_manhattan = QCheckBox(self.groupBox_path_field)
        self.checkBox_is_manhattan.setObjectName(u"checkBox_is_manhattan")
        self.checkBox_is_manhattan.setFont(font)
        self.checkBox_is_manhattan.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_is_manhattan, 0, 0, 1, 1)


        self.verticalLayout_5.addWidget(self.groupBox_path_field)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_15 = QLabel(self.groupBox_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_15)

        self.lineEdit_grid = QLineEdit(self.groupBox_4)
        self.lineEdit_grid.setObjectName(u"lineEdit_grid")
        self.lineEdit_grid.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_grid.setFont(font)
        self.lineEdit_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.lineEdit_grid)

        self.horizontalLayout_10.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_10)


        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_3.setFont(font1)
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
        self.verticalLayout_4.setContentsMargins(9, 12, 9, -1)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_14 = QLabel(self.groupBox_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_14)

        self.lineEdit_base_dx = QLineEdit(self.groupBox_3)
        self.lineEdit_base_dx.setObjectName(u"lineEdit_base_dx")
        self.lineEdit_base_dx.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_base_dx.setFont(font)
        self.lineEdit_base_dx.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.lineEdit_base_dx)

        self.horizontalLayout_8.setStretch(0, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_25 = QLabel(self.groupBox_3)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_25)

        self.line_2 = QFrame(self.groupBox_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_6.addWidget(self.line_2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(3)
        self.label_26 = QLabel(self.groupBox_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_26, 0, 0, 1, 1)

        self.lineEdit_region_min_y = QLineEdit(self.groupBox_3)
        self.lineEdit_region_min_y.setObjectName(u"lineEdit_region_min_y")
        self.lineEdit_region_min_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_region_min_y.setFont(font)
        self.lineEdit_region_min_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_region_min_y, 0, 2, 1, 1)

        self.label_27 = QLabel(self.groupBox_3)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font)
        self.label_27.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_27, 1, 0, 1, 1)

        self.lineEdit_region_max_y = QLineEdit(self.groupBox_3)
        self.lineEdit_region_max_y.setObjectName(u"lineEdit_region_max_y")
        self.lineEdit_region_max_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_region_max_y.setFont(font)
        self.lineEdit_region_max_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_region_max_y, 1, 2, 1, 1)

        self.lineEdit_region_max_x = QLineEdit(self.groupBox_3)
        self.lineEdit_region_max_x.setObjectName(u"lineEdit_region_max_x")
        self.lineEdit_region_max_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_region_max_x.setFont(font)
        self.lineEdit_region_max_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_region_max_x, 1, 1, 1, 1)

        self.lineEdit_region_min_x = QLineEdit(self.groupBox_3)
        self.lineEdit_region_min_x.setObjectName(u"lineEdit_region_min_x")
        self.lineEdit_region_min_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_region_min_x.setFont(font)
        self.lineEdit_region_min_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_region_min_x, 0, 1, 1, 1)


        self.horizontalLayout_6.addLayout(self.gridLayout_3)

        self.horizontalLayout_6.setStretch(0, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.groupBox)
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
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)

        self.horizontalLayout_13.addWidget(self.label_17)

        self.comboBox_segment_name = QComboBox(self.groupBox_2)
        self.comboBox_segment_name.setObjectName(u"comboBox_segment_name")
        self.comboBox_segment_name.setEnabled(False)
        self.comboBox_segment_name.setFont(font)
        self.comboBox_segment_name.setEditable(True)
        self.comboBox_segment_name.setMaxVisibleItems(10)

        self.horizontalLayout_13.addWidget(self.comboBox_segment_name)

        self.horizontalLayout_13.setStretch(0, 2)
        self.horizontalLayout_13.setStretch(1, 3)

        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, -1, -1)
        self.horizontalSpacer_4 = QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_4)

        self.pushButton_segment_add = QPushButton(self.groupBox_2)
        self.pushButton_segment_add.setObjectName(u"pushButton_segment_add")
        sizePolicy1.setHeightForWidth(self.pushButton_segment_add.sizePolicy().hasHeightForWidth())
        self.pushButton_segment_add.setSizePolicy(sizePolicy1)
        self.pushButton_segment_add.setMaximumSize(QSize(60, 16777215))
        self.pushButton_segment_add.setFont(font)

        self.horizontalLayout_14.addWidget(self.pushButton_segment_add)

        self.pushButton_segment_save = QPushButton(self.groupBox_2)
        self.pushButton_segment_save.setObjectName(u"pushButton_segment_save")
        self.pushButton_segment_save.setMaximumSize(QSize(60, 16777215))
        self.pushButton_segment_save.setFont(font)

        self.horizontalLayout_14.addWidget(self.pushButton_segment_save)

        self.pushButton_segment_remove = QPushButton(self.groupBox_2)
        self.pushButton_segment_remove.setObjectName(u"pushButton_segment_remove")
        self.pushButton_segment_remove.setMaximumSize(QSize(60, 16777215))
        self.pushButton_segment_remove.setFont(font)

        self.horizontalLayout_14.addWidget(self.pushButton_segment_remove)

        self.horizontalLayout_14.setStretch(0, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_14)

        self.line_3 = QFrame(self.groupBox_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFont(font)
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.checkBox_interval_normal = QCheckBox(self.groupBox_2)
        self.checkBox_interval_normal.setObjectName(u"checkBox_interval_normal")
        self.checkBox_interval_normal.setFont(font)

        self.verticalLayout_3.addWidget(self.checkBox_interval_normal)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_5.addWidget(self.label_5)

        self.lineEdit_segment_mesh_path = QLineEdit(self.groupBox_2)
        self.lineEdit_segment_mesh_path.setObjectName(u"lineEdit_segment_mesh_path")
        self.lineEdit_segment_mesh_path.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_segment_mesh_path.setFont(font)
        self.lineEdit_segment_mesh_path.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.lineEdit_segment_mesh_path)

        self.pushButton_mesh_select = QPushButton(self.groupBox_2)
        self.pushButton_mesh_select.setObjectName(u"pushButton_mesh_select")
        self.pushButton_mesh_select.setMaximumSize(QSize(72, 16777215))
        self.pushButton_mesh_select.setFont(font)

        self.horizontalLayout_5.addWidget(self.pushButton_mesh_select)

        self.horizontalLayout_5.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_6)

        self.comboBox_segment_material = QComboBox(self.groupBox_2)
        self.comboBox_segment_material.addItem("")
        self.comboBox_segment_material.addItem("")
        self.comboBox_segment_material.setObjectName(u"comboBox_segment_material")

        self.horizontalLayout_7.addWidget(self.comboBox_segment_material)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_9.addWidget(self.label_7)

        self.comboBox_segment_region_type = QComboBox(self.groupBox_2)
        self.comboBox_segment_region_type.addItem("")
        self.comboBox_segment_region_type.addItem("")
        self.comboBox_segment_region_type.setObjectName(u"comboBox_segment_region_type")

        self.horizontalLayout_9.addWidget(self.comboBox_segment_region_type)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_9)


        self.verticalLayout_2.addWidget(self.groupBox_2)


        self.verticalLayout.addWidget(self.groupBox)

        QWidget.setTabOrder(self.comboBox_name, self.pushButton_add)
        QWidget.setTabOrder(self.pushButton_add, self.pushButton_save)
        QWidget.setTabOrder(self.pushButton_save, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.checkBox_two_dimensional)
        QWidget.setTabOrder(self.checkBox_two_dimensional, self.checkBox_domain_general)
        QWidget.setTabOrder(self.checkBox_domain_general, self.lineEdit_grid)
        QWidget.setTabOrder(self.lineEdit_grid, self.lineEdit_base_dx)
        QWidget.setTabOrder(self.lineEdit_base_dx, self.lineEdit_region_min_x)
        QWidget.setTabOrder(self.lineEdit_region_min_x, self.lineEdit_region_min_y)
        QWidget.setTabOrder(self.lineEdit_region_min_y, self.lineEdit_region_max_x)
        QWidget.setTabOrder(self.lineEdit_region_max_x, self.lineEdit_region_max_y)
        QWidget.setTabOrder(self.lineEdit_region_max_y, self.lineEdit_segment_mesh_path)
        QWidget.setTabOrder(self.lineEdit_segment_mesh_path, self.pushButton_mesh_select)

        self.retranslateUi(ParticleForm)

        QMetaObject.connectSlotsByName(ParticleForm)
    # setupUi

    def retranslateUi(self, ParticleForm):
        ParticleForm.setWindowTitle(QCoreApplication.translate("ParticleForm", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("ParticleForm", u"< Particle Properties >", None))
        self.label_16.setText(QCoreApplication.translate("ParticleForm", u"\uc774\ub984 :", None))
        self.pushButton_add.setText(QCoreApplication.translate("ParticleForm", u"\ucd94\uac00", None))
        self.pushButton_save.setText(QCoreApplication.translate("ParticleForm", u"\uc800\uc7a5", None))
        self.pushButton_remove.setText(QCoreApplication.translate("ParticleForm", u"\uc0ad\uc81c", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ParticleForm", u"< Common >", None))
        self.checkBox_two_dimensional.setText(QCoreApplication.translate("ParticleForm", u"two_dimensional", None))
        self.checkBox_domain_general.setText(QCoreApplication.translate("ParticleForm", u"domain_general", None))
        self.checkBox_pwb.setText(QCoreApplication.translate("ParticleForm", u"pwb", None))
        self.groupBox_path_field.setTitle(QCoreApplication.translate("ParticleForm", u"path_field", None))
        self.checkBox_is_manhattan.setText(QCoreApplication.translate("ParticleForm", u"is_manhattan", None))
        self.label_15.setText(QCoreApplication.translate("ParticleForm", u"Grid :", None))
        self.lineEdit_grid.setText(QCoreApplication.translate("ParticleForm", u"0", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("ParticleForm", u"< Base >", None))
        self.label_14.setText(QCoreApplication.translate("ParticleForm", u"base_dx :", None))
        self.lineEdit_base_dx.setText(QCoreApplication.translate("ParticleForm", u"0.4", None))
        self.label_25.setText(QCoreApplication.translate("ParticleForm", u"Region", None))
        self.label_26.setText(QCoreApplication.translate("ParticleForm", u"min :", None))
        self.lineEdit_region_min_y.setText(QCoreApplication.translate("ParticleForm", u"-12", None))
        self.label_27.setText(QCoreApplication.translate("ParticleForm", u"max :", None))
        self.lineEdit_region_max_y.setText(QCoreApplication.translate("ParticleForm", u"12", None))
        self.lineEdit_region_max_x.setText(QCoreApplication.translate("ParticleForm", u"12", None))
        self.lineEdit_region_min_x.setText(QCoreApplication.translate("ParticleForm", u"-12", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("ParticleForm", u"< Regional Segment >", None))
        self.label_17.setText(QCoreApplication.translate("ParticleForm", u"Name :", None))
        self.pushButton_segment_add.setText(QCoreApplication.translate("ParticleForm", u"\ucd94\uac00", None))
        self.pushButton_segment_save.setText(QCoreApplication.translate("ParticleForm", u"\uc800\uc7a5", None))
        self.pushButton_segment_remove.setText(QCoreApplication.translate("ParticleForm", u"\uc0ad\uc81c", None))
        self.checkBox_interval_normal.setText(QCoreApplication.translate("ParticleForm", u"Invert Normal", None))
        self.label_5.setText(QCoreApplication.translate("ParticleForm", u"Mesh:", None))
        self.lineEdit_segment_mesh_path.setText("")
        self.pushButton_mesh_select.setText(QCoreApplication.translate("ParticleForm", u"Select", None))
        self.label_6.setText(QCoreApplication.translate("ParticleForm", u"Material :", None))
        self.comboBox_segment_material.setItemText(0, QCoreApplication.translate("ParticleForm", u"solid", None))
        self.comboBox_segment_material.setItemText(1, QCoreApplication.translate("ParticleForm", u"fluid", None))

        self.label_7.setText(QCoreApplication.translate("ParticleForm", u"Region Type:", None))
        self.comboBox_segment_region_type.setItemText(0, QCoreApplication.translate("ParticleForm", u"fixed", None))
        self.comboBox_segment_region_type.setItemText(1, QCoreApplication.translate("ParticleForm", u"path_field", None))

    # retranslateUi

