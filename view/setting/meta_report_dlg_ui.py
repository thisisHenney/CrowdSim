# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'meta_report_dlg.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QDoubleSpinBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(415, 538)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(415, 538))
        Dialog.setMaximumSize(QSize(16777215, 538))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_meta = QGroupBox(Dialog)
        self.groupBox_meta.setObjectName(u"groupBox_meta")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.groupBox_meta.setFont(font)
        self.groupBox_meta.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 2px;\n"
"    margin-top: 10;\n"
"	 border-color : rgb(200, 200, 200);\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
"}\n"
"")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_meta)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(-1, 15, -1, -1)
        self.gridLayout_meta = QGridLayout()
        self.gridLayout_meta.setObjectName(u"gridLayout_meta")
        self.label_9 = QLabel(self.groupBox_meta)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(111, 0))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_meta.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_7 = QLabel(self.groupBox_meta)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_meta.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_meta)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_meta.addWidget(self.label_6, 2, 0, 1, 1)

        self.lineEdit_meta_version = QLineEdit(self.groupBox_meta)
        self.lineEdit_meta_version.setObjectName(u"lineEdit_meta_version")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_meta_version.sizePolicy().hasHeightForWidth())
        self.lineEdit_meta_version.setSizePolicy(sizePolicy1)
        self.lineEdit_meta_version.setFont(font1)
        self.lineEdit_meta_version.setAlignment(Qt.AlignCenter)

        self.gridLayout_meta.addWidget(self.lineEdit_meta_version, 0, 1, 1, 1)

        self.lineEdit_meta_method = QLineEdit(self.groupBox_meta)
        self.lineEdit_meta_method.setObjectName(u"lineEdit_meta_method")
        sizePolicy1.setHeightForWidth(self.lineEdit_meta_method.sizePolicy().hasHeightForWidth())
        self.lineEdit_meta_method.setSizePolicy(sizePolicy1)
        self.lineEdit_meta_method.setFont(font1)
        self.lineEdit_meta_method.setAlignment(Qt.AlignCenter)

        self.gridLayout_meta.addWidget(self.lineEdit_meta_method, 1, 1, 1, 1)

        self.lineEdit_meta_title = QLineEdit(self.groupBox_meta)
        self.lineEdit_meta_title.setObjectName(u"lineEdit_meta_title")
        sizePolicy1.setHeightForWidth(self.lineEdit_meta_title.sizePolicy().hasHeightForWidth())
        self.lineEdit_meta_title.setSizePolicy(sizePolicy1)
        self.lineEdit_meta_title.setFont(font1)
        self.lineEdit_meta_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_meta.addWidget(self.lineEdit_meta_title, 2, 1, 1, 1)

        self.gridLayout_meta.setColumnStretch(1, 1)

        self.verticalLayout_8.addLayout(self.gridLayout_meta)


        self.verticalLayout.addWidget(self.groupBox_meta)

        self.groupBox_result = QGroupBox(Dialog)
        self.groupBox_result.setObjectName(u"groupBox_result")
        self.groupBox_result.setFont(font)
        self.groupBox_result.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 2px;\n"
"    margin-top: 10;\n"
"	 border-color : rgb(200, 200, 200);\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
"}\n"
"")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_result)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(-1, 15, -1, -1)
        self.gridLayout_result = QGridLayout()
        self.gridLayout_result.setObjectName(u"gridLayout_result")
        self.lineEdit_result_save_end_time = QLineEdit(self.groupBox_result)
        self.lineEdit_result_save_end_time.setObjectName(u"lineEdit_result_save_end_time")
        sizePolicy1.setHeightForWidth(self.lineEdit_result_save_end_time.sizePolicy().hasHeightForWidth())
        self.lineEdit_result_save_end_time.setSizePolicy(sizePolicy1)
        self.lineEdit_result_save_end_time.setFont(font1)
        self.lineEdit_result_save_end_time.setAlignment(Qt.AlignCenter)

        self.gridLayout_result.addWidget(self.lineEdit_result_save_end_time, 4, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_result)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_result.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_result_save_start_time = QLineEdit(self.groupBox_result)
        self.lineEdit_result_save_start_time.setObjectName(u"lineEdit_result_save_start_time")
        sizePolicy1.setHeightForWidth(self.lineEdit_result_save_start_time.sizePolicy().hasHeightForWidth())
        self.lineEdit_result_save_start_time.setSizePolicy(sizePolicy1)
        self.lineEdit_result_save_start_time.setFont(font1)
        self.lineEdit_result_save_start_time.setAlignment(Qt.AlignCenter)

        self.gridLayout_result.addWidget(self.lineEdit_result_save_start_time, 3, 1, 1, 1)

        self.label = QLabel(self.groupBox_result)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 0))
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_result.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_result_export_path = QLineEdit(self.groupBox_result)
        self.lineEdit_result_export_path.setObjectName(u"lineEdit_result_export_path")
        sizePolicy1.setHeightForWidth(self.lineEdit_result_export_path.sizePolicy().hasHeightForWidth())
        self.lineEdit_result_export_path.setSizePolicy(sizePolicy1)
        self.lineEdit_result_export_path.setFont(font1)
        self.lineEdit_result_export_path.setAlignment(Qt.AlignCenter)

        self.gridLayout_result.addWidget(self.lineEdit_result_export_path, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_result)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_result.addWidget(self.label_4, 4, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_result)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_result.addWidget(self.label_3, 3, 0, 1, 1)

        self.doubleSpinBox_result_save_time_interval = QDoubleSpinBox(self.groupBox_result)
        self.doubleSpinBox_result_save_time_interval.setObjectName(u"doubleSpinBox_result_save_time_interval")
        sizePolicy1.setHeightForWidth(self.doubleSpinBox_result_save_time_interval.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_result_save_time_interval.setSizePolicy(sizePolicy1)
        self.doubleSpinBox_result_save_time_interval.setFont(font1)
        self.doubleSpinBox_result_save_time_interval.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox_result_save_time_interval.setValue(0.020000000000000)

        self.gridLayout_result.addWidget(self.doubleSpinBox_result_save_time_interval, 5, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_result)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_result.addWidget(self.label_5, 5, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_result.addItem(self.verticalSpacer_5, 6, 0, 1, 1)

        self.groupBox_result_items = QGroupBox(self.groupBox_result)
        self.groupBox_result_items.setObjectName(u"groupBox_result_items")
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(True)
        self.groupBox_result_items.setFont(font2)
        self.groupBox_result_items.setStyleSheet(u"QGroupBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 2px;\n"
"    margin-top: 10;\n"
"	 border-color : rgb(200, 200, 200);\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    left: 10px;\n"
"    padding: 0 3px 0 3px;\n"
"}\n"
"")
        self.groupBox_result_items.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.groupBox_result_items.setCheckable(False)
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_result_items)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(-1, 15, -1, -1)
        self.checkBox_result_items_pressure = QCheckBox(self.groupBox_result_items)
        self.checkBox_result_items_pressure.setObjectName(u"checkBox_result_items_pressure")
        self.checkBox_result_items_pressure.setFont(font1)

        self.verticalLayout_13.addWidget(self.checkBox_result_items_pressure)

        self.checkBox_result_items_rest_density = QCheckBox(self.groupBox_result_items)
        self.checkBox_result_items_rest_density.setObjectName(u"checkBox_result_items_rest_density")
        self.checkBox_result_items_rest_density.setFont(font1)

        self.verticalLayout_13.addWidget(self.checkBox_result_items_rest_density)

        self.checkBox_result_items_position = QCheckBox(self.groupBox_result_items)
        self.checkBox_result_items_position.setObjectName(u"checkBox_result_items_position")
        self.checkBox_result_items_position.setFont(font1)

        self.verticalLayout_13.addWidget(self.checkBox_result_items_position)

        self.checkBox_result_items_velocity = QCheckBox(self.groupBox_result_items)
        self.checkBox_result_items_velocity.setObjectName(u"checkBox_result_items_velocity")
        self.checkBox_result_items_velocity.setFont(font1)

        self.verticalLayout_13.addWidget(self.checkBox_result_items_velocity)

        self.checkBox_result_items_goal_position = QCheckBox(self.groupBox_result_items)
        self.checkBox_result_items_goal_position.setObjectName(u"checkBox_result_items_goal_position")
        self.checkBox_result_items_goal_position.setFont(font1)

        self.verticalLayout_13.addWidget(self.checkBox_result_items_goal_position)


        self.gridLayout_result.addWidget(self.groupBox_result_items, 7, 0, 1, 2)

        self.verticalSpacer_6 = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_result.addItem(self.verticalSpacer_6, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_result_export_format_binary = QLineEdit(self.groupBox_result)
        self.lineEdit_result_export_format_binary.setObjectName(u"lineEdit_result_export_format_binary")
        sizePolicy1.setHeightForWidth(self.lineEdit_result_export_format_binary.sizePolicy().hasHeightForWidth())
        self.lineEdit_result_export_format_binary.setSizePolicy(sizePolicy1)
        self.lineEdit_result_export_format_binary.setFont(font1)
        self.lineEdit_result_export_format_binary.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit_result_export_format_binary)

        self.lineEdit_result_export_format_type = QLineEdit(self.groupBox_result)
        self.lineEdit_result_export_format_type.setObjectName(u"lineEdit_result_export_format_type")
        sizePolicy1.setHeightForWidth(self.lineEdit_result_export_format_type.sizePolicy().hasHeightForWidth())
        self.lineEdit_result_export_format_type.setSizePolicy(sizePolicy1)
        self.lineEdit_result_export_format_type.setFont(font1)
        self.lineEdit_result_export_format_type.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lineEdit_result_export_format_type)


        self.gridLayout_result.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.gridLayout_result.setColumnStretch(1, 1)

        self.verticalLayout_7.addLayout(self.gridLayout_result)


        self.verticalLayout.addWidget(self.groupBox_result)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox_meta.setTitle(QCoreApplication.translate("Dialog", u"< Meta >", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Version :", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Method :", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Title :", None))
        self.lineEdit_meta_version.setText(QCoreApplication.translate("Dialog", u"202405", None))
        self.lineEdit_meta_method.setText(QCoreApplication.translate("Dialog", u"SPH2D", None))
        self.lineEdit_meta_title.setText("")
        self.groupBox_result.setTitle(QCoreApplication.translate("Dialog", u"< Result Report >", None))
        self.lineEdit_result_save_end_time.setText(QCoreApplication.translate("Dialog", u"100", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Export Format :", None))
        self.lineEdit_result_save_start_time.setText(QCoreApplication.translate("Dialog", u"0.0", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Export Path :", None))
        self.lineEdit_result_export_path.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Save End Time :", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Save Start Time :", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Save Time Interval:", None))
        self.groupBox_result_items.setTitle(QCoreApplication.translate("Dialog", u"< Items >", None))
        self.checkBox_result_items_pressure.setText(QCoreApplication.translate("Dialog", u"items pressure", None))
        self.checkBox_result_items_rest_density.setText(QCoreApplication.translate("Dialog", u"rest density", None))
        self.checkBox_result_items_position.setText(QCoreApplication.translate("Dialog", u"position", None))
        self.checkBox_result_items_velocity.setText(QCoreApplication.translate("Dialog", u"velocity", None))
        self.checkBox_result_items_goal_position.setText(QCoreApplication.translate("Dialog", u"goal position", None))
        self.lineEdit_result_export_format_binary.setText(QCoreApplication.translate("Dialog", u"BINARY_VTK", None))
        self.lineEdit_result_export_format_type.setText(QCoreApplication.translate("Dialog", u"NFile", None))
    # retranslateUi

