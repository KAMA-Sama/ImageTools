import os
import uuid
from PySide2.QtGui import QBrush, QColor
from PySide2.QtWidgets import QFileDialog, QTableWidgetItem
from components.customwidget import critical_win, info_win
from components.window import SubWindow
from .batch_rename_window import Ui_BatchRenameWindow


class BatchRenameParams:
    def __init__(self):
        self.folder_path = ''
        self.prefix = 'image_'
        self.start_index = 1
        self.digits = 3


class BatchRenameTool(SubWindow):
    image_suffix = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tif', '.tiff')

    def __init__(self, name='BatchRenameTool', parent=None):
        super().__init__(name, parent, Ui_BatchRenameWindow())
        self.params = self.load_params(BatchRenameParams())
        self.rename_plan = []
        self._apply_params()
        self.ui.select_folder.clicked.connect(self.select_folder)
        self.ui.preview_button.clicked.connect(lambda: self.preview_rename(show_popup=True))
        self.ui.execute_button.clicked.connect(self.execute_rename)
        self.ui.prefix.textChanged.connect(self.on_rule_changed)
        self.ui.start_index.valueChanged.connect(self.on_rule_changed)
        self.ui.digits.valueChanged.connect(self.on_rule_changed)
        self.ui.folder_path.textChanged.connect(self.on_folder_changed)
        self.refresh_rule_preview()
        if self.ui.folder_path.text().strip() != '':
            self.preview_rename()

    def _apply_params(self):
        self.ui.folder_path.setText(self.params.folder_path)
        self.ui.prefix.setText(self.params.prefix)
        self.ui.start_index.setValue(self.params.start_index)
        self.ui.digits.setValue(self.params.digits)

    def _sync_params(self):
        self.params.folder_path = self.ui.folder_path.text().strip()
        self.params.prefix = self.ui.prefix.text().strip()
        self.params.start_index = self.ui.start_index.value()
        self.params.digits = self.ui.digits.value()

    def on_rule_changed(self):
        self._sync_params()
        self.refresh_rule_preview()
        if os.path.isdir(self.params.folder_path):
            self.preview_rename()

    def on_folder_changed(self):
        self._sync_params()
        if os.path.isdir(self.params.folder_path):
            self.preview_rename()
        else:
            self.rename_plan = []
            self.ui.preview_table.setRowCount(0)
            self.ui.statusBar.showMessage('请选择有效的图片文件夹')

    def refresh_rule_preview(self):
        prefix = self.ui.prefix.text().strip()
        sample_name = '{}{}.jpg'.format(prefix, str(self.ui.start_index.value()).zfill(self.ui.digits.value()))
        self.ui.rule_preview.setText(sample_name)

    def select_folder(self):
        current_path = self.ui.folder_path.text().strip()
        if current_path == '' or os.path.isdir(current_path) is False:
            current_path = './'
        folder = QFileDialog.getExistingDirectory(self, '选择图片文件夹', current_path)
        if folder != '':
            self.ui.folder_path.setText(folder)
            self.preview_rename(show_popup=True)

    def _get_image_files(self, folder_path):
        file_paths = []
        for filename in sorted(os.listdir(folder_path), key=lambda item: item.lower()):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath) and filename.lower().endswith(self.image_suffix):
                file_paths.append(filepath)
        return file_paths

    def _build_plan(self, folder_path):
        file_paths = self._get_image_files(folder_path)
        plan = []
        if len(file_paths) == 0:
            return plan
        prefix = self.ui.prefix.text().strip()
        source_names = set(os.path.basename(file_path) for file_path in file_paths)
        target_counts = {}
        start_index = self.ui.start_index.value()
        digits = self.ui.digits.value()
        for offset, file_path in enumerate(file_paths):
            source_name = os.path.basename(file_path)
            _, extension = os.path.splitext(source_name)
            target_name = '{}{}{}'.format(prefix, str(start_index + offset).zfill(digits), extension)
            target_counts[target_name] = target_counts.get(target_name, 0) + 1
            plan.append({
                'source_path': file_path,
                'source_name': source_name,
                'target_name': target_name,
                'target_path': os.path.join(folder_path, target_name),
                'status': '可重命名'
            })
        for item in plan:
            if target_counts[item['target_name']] > 1:
                item['status'] = '目标文件名重复'
                continue
            if item['source_name'] == item['target_name']:
                item['status'] = '保持不变'
                continue
            if os.path.exists(item['target_path']) and item['target_name'] not in source_names:
                item['status'] = '目标已存在'
        return plan

    def _fill_preview_table(self, plan):
        self.ui.preview_table.setRowCount(len(plan))
        for row, item in enumerate(plan):
            source_item = QTableWidgetItem(item['source_name'])
            target_item = QTableWidgetItem(item['target_name'])
            status_item = QTableWidgetItem(item['status'])
            if item['status'] == '可重命名':
                color = QColor(46, 125, 50)
            elif item['status'] == '保持不变':
                color = QColor(117, 117, 117)
            else:
                color = QColor(198, 40, 40)
            status_item.setForeground(QBrush(color))
            self.ui.preview_table.setItem(row, 0, source_item)
            self.ui.preview_table.setItem(row, 1, target_item)
            self.ui.preview_table.setItem(row, 2, status_item)
        self.ui.preview_table.resizeRowsToContents()

    def preview_rename(self, show_popup=False):
        self._sync_params()
        self.refresh_rule_preview()
        folder_path = self.params.folder_path
        prefix = self.params.prefix
        if folder_path == '' or os.path.isdir(folder_path) is False:
            self.rename_plan = []
            self.ui.preview_table.setRowCount(0)
            self.ui.statusBar.showMessage('请选择有效的图片文件夹')
            if show_popup:
                critical_win('请选择有效的图片文件夹', self)
            return []
        if prefix == '':
            self.rename_plan = []
            self.ui.preview_table.setRowCount(0)
            self.ui.statusBar.showMessage('请输入文件名前缀')
            if show_popup:
                critical_win('请输入文件名前缀', self)
            return []
        plan = self._build_plan(folder_path)
        if len(plan) == 0:
            self.rename_plan = []
            self.ui.preview_table.setRowCount(0)
            self.ui.statusBar.showMessage('当前文件夹内没有可处理的图片')
            if show_popup:
                critical_win('当前文件夹内没有可处理的图片', self)
            return []
        self.rename_plan = plan
        self._fill_preview_table(plan)
        error_count = len([item for item in plan if item['status'] not in ('可重命名', '保持不变')])
        if error_count > 0:
            self.ui.statusBar.showMessage('预览完成，存在 {} 项失败'.format(error_count))
        else:
            self.ui.statusBar.showMessage('预览完成，共 {} 张图片'.format(len(plan)))
        return plan

    def _build_temp_path(self, source_path):
        temp_path = '{}.imagetools_tmp_{}'.format(source_path, uuid.uuid4().hex)
        while os.path.exists(temp_path):
            temp_path = '{}.imagetools_tmp_{}'.format(source_path, uuid.uuid4().hex)
        return temp_path

    def execute_rename(self):
        plan = self.preview_rename(show_popup=True)
        if len(plan) == 0:
            return
        invalid_items = [item for item in plan if item['status'] not in ('可重命名', '保持不变')]
        if len(invalid_items) > 0:
            detail = '\n'.join('{} -> {}'.format(item['source_name'], item['status']) for item in invalid_items[:10])
            if len(invalid_items) > 10:
                detail = detail + '\n...'
            critical_win('当前预览存在失败项，无法执行重命名\n{}'.format(detail), self)
            return
        rename_items = [item for item in plan if item['status'] == '可重命名']
        if len(rename_items) == 0:
            info_win('当前规则下无需执行重命名', self)
            self.ui.statusBar.showMessage('没有需要重命名的图片')
            return
        temp_items = []
        completed_items = []
        try:
            for item in rename_items:
                temp_path = self._build_temp_path(item['source_path'])
                os.rename(item['source_path'], temp_path)
                item['temp_path'] = temp_path
                temp_items.append(item)
        except Exception as error:
            for item in reversed(temp_items):
                temp_path = item.get('temp_path', '')
                if temp_path != '' and os.path.exists(temp_path) and os.path.exists(item['source_path']) is False:
                    os.rename(temp_path, item['source_path'])
            critical_win('执行失败：{}'.format(str(error)), self)
            self.ui.statusBar.showMessage('执行失败，已停止重命名')
            return
        try:
            for item in rename_items:
                os.rename(item['temp_path'], item['target_path'])
                completed_items.append(item)
        except Exception as error:
            for item in reversed(completed_items):
                if os.path.exists(item['target_path']) and os.path.exists(item['source_path']) is False:
                    os.rename(item['target_path'], item['source_path'])
            for item in reversed(temp_items):
                temp_path = item.get('temp_path', '')
                if temp_path != '' and os.path.exists(temp_path) and os.path.exists(item['source_path']) is False:
                    os.rename(temp_path, item['source_path'])
            critical_win('执行失败：{}'.format(str(error)), self)
            self.ui.statusBar.showMessage('执行失败，已回滚已处理文件')
            self.preview_rename()
            return
        info_win('重命名完成，共处理 {} 张图片'.format(len(rename_items)), self)
        self.ui.statusBar.showMessage('重命名完成，共处理 {} 张图片'.format(len(rename_items)))
        self.preview_rename()
