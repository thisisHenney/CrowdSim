# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grid.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_GridForm(object):
    def setupUi(self, GridForm):
        if not GridForm.objectName():
            GridForm.setObjectName(u"GridForm")
        GridForm.resize(300, 236)
        font = QFont()
        font.setFamilies([u"Ubuntu"])
        font.setPointSize(9)
        GridForm.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(GridForm)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 6, 3, 3)
        self.groupBox = QGroupBox(GridForm)
        self.groupBox.setObjectName(u"groupBox")
        font1 = QFont()
        font1.setFamilies([u"Ubuntu"])
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
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 12, -1, -1)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")
        font2 = QFont()
        font2.setPointSize(9)
        self.label_14.setFont(font2)

        self.horizontalLayout_5.addWidget(self.label_14)

        self.comboBox_name = QComboBox(self.groupBox)
        self.comboBox_name.setObjectName(u"comboBox_name")
        self.comboBox_name.setFont(font2)
        self.comboBox_name.setEditable(True)
        self.comboBox_name.setMaxVisibleItems(10)

        self.horizontalLayout_5.addWidget(self.comboBox_name)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 2)

        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, -1)
        self.horizontalSpacer_2 = QSpacerItem(40, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.pushButton_add = QPushButton(self.groupBox)
        self.pushButton_add.setObjectName(u"pushButton_add")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_add.sizePolicy().hasHeightForWidth())
        self.pushButton_add.setSizePolicy(sizePolicy)
        self.pushButton_add.setMaximumSize(QSize(60, 16777215))
        self.pushButton_add.setFont(font2)

        self.horizontalLayout_6.addWidget(self.pushButton_add)

        self.pushButton_save = QPushButton(self.groupBox)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setMaximumSize(QSize(60, 16777215))
        self.pushButton_save.setFont(font2)

        self.horizontalLayout_6.addWidget(self.pushButton_save)

        self.pushButton_remove = QPushButton(self.groupBox)
        self.pushButton_remove.setObjectName(u"pushButton_remove")
        self.pushButton_remove.setMaximumSize(QSize(60, 16777215))
        self.pushButton_remove.setFont(font2)

        self.horizontalLayout_6.addWidget(self.pushButton_remove)

        self.horizontalLayout_6.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_22 = QLabel(self.groupBox)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font2)
        self.label_22.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_22)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(3)
        self.lineEdit_min_y = QLineEdit(self.groupBox)
        self.lineEdit_min_y.setObjectName(u"lineEdit_min_y")
        self.lineEdit_min_y.setEnabled(True)
        self.lineEdit_min_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_min_y.setFont(font2)
        self.lineEdit_min_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_min_y, 0, 2, 1, 1)

        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font2)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_23, 0, 0, 1, 1)

        self.lineEdit_min_x = QLineEdit(self.groupBox)
        self.lineEdit_min_x.setObjectName(u"lineEdit_min_x")
        self.lineEdit_min_x.setEnabled(True)
        self.lineEdit_min_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_min_x.setFont(font2)
        self.lineEdit_min_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_min_x, 0, 1, 1, 1)

        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font2)
        self.label_24.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.label_24, 1, 0, 1, 1)

        self.lineEdit_max_y = QLineEdit(self.groupBox)
        self.lineEdit_max_y.setObjectName(u"lineEdit_max_y")
        self.lineEdit_max_y.setEnabled(True)
        self.lineEdit_max_y.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_max_y.setFont(font2)
        self.lineEdit_max_y.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_max_y, 1, 2, 1, 1)

        self.lineEdit_max_x = QLineEdit(self.groupBox)
        self.lineEdit_max_x.setObjectName(u"lineEdit_max_x")
        self.lineEdit_max_x.setEnabled(True)
        self.lineEdit_max_x.setMaximumSize(QSize(100, 16777215))
        self.lineEdit_max_x.setFont(font2)
        self.lineEdit_max_x.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_max_x, 1, 1, 1, 1)


        self.horizontalLayout_4.addLayout(self.gridLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, -1, -1, -1)
        self.label_26 = QLabel(self.groupBox)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font2)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_26)

        self.lineEdit_width = QLineEdit(self.groupBox)
        self.lineEdit_width.setObjectName(u"lineEdit_width")
        self.lineEdit_width.setEnabled(True)
        self.lineEdit_width.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_width.setFont(font2)
        self.lineEdit_width.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.lineEdit_width)

        self.horizontalLayout_8.setStretch(0, 2)
        self.horizontalLayout_8.setStretch(1, 3)

        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, -1, -1, -1)
        self.label_25 = QLabel(self.groupBox)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font2)
        self.label_25.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_14.addWidget(self.label_25)

        self.lineEdit_max_particle = QLineEdit(self.groupBox)
        self.lineEdit_max_particle.setObjectName(u"lineEdit_max_particle")
        self.lineEdit_max_particle.setEnabled(True)
        self.lineEdit_max_particle.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_max_particle.setFont(font2)
        self.lineEdit_max_particle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_14.addWidget(self.lineEdit_max_particle)

        self.horizontalLayout_14.setStretch(0, 2)
        self.horizontalLayout_14.setStretch(1, 3)

        self.verticalLayout.addLayout(self.horizontalLayout_14)


        self.verticalLayout_2.addWidget(self.groupBox)

        QWidget.setTabOrder(self.comboBox_name, self.pushButton_add)
        QWidget.setTabOrder(self.pushButton_add, self.pushButton_save)
        QWidget.setTabOrder(self.pushButton_save, self.pushButton_remove)
        QWidget.setTabOrder(self.pushButton_remove, self.lineEdit_min_x)
        QWidget.setTabOrder(self.lineEdit_min_x, self.lineEdit_min_y)
        QWidget.setTabOrder(self.lineEdit_min_y, self.lineEdit_max_x)
        QWidget.setTabOrder(self.lineEdit_max_x, self.lineEdit_max_y)
        QWidget.setTabOrder(self.lineEdit_max_y, self.lineEdit_width)
        QWidget.setTabOrder(self.lineEdit_width, self.lineEdit_max_particle)

        self.retranslateUi(GridForm)

        QMetaObject.connectSlotsByName(GridForm)
    # setupUi

    def retranslateUi(self, GridForm):
        GridForm.setWindowTitle(QCoreApplication.translate("GridForm", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("GridForm", u"< Grid Properties >", None))
        self.label_14.setText(QCoreApplication.translate("GridForm", u"Name :", None))
        self.pushButton_add.setText(QCoreApplication.translate("GridForm", u"\ucd94\uac00", None))
        self.pushButton_save.setText(QCoreApplication.translate("GridForm", u"\uc800\uc7a5", None))
        self.pushButton_remove.setText(QCoreApplication.translate("GridForm", u"\uc0ad\uc81c", None))
        self.label_22.setText(QCoreApplication.translate("GridForm", u"Domain", None))
        self.lineEdit_min_y.setText(QCoreApplication.translate("GridForm", u"-12", None))
        self.label_23.setText(QCoreApplication.translate("GridForm", u"min :", None))
        self.lineEdit_min_x.setText(QCoreApplication.translate("GridForm", u"-12", None))
        self.label_24.setText(QCoreApplication.translate("GridForm", u"max :", None))
        self.lineEdit_max_y.setText(QCoreApplication.translate("GridForm", u"12", None))
        self.lineEdit_max_x.setText(QCoreApplication.translate("GridForm", u"12", None))
        self.label_26.setText(QCoreApplication.translate("GridForm", u"width :", None))
        self.lineEdit_width.setText(QCoreApplication.translate("GridForm", u"-1", None))
        self.label_25.setText(QCoreApplication.translate("GridForm", u"max_particle :", None))
        self.lineEdit_max_particle.setText(QCoreApplication.translate("GridForm", u"10000", None))
    # retranslateUi

