import os
from PySide2.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem
from tools.batch_rename.batch_rename_window import Ui_BatchRenameWindow
from components.window import SubWindow
from logging import info, error

class BatchRenameTool(SubWindow):
    def __init__(self, name='BatchRenameTool', parent=None):
        super().__init__(name, parent, Ui_BatchRenameWindow(), need_processBar=True)
        
        self.current_folder = ""
        self.image_files = []
        self.preview_data = [] # List of tuples: (original_name, new_name)
        
        # Connect signals
        self.ui.select_folder_btn.clicked.connect(self.select_folder)
        self.ui.preview_btn.clicked.connect(self.preview_rename)
        self.ui.execute_btn.clicked.connect(self.execute_rename)
        
        self.ui.execute_btn.setEnabled(False)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择图片文件夹", "./")
        if folder:
            self.current_folder = folder
            self.ui.folder_label.setText(folder)
            self.load_images()

    def load_images(self):
        self.image_files = []
        if not self.current_folder or not os.path.exists(self.current_folder):
            return
            
        valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.raw', '.yuv'}
        for f in os.listdir(self.current_folder):
            if os.path.isfile(os.path.join(self.current_folder, f)):
                ext = os.path.splitext(f)[1].lower()
                if ext in valid_extensions:
                    self.image_files.append(f)
        
        # Sort files to ensure deterministic order
        self.image_files.sort()
        
        self.update_table_original()
        self.ui.execute_btn.setEnabled(False)
        self.info_bar.setText(f"共加载 {len(self.image_files)} 张图片")

    def update_table_original(self):
        self.ui.tableWidget.setRowCount(len(self.image_files))
        for i, f in enumerate(self.image_files):
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(f))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(""))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(""))

    def preview_rename(self):
        if not self.image_files:
            QMessageBox.warning(self, "警告", "没有可重命名的图片文件！")
            return
            
        prefix = self.ui.prefix_input.text()
        suffix = self.ui.suffix_input.text()
        old_str = self.ui.replace_old_input.text()
        new_str = self.ui.replace_new_input.text()
        
        start_num_str = self.ui.start_num_input.text().strip()
        padding = self.ui.num_padding_input.value()
        
        use_numbering = False
        current_num = 0
        if start_num_str.isdigit():
            use_numbering = True
            current_num = int(start_num_str)
            
        self.preview_data = []
        self.ui.tableWidget.setRowCount(len(self.image_files))
        
        for i, original_name in enumerate(self.image_files):
            name, ext = os.path.splitext(original_name)
            
            # Apply replace
            if old_str:
                name = name.replace(old_str, new_str)
                
            # Apply prefix and suffix
            new_name = prefix + name + suffix
            
            # Apply numbering
            if use_numbering:
                num_str = str(current_num).zfill(padding)
                new_name += num_str
                current_num += 1
                
            new_name += ext
            self.preview_data.append((original_name, new_name))
            
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem(original_name))
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(new_name))
            self.ui.tableWidget.setItem(i, 2, QTableWidgetItem("待执行"))
            
        self.ui.execute_btn.setEnabled(True)

    def execute_rename(self):
        if not self.preview_data:
            return
            
        # Check for conflicts
        new_names = [data[1] for data in self.preview_data]
        if len(new_names) != len(set(new_names)):
            QMessageBox.critical(self, "错误", "重命名规则会导致文件名冲突，请修改规则！")
            return
            
        success_count = 0
        fail_count = 0
        
        self.progress_bar.setRange(0, len(self.preview_data))
        self.progress_bar.setValue(0)
        
        for i, (old_name, new_name) in enumerate(self.preview_data):
            if old_name == new_name:
                self.ui.tableWidget.setItem(i, 2, QTableWidgetItem("跳过"))
                success_count += 1
                self.progress_bar.setValue(i + 1)
                continue
                
            old_path = os.path.join(self.current_folder, old_name)
            new_path = os.path.join(self.current_folder, new_name)
            
            if os.path.exists(new_path) and old_name.lower() != new_name.lower():
                self.ui.tableWidget.setItem(i, 2, QTableWidgetItem("失败: 文件已存在"))
                fail_count += 1
            else:
                try:
                    os.rename(old_path, new_path)
                    self.ui.tableWidget.setItem(i, 2, QTableWidgetItem("成功"))
                    success_count += 1
                except Exception as e:
                    error(f"Rename failed: {e}")
                    self.ui.tableWidget.setItem(i, 2, QTableWidgetItem(f"失败: {str(e)}"))
                    fail_count += 1
                    
            self.progress_bar.setValue(i + 1)
            
        QMessageBox.information(self, "重命名完成", f"成功: {success_count}, 失败: {fail_count}")
        self.ui.execute_btn.setEnabled(False)
        self.load_images() # Reload directory to reflect changes
