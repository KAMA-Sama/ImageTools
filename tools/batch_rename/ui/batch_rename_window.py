# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'batch_rename_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resource_rc


class Ui_BatchRename(object):
    def setupUi(self, BatchRename):
        if not BatchRename.objectName():
            BatchRename.setObjectName(u"BatchRename")
        BatchRename.resize(900, 700)
        icon = QIcon()
        icon.addFile(u":/tool_icon/resource/main.png", QSize(), QIcon.Normal, QIcon.Off)
        BatchRename.setWindowIcon(icon)

        self.centralwidget = QWidget(BatchRename)
        self.centralwidget.setObjectName(u"centralwidget")

        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.groupSelect = QGroupBox(self.centralwidget)
        self.groupSelect.setObjectName(u"groupSelect")
        self.horizontalLayout_2 = QHBoxLayout(self.groupSelect)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.labelPath = QLabel(self.groupSelect)
        self.labelPath.setObjectName(u"labelPath")
        self.horizontalLayout_2.addWidget(self.labelPath)

        self.lineEditPath = QLineEdit(self.groupSelect)
        self.lineEditPath.setObjectName(u"lineEditPath")
        self.horizontalLayout_2.addWidget(self.lineEditPath)

        self.btnSelectPath = QPushButton(self.groupSelect)
        self.btnSelectPath.setObjectName(u"btnSelectPath")
        self.horizontalLayout_2.addWidget(self.btnSelectPath)

        self.btnRefresh = QPushButton(self.groupSelect)
        self.btnRefresh.setObjectName(u"btnRefresh")
        self.horizontalLayout_2.addWidget(self.btnRefresh)

        self.verticalLayout.addWidget(self.groupSelect)

        self.groupRule = QGroupBox(self.centralwidget)
        self.groupRule.setObjectName(u"groupRule")
        self.gridLayout = QGridLayout(self.groupRule)
        self.gridLayout.setObjectName(u"gridLayout")

        self.labelPrefix = QLabel(self.groupRule)
        self.labelPrefix.setObjectName(u"labelPrefix")
        self.gridLayout.addWidget(self.labelPrefix, 0, 0, 1, 1)

        self.lineEditPrefix = QLineEdit(self.groupRule)
        self.lineEditPrefix.setObjectName(u"lineEditPrefix")
        self.gridLayout.addWidget(self.lineEditPrefix, 0, 1, 1, 1)

        self.labelStartNum = QLabel(self.groupRule)
        self.labelStartNum.setObjectName(u"labelStartNum")
        self.gridLayout.addWidget(self.labelStartNum, 0, 2, 1, 1)

        self.spinBoxStartNum = QSpinBox(self.groupRule)
        self.spinBoxStartNum.setObjectName(u"spinBoxStartNum")
        self.spinBoxStartNum.setMinimum(0)
        self.spinBoxStartNum.setMaximum(99999)
        self.spinBoxStartNum.setValue(1)
        self.gridLayout.addWidget(self.spinBoxStartNum, 0, 3, 1, 1)

        self.labelDigit = QLabel(self.groupRule)
        self.labelDigit.setObjectName(u"labelDigit")
        self.gridLayout.addWidget(self.labelDigit, 1, 0, 1, 1)

        self.spinBoxDigit = QSpinBox(self.groupRule)
        self.spinBoxDigit.setObjectName(u"spinBoxDigit")
        self.spinBoxDigit.setMinimum(1)
        self.spinBoxDigit.setMaximum(10)
        self.spinBoxDigit.setValue(3)
        self.gridLayout.addWidget(self.spinBoxDigit, 1, 1, 1, 1)

        self.labelSuffix = QLabel(self.groupRule)
        self.labelSuffix.setObjectName(u"labelSuffix")
        self.gridLayout.addWidget(self.labelSuffix, 1, 2, 1, 1)

        self.lineEditSuffix = QLineEdit(self.groupRule)
        self.lineEditSuffix.setObjectName(u"lineEditSuffix")
        self.gridLayout.addWidget(self.lineEditSuffix, 1, 3, 1, 1)

        self.btnPreview = QPushButton(self.groupRule)
        self.btnPreview.setObjectName(u"btnPreview")
        self.gridLayout.addWidget(self.btnPreview, 2, 0, 1, 4)

        self.verticalLayout.addWidget(self.groupRule)

        self.groupPreview = QGroupBox(self.centralwidget)
        self.groupPreview.setObjectName(u"groupPreview")
        self.verticalLayout_2 = QVBoxLayout(self.groupPreview)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.tableWidget = QTableWidget(self.groupPreview)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["原文件名", "新文件名", "状态"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalLayout_2.addWidget(self.tableWidget)

        self.verticalLayout.addWidget(self.groupPreview)

        self.btnRename = QPushButton(self.centralwidget)
        self.btnRename.setObjectName(u"btnRename")
        self.verticalLayout.addWidget(self.btnRename)

        BatchRename.setCentralWidget(self.centralwidget)

        self.statusBar = QStatusBar(BatchRename)
        self.statusBar.setObjectName(u"statusBar")
        BatchRename.setStatusBar(self.statusBar)

        self.retranslateUi(BatchRename)

        QMetaObject.connectSlotsByName(BatchRename)

    def retranslateUi(self, BatchRename):
        BatchRename.setWindowTitle(QCoreApplication.translate("BatchRename", u"图片批量重命名", None))
        self.groupSelect.setTitle(QCoreApplication.translate("BatchRename", u"选择文件夹", None))
        self.labelPath.setText(QCoreApplication.translate("BatchRename", u"文件夹路径:", None))
        self.btnSelectPath.setText(QCoreApplication.translate("BatchRename", u"浏览...", None))
        self.btnRefresh.setText(QCoreApplication.translate("BatchRename", u"刷新", None))
        self.groupRule.setTitle(QCoreApplication.translate("BatchRename", u"重命名规则", None))
        self.labelPrefix.setText(QCoreApplication.translate("BatchRename", u"前缀:", None))
        self.labelStartNum.setText(QCoreApplication.translate("BatchRename", u"起始编号:", None))
        self.labelDigit.setText(QCoreApplication.translate("BatchRename", u"编号位数:", None))
        self.labelSuffix.setText(QCoreApplication.translate("BatchRename", u"后缀:", None))
        self.btnPreview.setText(QCoreApplication.translate("BatchRename", u"预览重命名", None))
        self.groupPreview.setTitle(QCoreApplication.translate("BatchRename", u"预览", None))
        self.btnRename.setText(QCoreApplication.translate("BatchRename", u"执行重命名", None))
