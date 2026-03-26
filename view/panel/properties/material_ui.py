# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'material.ui'
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
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MaterialsForm(object):
    def setupUi(self, MaterialsForm):
        if not MaterialsForm.objectName():
            MaterialsForm.setObjectName(u"MaterialsForm")
        MaterialsForm.resize(300, 230)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MaterialsForm.sizePolicy().hasHeightForWidth())
        MaterialsForm.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        MaterialsForm.setFont(font)
        self.verticalLayout = QVBoxLayout(MaterialsForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.groupBox = QGroupBox(MaterialsForm)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(8)
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
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 12, 9, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.horizontalLayout.addWidget(self.label_13)

        self.comboBox_name = QComboBox(self.groupBox)
        self.comboBox_name.setObjectName(u"comboBox_name")
        self.comboBox_name.setFont(font)
        self.comboBox_name.setEditable(True)
        self.comboBox_name.setMaxVisibleItems(10)

        self.horizontalLayout.addWidget(self.comboBox_name)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 3)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

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

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, -1, -1, -1)
        self.checkBox_main = QCheckBox(self.groupBox)
        self.checkBox_main.setObjectName(u"checkBox_main")
        self.checkBox_main.setFont(font)

        self.horizontalLayout_7.addWidget(self.checkBox_main)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, -1, -1, -1)
        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font)
        self.label_21.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_21)

        self.lineEdit_rho_min = QLineEdit(self.groupBox)
        self.lineEdit_rho_min.setObjectName(u"lineEdit_rho_min")
        self.lineEdit_rho_min.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_rho_min.setFont(font)
        self.lineEdit_rho_min.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.lineEdit_rho_min)

        self.lineEdit_rho_max = QLineEdit(self.groupBox)
        self.lineEdit_rho_max.setObjectName(u"lineEdit_rho_max")
        self.lineEdit_rho_max.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_rho_max.setFont(font)
        self.lineEdit_rho_max.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.lineEdit_rho_max)


        self.verticalLayout_2.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, -1, -1, -1)
        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_14.addWidget(self.label_23)

        self.lineEdit_mu = QLineEdit(self.groupBox)
        self.lineEdit_mu.setObjectName(u"lineEdit_mu")
        self.lineEdit_mu.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_mu.setFont(font)
        self.lineEdit_mu.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_14.addWidget(self.lineEdit_mu)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, -1, -1, -1)
        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_24)

        self.lineEdit_outlet_id = QLineEdit(self.groupBox)
        self.lineEdit_outlet_id.setObjectName(u"lineEdit_outlet_id")
        self.lineEdit_outlet_id.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_outlet_id.setFont(font)
        self.lineEdit_outlet_id.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_15.addWidget(self.lineEdit_outlet_id)


        self.verticalLayout_2.addLayout(self.horizontalLayout_15)


        self.verticalLayout.addWidget(self.groupBox)

        QWidget.setTabOrder(self.comboBox_name, self.pushButton_add)
        QWidget.setTabOrder(self.pushButton_add, self.pushButton_save)
        QWidget.setTabOrder(self.pushButton_save, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.checkBox_main)
        QWidget.setTabOrder(self.checkBox_main, self.lineEdit_rho_min)
        QWidget.setTabOrder(self.lineEdit_rho_min, self.lineEdit_rho_max)
        QWidget.setTabOrder(self.lineEdit_rho_max, self.lineEdit_mu)

        self.retranslateUi(MaterialsForm)

        QMetaObject.connectSlotsByName(MaterialsForm)
    # setupUi

    def retranslateUi(self, MaterialsForm):
        MaterialsForm.setWindowTitle(QCoreApplication.translate("MaterialsForm", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("MaterialsForm", u"< Materials Properties >", None))
        self.label_13.setText(QCoreApplication.translate("MaterialsForm", u"\uc774\ub984 :", None))
        self.pushButton_add.setText(QCoreApplication.translate("MaterialsForm", u"\ucd94\uac00", None))
        self.pushButton_save.setText(QCoreApplication.translate("MaterialsForm", u"\uc800\uc7a5", None))
        self.pushButton_remove.setText(QCoreApplication.translate("MaterialsForm", u"\uc0ad\uc81c", None))
        self.checkBox_main.setText(QCoreApplication.translate("MaterialsForm", u"Main Material", None))
        self.label_21.setText(QCoreApplication.translate("MaterialsForm", u"Rho (Min/Max) :", None))
        self.lineEdit_rho_min.setText(QCoreApplication.translate("MaterialsForm", u"0", None))
        self.lineEdit_rho_max.setText(QCoreApplication.translate("MaterialsForm", u"5", None))
        self.label_23.setText(QCoreApplication.translate("MaterialsForm", u"mu :", None))
        self.lineEdit_mu.setText(QCoreApplication.translate("MaterialsForm", u"0.0", None))
        self.label_24.setText(QCoreApplication.translate("MaterialsForm", u"outlet_id :", None))
        self.lineEdit_outlet_id.setText(QCoreApplication.translate("MaterialsForm", u"0", None))
    # retranslateUi

