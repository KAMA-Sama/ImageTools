from PySide2.QtWidgets import QFileDialog, QTableWidgetItem
from PySide2.QtCore import Qt
from components.window import SubWindow
from components.customwidget import critical_win, info_win
from os import listdir, rename
from os.path import isfile, join, splitext, exists
from natsort import natsorted
from .ui.batch_rename_window import Ui_BatchRename


class BatchRename(SubWindow):
    def __init__(self, name='BatchRename', parent=None):
        super().__init__(name, parent, Ui_BatchRename())
        self.folder_path = './'
        self.image_files = []
        self.renamed_files = []
        
        self.ui.btnSelectPath.clicked.connect(self.select_folder)
        self.ui.btnRefresh.clicked.connect(self.refresh_folder)
        self.ui.btnPreview.clicked.connect(self.preview_rename)
        self.ui.btnRename.clicked.connect(self.execute_rename)
        
        self.ui.statusBar.showMessage("请选择包含图片的文件夹")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "选择文件夹", self.folder_path
        )
        if folder_path:
            self.folder_path = folder_path
            self.ui.lineEditPath.setText(folder_path)
            self.load_images()

    def refresh_folder(self):
        path = self.ui.lineEditPath.text()
        if path and exists(path):
            self.folder_path = path
            self.load_images()
        else:
            critical_win("请输入有效的文件夹路径", self)

    def load_images(self):
        if not self.folder_path:
            return
        
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
        self.image_files = []
        
        for f in listdir(self.folder_path):
            file_path = join(self.folder_path, f)
            if isfile(file_path):
                ext = splitext(f)[1].lower()
                if ext in image_extensions:
                    self.image_files.append(f)
        
        self.image_files = natsorted(self.image_files)
        self.ui.statusBar.showMessage(f"找到 {len(self.image_files)} 张图片")
        self.update_table()

    def generate_new_filename(self, index, ext):
        prefix = self.ui.lineEditPrefix.text()
        suffix = self.ui.lineEditSuffix.text()
        start_num = self.ui.spinBoxStartNum.value()
        digit = self.ui.spinBoxDigit.value()
        
        num_str = str(start_num + index).zfill(digit)
        return f"{prefix}{num_str}{suffix}{ext}"

    def preview_rename(self):
        if not self.image_files:
            self.load_images()
            if not self.image_files:
                critical_win("没有找到图片文件", self)
                return
        
        self.renamed_files = []
        for index, filename in enumerate(self.image_files):
            name, ext = splitext(filename)
            new_name = self.generate_new_filename(index, ext)
            self.renamed_files.append((filename, new_name, "待重命名"))
        
        self.update_table()

    def update_table(self):
        self.ui.tableWidget.setRowCount(len(self.renamed_files) if self.renamed_files else len(self.image_files))
        
        for row in range(self.ui.tableWidget.rowCount()):
            if self.renamed_files:
                old_name, new_name, status = self.renamed_files[row]
                self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(old_name))
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(new_name))
                status_item = QTableWidgetItem(status)
                if status == "成功":
                    status_item.setForeground(Qt.green)
                elif status == "失败":
                    status_item.setForeground(Qt.red)
                self.ui.tableWidget.setItem(row, 2, status_item)
            else:
                self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(self.image_files[row]))
                self.ui.tableWidget.setItem(row, 1, QTableWidgetItem("-"))
                self.ui.tableWidget.setItem(row, 2, QTableWidgetItem("-"))

    def execute_rename(self):
        if not self.renamed_files:
            self.preview_rename()
            if not self.renamed_files:
                return
        
        success_count = 0
        fail_count = 0
        failed_files = []
        
        for index, (old_name, new_name, _) in enumerate(self.renamed_files):
            old_path = join(self.folder_path, old_name)
            new_path = join(self.folder_path, new_name)
            
            try:
                if old_path == new_path:
                    self.renamed_files[index] = (old_name, new_name, "无需重命名")
                    continue
                
                if exists(new_path):
                    self.renamed_files[index] = (old_name, new_name, "失败: 文件名已存在")
                    fail_count += 1
                    failed_files.append(f"{old_name} -> {new_name}")
                    continue
                
                rename(old_path, new_path)
                self.renamed_files[index] = (old_name, new_name, "成功")
                success_count += 1
            except Exception as e:
                self.renamed_files[index] = (old_name, new_name, f"失败: {str(e)}")
                fail_count += 1
                failed_files.append(f"{old_name} -> {new_name}: {str(e)}")
        
        self.update_table()
        self.image_files = [new_name for _, new_name, _ in self.renamed_files]
        self.renamed_files = []
        
        msg = f"重命名完成！成功: {success_count}，失败: {fail_count}"
        self.ui.statusBar.showMessage(msg)
        
        if fail_count > 0:
            fail_msg = msg + "\n\n失败的文件:\n" + "\n".join(failed_files)
            critical_win(fail_msg, self)
        else:
            info_win(msg, self)
