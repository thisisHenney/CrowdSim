# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'report.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_ReportForm(object):
    def setupUi(self, ReportForm):
        if not ReportForm.objectName():
            ReportForm.setObjectName(u"ReportForm")
        ReportForm.resize(300, 549)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ReportForm.sizePolicy().hasHeightForWidth())
        ReportForm.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        ReportForm.setFont(font)
        self.verticalLayout = QVBoxLayout(ReportForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 6, 3, 3)
        self.groupBox_4 = QGroupBox(ReportForm)
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
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(10, -1, -1, -1)
        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_10.addWidget(self.label_5)

        self.lineEdit_start_time = QLineEdit(self.groupBox_4)
        self.lineEdit_start_time.setObjectName(u"lineEdit_start_time")
        self.lineEdit_start_time.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_start_time.setFont(font)
        self.lineEdit_start_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.lineEdit_start_time)

        self.horizontalLayout_10.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(10, -1, -1, -1)
        self.label_7 = QLabel(self.groupBox_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_11.addWidget(self.label_7)

        self.lineEdit_end_time = QLineEdit(self.groupBox_4)
        self.lineEdit_end_time.setObjectName(u"lineEdit_end_time")
        self.lineEdit_end_time.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_end_time.setFont(font)
        self.lineEdit_end_time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_11.addWidget(self.lineEdit_end_time)

        self.horizontalLayout_11.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(10, -1, -1, -1)
        self.label_8 = QLabel(self.groupBox_4)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_8)

        self.lineEdit_time_interval = QLineEdit(self.groupBox_4)
        self.lineEdit_time_interval.setObjectName(u"lineEdit_time_interval")
        self.lineEdit_time_interval.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_time_interval.setFont(font)
        self.lineEdit_time_interval.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_12.addWidget(self.lineEdit_time_interval)

        self.horizontalLayout_12.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_12)


        self.verticalLayout.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(ReportForm)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_5.setFont(font1)
        self.groupBox_5.setStyleSheet(u"QGroupBox {\n"
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
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, 12, -1, -1)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, -1, -1, -1)
        self.checkBox_pressure = QCheckBox(self.groupBox_5)
        self.checkBox_pressure.setObjectName(u"checkBox_pressure")
        self.checkBox_pressure.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_pressure)

        self.checkBox_density = QCheckBox(self.groupBox_5)
        self.checkBox_density.setObjectName(u"checkBox_density")
        self.checkBox_density.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_density)

        self.checkBox_restDensity = QCheckBox(self.groupBox_5)
        self.checkBox_restDensity.setObjectName(u"checkBox_restDensity")
        self.checkBox_restDensity.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_restDensity)

        self.checkBox_position = QCheckBox(self.groupBox_5)
        self.checkBox_position.setObjectName(u"checkBox_position")
        self.checkBox_position.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_position)

        self.checkBox_velocity = QCheckBox(self.groupBox_5)
        self.checkBox_velocity.setObjectName(u"checkBox_velocity")
        self.checkBox_velocity.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_velocity)

        self.checkBox_goal_position = QCheckBox(self.groupBox_5)
        self.checkBox_goal_position.setObjectName(u"checkBox_goal_position")
        self.checkBox_goal_position.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_goal_position)

        self.checkBox_adjoint = QCheckBox(self.groupBox_5)
        self.checkBox_adjoint.setObjectName(u"checkBox_adjoint")
        self.checkBox_adjoint.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_adjoint)

        self.checkBox_prt_idx = QCheckBox(self.groupBox_5)
        self.checkBox_prt_idx.setObjectName(u"checkBox_prt_idx")
        self.checkBox_prt_idx.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_prt_idx)

        self.checkBox_forward_vector = QCheckBox(self.groupBox_5)
        self.checkBox_forward_vector.setObjectName(u"checkBox_forward_vector")
        self.checkBox_forward_vector.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_forward_vector)

        self.checkBox_line_id = QCheckBox(self.groupBox_5)
        self.checkBox_line_id.setObjectName(u"checkBox_line_id")
        self.checkBox_line_id.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_line_id)

        self.checkBox_acceleration_collision = QCheckBox(self.groupBox_5)
        self.checkBox_acceleration_collision.setObjectName(u"checkBox_acceleration_collision")
        self.checkBox_acceleration_collision.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_acceleration_collision)


        self.verticalLayout_6.addLayout(self.verticalLayout_2)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(ReportForm)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_6.setFont(font1)
        self.groupBox_6.setStyleSheet(u"QGroupBox {\n"
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
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 12, -1, -1)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, -1, -1, -1)
        self.checkBox_path_goal_point = QCheckBox(self.groupBox_6)
        self.checkBox_path_goal_point.setObjectName(u"checkBox_path_goal_point")

        self.verticalLayout_3.addWidget(self.checkBox_path_goal_point)

        self.checkBox_path_solid = QCheckBox(self.groupBox_6)
        self.checkBox_path_solid.setObjectName(u"checkBox_path_solid")

        self.verticalLayout_3.addWidget(self.checkBox_path_solid)


        self.verticalLayout_7.addLayout(self.verticalLayout_3)


        self.verticalLayout.addWidget(self.groupBox_6)


        self.retranslateUi(ReportForm)

        QMetaObject.connectSlotsByName(ReportForm)
    # setupUi

    def retranslateUi(self, ReportForm):
        ReportForm.setWindowTitle(QCoreApplication.translate("ReportForm", u"Form", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("ReportForm", u"< Save >", None))
        self.label_5.setText(QCoreApplication.translate("ReportForm", u"Start Time:", None))
        self.lineEdit_start_time.setText(QCoreApplication.translate("ReportForm", u"0.0", None))
        self.label_7.setText(QCoreApplication.translate("ReportForm", u"End Time:", None))
        self.lineEdit_end_time.setText(QCoreApplication.translate("ReportForm", u"100.0", None))
        self.label_8.setText(QCoreApplication.translate("ReportForm", u"Time Interval:", None))
        self.lineEdit_time_interval.setText(QCoreApplication.translate("ReportForm", u"0.02", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("ReportForm", u"< Items >", None))
        self.checkBox_pressure.setText(QCoreApplication.translate("ReportForm", u"presssure", None))
        self.checkBox_density.setText(QCoreApplication.translate("ReportForm", u"density", None))
        self.checkBox_restDensity.setText(QCoreApplication.translate("ReportForm", u"restDensity", None))
        self.checkBox_position.setText(QCoreApplication.translate("ReportForm", u"position", None))
        self.checkBox_velocity.setText(QCoreApplication.translate("ReportForm", u"velocity", None))
        self.checkBox_goal_position.setText(QCoreApplication.translate("ReportForm", u"goal_position", None))
        self.checkBox_adjoint.setText(QCoreApplication.translate("ReportForm", u"adjoint", None))
        self.checkBox_prt_idx.setText(QCoreApplication.translate("ReportForm", u"prt_idx", None))
        self.checkBox_forward_vector.setText(QCoreApplication.translate("ReportForm", u"forward_vector", None))
        self.checkBox_line_id.setText(QCoreApplication.translate("ReportForm", u"line_id", None))
        self.checkBox_acceleration_collision.setText(QCoreApplication.translate("ReportForm", u"acceleration_collision", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("ReportForm", u"< Flags >", None))
        self.checkBox_path_goal_point.setText(QCoreApplication.translate("ReportForm", u"path_goal_point", None))
        self.checkBox_path_solid.setText(QCoreApplication.translate("ReportForm", u"path_solid", None))
    # retranslateUi

