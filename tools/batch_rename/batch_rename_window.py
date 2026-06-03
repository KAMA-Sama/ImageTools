# -*- coding: utf-8 -*-

from PySide2.QtCore import (QCoreApplication, QMetaObject, Qt)
from PySide2.QtGui import QIcon, QFont
from PySide2.QtWidgets import *


class Ui_BatchRenameWindow(object):
    def setupUi(self, BatchRenameWindow):
        if not BatchRenameWindow.objectName():
            BatchRenameWindow.setObjectName(u"BatchRenameWindow")
        BatchRenameWindow.resize(820, 600)
        BatchRenameWindow.setMinimumSize(QSize(700, 500))
        self.centralwidget = QWidget(BatchRenameWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")

        self.groupBox_folder = QGroupBox(self.centralwidget)
        self.groupBox_folder.setObjectName(u"groupBox_folder")
        self.gridLayout_folder = QGridLayout(self.groupBox_folder)
        self.gridLayout_folder.setObjectName(u"gridLayout_folder")

        self.folder_path = QLineEdit(self.groupBox_folder)
        self.folder_path.setObjectName(u"folder_path")
        self.folder_path.setReadOnly(True)

        self.btn_select_folder = QPushButton(self.groupBox_folder)
        self.btn_select_folder.setObjectName(u"btn_select_folder")
        self.btn_select_folder.setMaximumSize(QSize(80, 16777215))

        self.gridLayout_folder.addWidget(self.folder_path, 0, 0, 1, 1)
        self.gridLayout_folder.addWidget(self.btn_select_folder, 0, 1, 1, 1)

        self.gridLayout.addWidget(self.groupBox_folder, 0, 0, 1, 1)

        self.groupBox_rule = QGroupBox(self.centralwidget)
        self.groupBox_rule.setObjectName(u"groupBox_rule")
        self.gridLayout_rule = QGridLayout(self.groupBox_rule)
        self.gridLayout_rule.setObjectName(u"gridLayout_rule")

        self.label_prefix = QLabel(self.groupBox_rule)
        self.label_prefix.setObjectName(u"label_prefix")
        self.prefix = QLineEdit(self.groupBox_rule)
        self.prefix.setObjectName(u"prefix")

        self.label_suffix = QLabel(self.groupBox_rule)
        self.label_suffix.setObjectName(u"label_suffix")
        self.suffix = QLineEdit(self.groupBox_rule)
        self.suffix.setObjectName(u"suffix")

        self.label_start_num = QLabel(self.groupBox_rule)
        self.label_start_num.setObjectName(u"label_start_num")
        self.start_num = QSpinBox(self.groupBox_rule)
        self.start_num.setObjectName(u"start_num")
        self.start_num.setRange(0, 999999)
        self.start_num.setValue(1)

        self.label_digit = QLabel(self.groupBox_rule)
        self.label_digit.setObjectName(u"label_digit")
        self.digit_count = QSpinBox(self.groupBox_rule)
        self.digit_count.setObjectName(u"digit_count")
        self.digit_count.setRange(1, 10)
        self.digit_count.setValue(4)

        self.label_filter = QLabel(self.groupBox_rule)
        self.label_filter.setObjectName(u"label_filter")
        self.filter = QLineEdit(self.groupBox_rule)
        self.filter.setObjectName(u"filter")
        self.filter.setPlaceholderText(u"*.jpg;*.png;*.bmp")

        self.label_preview_name = QLabel(self.groupBox_rule)
        self.label_preview_name.setObjectName(u"label_preview_name")
        self.preview_example = QLineEdit(self.groupBox_rule)
        self.preview_example.setObjectName(u"preview_example")
        self.preview_example.setReadOnly(True)

        self.gridLayout_rule.addWidget(self.label_prefix, 0, 0, 1, 1)
        self.gridLayout_rule.addWidget(self.prefix, 0, 1, 1, 1)
        self.gridLayout_rule.addWidget(self.label_suffix, 1, 0, 1, 1)
        self.gridLayout_rule.addWidget(self.suffix, 1, 1, 1, 1)
        self.gridLayout_rule.addWidget(self.label_start_num, 2, 0, 1, 1)
        self.gridLayout_rule.addWidget(self.start_num, 2, 1, 1, 1)
        self.gridLayout_rule.addWidget(self.label_digit, 3, 0, 1, 1)
        self.gridLayout_rule.addWidget(self.digit_count, 3, 1, 1, 1)
        self.gridLayout_rule.addWidget(self.label_filter, 4, 0, 1, 1)
        self.gridLayout_rule.addWidget(self.filter, 4, 1, 1, 1)
        self.gridLayout_rule.addWidget(self.label_preview_name, 5, 0, 1, 1)
        self.gridLayout_rule.addWidget(self.preview_example, 5, 1, 1, 1)

        self.gridLayout.addWidget(self.groupBox_rule, 1, 0, 1, 1)

        self.groupBox_preview = QGroupBox(self.centralwidget)
        self.groupBox_preview.setObjectName(u"groupBox_preview")
        self.gridLayout_preview = QGridLayout(self.groupBox_preview)
        self.gridLayout_preview.setObjectName(u"gridLayout_preview")

        self.preview_list = QTableWidget(self.groupBox_preview)
        self.preview_list.setObjectName(u"preview_list")
        self.preview_list.setColumnCount(2)
        self.preview_list.setHorizontalHeaderLabels([u"\u539f\u6587\u4ef6\u540d", u"\u65b0\u6587\u4ef6\u540d"])
        self.preview_list.horizontalHeader().setStretchLastSection(True)
        self.preview_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.preview_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.preview_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.preview_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.gridLayout_preview.addWidget(self.preview_list, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_preview, 2, 0, 1, 1)

        self.horizontalLayout_btn = QHBoxLayout()
        self.horizontalLayout_btn.setObjectName(u"horizontalLayout_btn")

        self.btn_preview = QPushButton(self.centralwidget)
        self.btn_preview.setObjectName(u"btn_preview")
        self.btn_preview.setMinimumSize(QSize(100, 32))

        self.btn_execute = QPushButton(self.centralwidget)
        self.btn_execute.setObjectName(u"btn_execute")
        self.btn_execute.setMinimumSize(QSize(100, 32))

        self.horizontalLayout_btn.addStretch()
        self.horizontalLayout_btn.addWidget(self.btn_preview)
        self.horizontalLayout_btn.addWidget(self.btn_execute)
        self.horizontalLayout_btn.addStretch()

        self.gridLayout.addLayout(self.horizontalLayout_btn, 3, 0, 1, 1)

        self.statusbar = QStatusBar(BatchRenameWindow)
        self.statusbar.setObjectName(u"statusbar")
        BatchRenameWindow.setStatusBar(self.statusbar)

        self.retranslateUi(BatchRenameWindow)
        QMetaObject.connectSlotsByName(BatchRenameWindow)

    def retranslateUi(self, BatchRenameWindow):
        BatchRenameWindow.setWindowTitle(QCoreApplication.translate("BatchRenameWindow", u"\u56fe\u7247\u6279\u91cf\u91cd\u547d\u540d", None))
        self.groupBox_folder.setTitle(QCoreApplication.translate("BatchRenameWindow", u"\u9009\u62e9\u6587\u4ef6\u5939", None))
        self.btn_select_folder.setText(QCoreApplication.translate("BatchRenameWindow", u"\u6d4f\u89c8...", None))
        self.groupBox_rule.setTitle(QCoreApplication.translate("BatchRenameWindow", u"\u91cd\u547d\u540d\u89c4\u5219", None))
        self.label_prefix.setText(QCoreApplication.translate("BatchRenameWindow", u"\u524d\u7f00\uff1a", None))
        self.label_suffix.setText(QCoreApplication.translate("BatchRenameWindow", u"\u540e\u7f00\uff1a", None))
        self.label_start_num.setText(QCoreApplication.translate("BatchRenameWindow", u"\u8d77\u59cb\u5e8f\u53f7\uff1a", None))
        self.label_digit.setText(QCoreApplication.translate("BatchRenameWindow", u"\u5e8f\u53f7\u4f4d\u6570\uff1a", None))
        self.label_filter.setText(QCoreApplication.translate("BatchRenameWindow", u"\u6587\u4ef6\u8fc7\u6ee4\uff1a", None))
        self.label_preview_name.setText(QCoreApplication.translate("BatchRenameWindow", u"\u9884\u89c8\u793a\u4f8b\uff1a", None))
        self.groupBox_preview.setTitle(QCoreApplication.translate("BatchRenameWindow", u"\u91cd\u547d\u540d\u9884\u89c8", None))
        self.btn_preview.setText(QCoreApplication.translate("BatchRenameWindow", u"\u9884\u89c8\u91cd\u547d\u540d", None))
        self.btn_execute.setText(QCoreApplication.translate("BatchRenameWindow", u"\u6267\u884c\u91cd\u547d\u540d", None))