from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_BatchRenameWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"BatchRenameWindow")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        
        # Folder selection
        self.horizontalLayout_1 = QHBoxLayout()
        self.folder_label = QLabel(self.centralwidget)
        self.folder_label.setText(u"未选择文件夹")
        self.select_folder_btn = QPushButton(self.centralwidget)
        self.select_folder_btn.setText(u"选择文件夹")
        self.horizontalLayout_1.addWidget(self.folder_label)
        self.horizontalLayout_1.addWidget(self.select_folder_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        
        # Rules layout
        self.gridLayout = QGridLayout()
        
        self.label_prefix = QLabel(u"前缀:")
        self.prefix_input = QLineEdit()
        self.gridLayout.addWidget(self.label_prefix, 0, 0)
        self.gridLayout.addWidget(self.prefix_input, 0, 1)
        
        self.label_suffix = QLabel(u"后缀(不含扩展名):")
        self.suffix_input = QLineEdit()
        self.gridLayout.addWidget(self.label_suffix, 0, 2)
        self.gridLayout.addWidget(self.suffix_input, 0, 3)
        
        self.label_replace_old = QLabel(u"替换:")
        self.replace_old_input = QLineEdit()
        self.gridLayout.addWidget(self.label_replace_old, 1, 0)
        self.gridLayout.addWidget(self.replace_old_input, 1, 1)
        
        self.label_replace_new = QLabel(u"为:")
        self.replace_new_input = QLineEdit()
        self.gridLayout.addWidget(self.label_replace_new, 1, 2)
        self.gridLayout.addWidget(self.replace_new_input, 1, 3)
        
        self.label_start_num = QLabel(u"起始编号(留空不编号):")
        self.start_num_input = QLineEdit()
        self.gridLayout.addWidget(self.label_start_num, 2, 0)
        self.gridLayout.addWidget(self.start_num_input, 2, 1)

        self.label_num_padding = QLabel(u"编号补零位数:")
        self.num_padding_input = QSpinBox()
        self.num_padding_input.setMinimum(0)
        self.num_padding_input.setMaximum(10)
        self.num_padding_input.setValue(0)
        self.gridLayout.addWidget(self.label_num_padding, 2, 2)
        self.gridLayout.addWidget(self.num_padding_input, 2, 3)
        
        self.verticalLayout.addLayout(self.gridLayout)
        
        # Buttons
        self.horizontalLayout_2 = QHBoxLayout()
        self.preview_btn = QPushButton(u"预览")
        self.execute_btn = QPushButton(u"执行重命名")
        self.horizontalLayout_2.addWidget(self.preview_btn)
        self.horizontalLayout_2.addWidget(self.execute_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        # Table
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels([u"原文件名", u"新文件名", u"状态"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.tableWidget)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusBar)
        
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("BatchRenameWindow", u"图片批量重命名", None))
