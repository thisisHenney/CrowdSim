# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'solver_common.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QLabel,
    QLineEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_SolverCommonForm(object):
    def setupUi(self, SolverCommonForm):
        if not SolverCommonForm.objectName():
            SolverCommonForm.setObjectName(u"SolverCommonForm")
        SolverCommonForm.resize(300, 656)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SolverCommonForm.sizePolicy().hasHeightForWidth())
        SolverCommonForm.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        SolverCommonForm.setFont(font)
        self.verticalLayout = QVBoxLayout(SolverCommonForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.groupBox = QGroupBox(SolverCommonForm)
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
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 12, 9, -1)
        self.lineEdit_13 = QLineEdit(self.groupBox)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        self.lineEdit_13.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_13.setFont(font)
        self.lineEdit_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_13, 2, 3, 1, 1)

        self.lineEdit_14 = QLineEdit(self.groupBox)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_14.setFont(font)
        self.lineEdit_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_14, 4, 1, 1, 1)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font)
        self.label_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_20, 7, 2, 1, 1)

        self.lineEdit_29 = QLineEdit(self.groupBox)
        self.lineEdit_29.setObjectName(u"lineEdit_29")
        self.lineEdit_29.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_29.setFont(font)
        self.lineEdit_29.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_29, 15, 1, 1, 1)

        self.label_16 = QLabel(self.groupBox)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font)

        self.gridLayout.addWidget(self.label_16, 4, 0, 1, 1)

        self.lineEdit_33 = QLineEdit(self.groupBox)
        self.lineEdit_33.setObjectName(u"lineEdit_33")
        self.lineEdit_33.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_33.setFont(font)
        self.lineEdit_33.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_33, 20, 2, 1, 1)

        self.lineEdit_28 = QLineEdit(self.groupBox)
        self.lineEdit_28.setObjectName(u"lineEdit_28")
        self.lineEdit_28.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_28.setFont(font)
        self.lineEdit_28.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_28, 14, 3, 1, 1)

        self.lineEdit_25 = QLineEdit(self.groupBox)
        self.lineEdit_25.setObjectName(u"lineEdit_25")
        self.lineEdit_25.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_25.setFont(font)
        self.lineEdit_25.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_25, 13, 1, 1, 1)

        self.label_26 = QLabel(self.groupBox)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font)
        self.label_26.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_26, 12, 2, 1, 1)

        self.lineEdit_23 = QLineEdit(self.groupBox)
        self.lineEdit_23.setObjectName(u"lineEdit_23")
        self.lineEdit_23.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_23.setFont(font)
        self.lineEdit_23.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_23, 12, 1, 1, 1)

        self.line_5 = QFrame(self.groupBox)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_5, 17, 0, 1, 4)

        self.label_33 = QLabel(self.groupBox)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setFont(font)
        self.label_33.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_33, 15, 2, 1, 1)

        self.lineEdit_21 = QLineEdit(self.groupBox)
        self.lineEdit_21.setObjectName(u"lineEdit_21")
        self.lineEdit_21.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_21.setFont(font)
        self.lineEdit_21.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_21, 10, 3, 1, 1)

        self.label_28 = QLabel(self.groupBox)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font)
        self.label_28.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_28, 13, 2, 1, 1)

        self.line_6 = QFrame(self.groupBox)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_6, 19, 0, 1, 4)

        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font)

        self.gridLayout.addWidget(self.label_21, 8, 0, 1, 1)

        self.lineEdit_26 = QLineEdit(self.groupBox)
        self.lineEdit_26.setObjectName(u"lineEdit_26")
        self.lineEdit_26.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_26.setFont(font)
        self.lineEdit_26.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_26, 13, 3, 1, 1)

        self.lineEdit_type = QLineEdit(self.groupBox)
        self.lineEdit_type.setObjectName(u"lineEdit_type")
        self.lineEdit_type.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_type.setFont(font)
        self.lineEdit_type.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_type, 0, 1, 1, 3)

        self.label_19 = QLabel(self.groupBox)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font)

        self.gridLayout.addWidget(self.label_19, 7, 0, 1, 1)

        self.label_30 = QLabel(self.groupBox)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font)

        self.gridLayout.addWidget(self.label_30, 15, 0, 1, 1)

        self.lineEdit_16 = QLineEdit(self.groupBox)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_16.setFont(font)
        self.lineEdit_16.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_16, 5, 3, 1, 1)

        self.lineEdit_20 = QLineEdit(self.groupBox)
        self.lineEdit_20.setObjectName(u"lineEdit_20")
        self.lineEdit_20.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_20.setFont(font)
        self.lineEdit_20.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_20, 10, 1, 1, 1)

        self.label_27 = QLabel(self.groupBox)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font)

        self.gridLayout.addWidget(self.label_27, 13, 0, 1, 1)

        self.lineEdit_15 = QLineEdit(self.groupBox)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_15.setFont(font)
        self.lineEdit_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_15, 5, 1, 1, 1)

        self.label_24 = QLabel(self.groupBox)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font)

        self.gridLayout.addWidget(self.label_24, 11, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_15, 2, 2, 1, 1)

        self.lineEdit_18 = QLineEdit(self.groupBox)
        self.lineEdit_18.setObjectName(u"lineEdit_18")
        self.lineEdit_18.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_18.setFont(font)
        self.lineEdit_18.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_18, 7, 3, 1, 1)

        self.line_4 = QFrame(self.groupBox)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_4, 1, 0, 1, 4)

        self.label_25 = QLabel(self.groupBox)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font)

        self.gridLayout.addWidget(self.label_25, 12, 0, 1, 1)

        self.lineEdit_22 = QLineEdit(self.groupBox)
        self.lineEdit_22.setObjectName(u"lineEdit_22")
        self.lineEdit_22.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_22.setFont(font)
        self.lineEdit_22.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_22, 11, 1, 1, 1)

        self.label_29 = QLabel(self.groupBox)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font)

        self.gridLayout.addWidget(self.label_29, 14, 0, 1, 1)

        self.label_23 = QLabel(self.groupBox)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font)
        self.label_23.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_23, 10, 2, 1, 1)

        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font)

        self.gridLayout.addWidget(self.label_13, 0, 0, 1, 1)

        self.label_32 = QLabel(self.groupBox)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setFont(font)
        self.label_32.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_32, 14, 2, 1, 1)

        self.label_35 = QLabel(self.groupBox)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font)

        self.gridLayout.addWidget(self.label_35, 20, 0, 1, 1)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFont(font)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 9, 0, 1, 4)

        self.lineEdit_27 = QLineEdit(self.groupBox)
        self.lineEdit_27.setObjectName(u"lineEdit_27")
        self.lineEdit_27.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_27.setFont(font)
        self.lineEdit_27.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_27, 14, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setCheckable(False)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_38 = QLabel(self.groupBox_2)
        self.label_38.setObjectName(u"label_38")
        self.label_38.setFont(font)

        self.gridLayout_2.addWidget(self.label_38, 2, 0, 1, 1)

        self.comboBox_collision_avoidance = QComboBox(self.groupBox_2)
        self.comboBox_collision_avoidance.addItem("")
        self.comboBox_collision_avoidance.addItem("")
        self.comboBox_collision_avoidance.setObjectName(u"comboBox_collision_avoidance")

        self.gridLayout_2.addWidget(self.comboBox_collision_avoidance, 1, 1, 1, 1)

        self.checkBox_is_blending = QCheckBox(self.groupBox_2)
        self.checkBox_is_blending.setObjectName(u"checkBox_is_blending")
        self.checkBox_is_blending.setChecked(True)

        self.gridLayout_2.addWidget(self.checkBox_is_blending, 0, 0, 1, 1)

        self.label_34 = QLabel(self.groupBox_2)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font)

        self.gridLayout_2.addWidget(self.label_34, 1, 0, 1, 1)

        self.doubleSpinBox_sph_density = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_sph_density.setObjectName(u"doubleSpinBox_sph_density")
        self.doubleSpinBox_sph_density.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_sph_density.setDecimals(1)
        self.doubleSpinBox_sph_density.setValue(4.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_sph_density, 3, 1, 1, 1)

        self.label_39 = QLabel(self.groupBox_2)
        self.label_39.setObjectName(u"label_39")
        self.label_39.setFont(font)

        self.gridLayout_2.addWidget(self.label_39, 3, 0, 1, 1)

        self.doubleSpinBox_collision_density = QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_collision_density.setObjectName(u"doubleSpinBox_collision_density")
        self.doubleSpinBox_collision_density.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.doubleSpinBox_collision_density.setDecimals(1)
        self.doubleSpinBox_collision_density.setValue(2.000000000000000)

        self.gridLayout_2.addWidget(self.doubleSpinBox_collision_density, 2, 1, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 18, 0, 1, 4)

        self.label_17 = QLabel(self.groupBox)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font)

        self.gridLayout.addWidget(self.label_17, 5, 0, 1, 1)

        self.lineEdit_30 = QLineEdit(self.groupBox)
        self.lineEdit_30.setObjectName(u"lineEdit_30")
        self.lineEdit_30.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_30.setFont(font)
        self.lineEdit_30.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_30, 15, 3, 1, 1)

        self.lineEdit_24 = QLineEdit(self.groupBox)
        self.lineEdit_24.setObjectName(u"lineEdit_24")
        self.lineEdit_24.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_24.setFont(font)
        self.lineEdit_24.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_24, 12, 3, 1, 1)

        self.lineEdit_12 = QLineEdit(self.groupBox)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_12.setFont(font)
        self.lineEdit_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_12, 2, 1, 1, 1)

        self.label_36 = QLabel(self.groupBox)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setFont(font)

        self.gridLayout.addWidget(self.label_36, 22, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font)

        self.gridLayout.addWidget(self.label_14, 2, 0, 1, 1)

        self.lineEdit_31 = QLineEdit(self.groupBox)
        self.lineEdit_31.setObjectName(u"lineEdit_31")
        self.lineEdit_31.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_31.setFont(font)
        self.lineEdit_31.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_31, 16, 1, 1, 1)

        self.lineEdit_19 = QLineEdit(self.groupBox)
        self.lineEdit_19.setObjectName(u"lineEdit_19")
        self.lineEdit_19.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_19.setFont(font)
        self.lineEdit_19.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_19, 8, 1, 1, 2)

        self.label_31 = QLabel(self.groupBox)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font)

        self.gridLayout.addWidget(self.label_31, 16, 0, 1, 1)

        self.label_22 = QLabel(self.groupBox)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font)

        self.gridLayout.addWidget(self.label_22, 10, 0, 1, 1)

        self.lineEdit_32 = QLineEdit(self.groupBox)
        self.lineEdit_32.setObjectName(u"lineEdit_32")
        self.lineEdit_32.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_32.setFont(font)
        self.lineEdit_32.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_32, 20, 1, 1, 1)

        self.lineEdit_17 = QLineEdit(self.groupBox)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_17.setFont(font)
        self.lineEdit_17.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_17, 7, 1, 1, 1)

        self.line_3 = QFrame(self.groupBox)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_3, 21, 0, 1, 4)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setFont(font)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 6, 0, 1, 4)

        self.lineEdit_36 = QLineEdit(self.groupBox)
        self.lineEdit_36.setObjectName(u"lineEdit_36")
        self.lineEdit_36.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_36.setFont(font)
        self.lineEdit_36.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_36, 22, 1, 1, 1)

        self.label_18 = QLabel(self.groupBox)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)
        self.label_18.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label_18, 5, 2, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        QWidget.setTabOrder(self.lineEdit_12, self.lineEdit_13)
        QWidget.setTabOrder(self.lineEdit_13, self.lineEdit_14)
        QWidget.setTabOrder(self.lineEdit_14, self.lineEdit_15)
        QWidget.setTabOrder(self.lineEdit_15, self.lineEdit_16)
        QWidget.setTabOrder(self.lineEdit_16, self.lineEdit_17)
        QWidget.setTabOrder(self.lineEdit_17, self.lineEdit_18)
        QWidget.setTabOrder(self.lineEdit_18, self.lineEdit_19)
        QWidget.setTabOrder(self.lineEdit_19, self.lineEdit_20)
        QWidget.setTabOrder(self.lineEdit_20, self.lineEdit_21)
        QWidget.setTabOrder(self.lineEdit_21, self.lineEdit_22)
        QWidget.setTabOrder(self.lineEdit_22, self.lineEdit_23)
        QWidget.setTabOrder(self.lineEdit_23, self.lineEdit_24)
        QWidget.setTabOrder(self.lineEdit_24, self.lineEdit_25)
        QWidget.setTabOrder(self.lineEdit_25, self.lineEdit_26)
        QWidget.setTabOrder(self.lineEdit_26, self.lineEdit_27)
        QWidget.setTabOrder(self.lineEdit_27, self.lineEdit_28)
        QWidget.setTabOrder(self.lineEdit_28, self.lineEdit_29)
        QWidget.setTabOrder(self.lineEdit_29, self.lineEdit_30)
        QWidget.setTabOrder(self.lineEdit_30, self.lineEdit_31)
        QWidget.setTabOrder(self.lineEdit_31, self.lineEdit_32)
        QWidget.setTabOrder(self.lineEdit_32, self.lineEdit_33)
        QWidget.setTabOrder(self.lineEdit_33, self.lineEdit_36)

        self.retranslateUi(SolverCommonForm)

        QMetaObject.connectSlotsByName(SolverCommonForm)
    # setupUi

    def retranslateUi(self, SolverCommonForm):
        SolverCommonForm.setWindowTitle(QCoreApplication.translate("SolverCommonForm", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("SolverCommonForm", u"< Solver Common>", None))
        self.lineEdit_13.setText(QCoreApplication.translate("SolverCommonForm", u"20.0", None))
        self.lineEdit_14.setText(QCoreApplication.translate("SolverCommonForm", u"0.02", None))
        self.label_20.setText(QCoreApplication.translate("SolverCommonForm", u"s_max :", None))
        self.lineEdit_29.setText(QCoreApplication.translate("SolverCommonForm", u"1.0", None))
        self.label_16.setText(QCoreApplication.translate("SolverCommonForm", u"\uc2dc\uac04 \uac04\uaca9 :", None))
        self.lineEdit_33.setText(QCoreApplication.translate("SolverCommonForm", u"0", None))
        self.lineEdit_28.setText(QCoreApplication.translate("SolverCommonForm", u"0.1", None))
        self.lineEdit_25.setText(QCoreApplication.translate("SolverCommonForm", u"0.3", None))
        self.label_26.setText(QCoreApplication.translate("SolverCommonForm", u"V_0 :", None))
        self.lineEdit_23.setText(QCoreApplication.translate("SolverCommonForm", u"0.5", None))
        self.label_33.setText(QCoreApplication.translate("SolverCommonForm", u"k :", None))
        self.lineEdit_21.setText(QCoreApplication.translate("SolverCommonForm", u"50.0", None))
        self.label_28.setText(QCoreApplication.translate("SolverCommonForm", u"T :", None))
        self.label_21.setText(QCoreApplication.translate("SolverCommonForm", u"a_max :", None))
        self.lineEdit_26.setText(QCoreApplication.translate("SolverCommonForm", u"2.0", None))
        self.lineEdit_type.setText(QCoreApplication.translate("SolverCommonForm", u"CROWD", None))
        self.label_19.setText(QCoreApplication.translate("SolverCommonForm", u"s_pref :", None))
        self.label_30.setText(QCoreApplication.translate("SolverCommonForm", u"w :", None))
        self.lineEdit_16.setText(QCoreApplication.translate("SolverCommonForm", u"1", None))
        self.lineEdit_20.setText(QCoreApplication.translate("SolverCommonForm", u"200.0", None))
        self.label_27.setText(QCoreApplication.translate("SolverCommonForm", u"sigma :", None))
        self.lineEdit_15.setText(QCoreApplication.translate("SolverCommonForm", u"0.25", None))
        self.label_24.setText(QCoreApplication.translate("SolverCommonForm", u"K_goal :", None))
        self.label_15.setText(QCoreApplication.translate("SolverCommonForm", u"\uc885\ub8cc \uc2dc\uac04 :", None))
        self.lineEdit_18.setText(QCoreApplication.translate("SolverCommonForm", u"1.8", None))
        self.label_25.setText(QCoreApplication.translate("SolverCommonForm", u"tau :", None))
        self.lineEdit_22.setText(QCoreApplication.translate("SolverCommonForm", u"1.0", None))
        self.label_29.setText(QCoreApplication.translate("SolverCommonForm", u"U_0 :", None))
        self.label_23.setText(QCoreApplication.translate("SolverCommonForm", u"K_ag :", None))
        self.label_13.setText(QCoreApplication.translate("SolverCommonForm", u"\ud574\uc11d \ud0c0\uc785 :", None))
        self.label_32.setText(QCoreApplication.translate("SolverCommonForm", u"R :", None))
        self.label_35.setText(QCoreApplication.translate("SolverCommonForm", u"Init. Velocity :", None))
        self.lineEdit_27.setText(QCoreApplication.translate("SolverCommonForm", u"2.1", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SolverCommonForm", u"< Blending >", None))
        self.label_38.setText(QCoreApplication.translate("SolverCommonForm", u"collision_density :", None))
        self.comboBox_collision_avoidance.setItemText(0, QCoreApplication.translate("SolverCommonForm", u"SF", None))
        self.comboBox_collision_avoidance.setItemText(1, QCoreApplication.translate("SolverCommonForm", u"RVO", None))

        self.checkBox_is_blending.setText(QCoreApplication.translate("SolverCommonForm", u"is_blending", None))
        self.label_34.setText(QCoreApplication.translate("SolverCommonForm", u"collision_avoidance :", None))
        self.label_39.setText(QCoreApplication.translate("SolverCommonForm", u"sph_density :", None))
        self.label_17.setText(QCoreApplication.translate("SolverCommonForm", u"Radius :", None))
        self.lineEdit_30.setText(QCoreApplication.translate("SolverCommonForm", u"200.0", None))
        self.lineEdit_24.setText(QCoreApplication.translate("SolverCommonForm", u"2.1", None))
        self.lineEdit_12.setText(QCoreApplication.translate("SolverCommonForm", u"0.0", None))
        self.label_36.setText(QCoreApplication.translate("SolverCommonForm", u"devices :", None))
        self.label_14.setText(QCoreApplication.translate("SolverCommonForm", u"\uc2dc\uc791\uc2dc\uac04 :", None))
        self.lineEdit_31.setText(QCoreApplication.translate("SolverCommonForm", u"0.1", None))
        self.lineEdit_19.setText(QCoreApplication.translate("SolverCommonForm", u"9999999999.9", None))
        self.label_31.setText(QCoreApplication.translate("SolverCommonForm", u"T_p :", None))
        self.label_22.setText(QCoreApplication.translate("SolverCommonForm", u"K_obs :", None))
        self.lineEdit_32.setText(QCoreApplication.translate("SolverCommonForm", u"0", None))
        self.lineEdit_17.setText(QCoreApplication.translate("SolverCommonForm", u"1.4", None))
        self.lineEdit_36.setText(QCoreApplication.translate("SolverCommonForm", u"0", None))
        self.label_18.setText(QCoreApplication.translate("SolverCommonForm", u"H :", None))
    # retranslateUi

