import os
from PySide2.QtWidgets import QFileDialog, QTableWidgetItem
from components.customwidget import critical_win, info_win
from components.window import SubWindow
from tools.batch_rename.batch_rename_window import Ui_BatchRenameWindow


class BatchRenameParams:
    def __init__(self):
        self.folder_path = ''
        self.prefix = 'img_'
        self.suffix = ''
        self.start_num = 1
        self.digit_count = 4
        self.filter = '*.jpg;*.png;*.bmp'

    def get_params(self, ui):
        self.folder_path = ui.folder_path.text()
        self.prefix = ui.prefix.text()
        self.suffix = ui.suffix.text()
        self.start_num = ui.start_num.value()
        self.digit_count = ui.digit_count.value()
        self.filter = ui.filter.text()

    def set_params(self, ui):
        ui.folder_path.setText(self.folder_path)
        ui.prefix.setText(self.prefix)
        ui.suffix.setText(self.suffix)
        ui.start_num.setValue(self.start_num)
        ui.digit_count.setValue(self.digit_count)
        ui.filter.setText(self.filter)


class BatchRename(SubWindow):
    def __init__(self, name='BatchRename', parent=None):
        super().__init__(name, parent, Ui_BatchRenameWindow(), need_processBar=True)
        self.params = self.load_params(BatchRenameParams())
        self.params.set_params(self.ui)
        self.file_list = []

        self.ui.btn_select_folder.clicked.connect(self.select_folder)
        self.ui.btn_preview.clicked.connect(self.preview_rename)
        self.ui.btn_execute.clicked.connect(self.execute_rename)
        self.ui.prefix.textChanged.connect(self.update_preview_example)
        self.ui.suffix.textChanged.connect(self.update_preview_example)
        self.ui.start_num.valueChanged.connect(self.update_preview_example)
        self.ui.digit_count.valueChanged.connect(self.update_preview_example)

        self.update_preview_example()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self, u'选择图片文件夹', self.params.folder_path or './')
        if folder:
            self.ui.folder_path.setText(folder)
            self.params.folder_path = folder

    def update_preview_example(self):
        prefix = self.ui.prefix.text()
        suffix = self.ui.suffix.text()
        start = self.ui.start_num.value()
        digit = self.ui.digit_count.value()
        example = u'{}{}.{}'.format(
            prefix,
            str(start).zfill(digit),
            (suffix.lstrip('.') if suffix else 'jpg')
        )
        self.ui.preview_example.setText(example)

    def get_image_files(self):
        folder = self.ui.folder_path.text()
        if not folder:
            critical_win(u'请先选择图片文件夹', self)
            return None

        if not os.path.isdir(folder):
            critical_win(u'所选文件夹不存在', self)
            return None

        filter_text = self.ui.filter.text().strip()
        extensions = []
        if filter_text:
            parts = filter_text.replace(';', ' ').replace(',', ' ').split()
            for part in parts:
                part = part.strip().lower().lstrip('*').lstrip('.')
                if part:
                    extensions.append('.' + part)

        if not extensions:
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']

        files = []
        try:
            for entry in os.scandir(folder):
                if entry.is_file():
                    _, ext = os.path.splitext(entry.name)
                    if ext.lower() in extensions:
                        files.append(entry.name)
        except OSError:
            critical_win(u'无法读取文件夹内容', self)
            return None

        files.sort()
        return files

    def generate_new_name(self, index, ext):
        prefix = self.ui.prefix.text()
        suffix = self.ui.suffix.text()
        start = self.ui.start_num.value()
        digit = self.ui.digit_count.value()

        seq = str(start + index).zfill(digit)
        if suffix:
            ext = suffix if suffix.startswith('.') else '.' + suffix

        return u'{}{}{}'.format(prefix, seq, ext)

    def preview_rename(self):
        files = self.get_image_files()
        if files is None:
            return
        if not files:
            info_win(u'文件夹中没有匹配的图片文件', self)
            return

        self.file_list = files
        self.ui.preview_list.setRowCount(len(files))

        for i, fname in enumerate(files):
            _, ext = os.path.splitext(fname)
            new_name = self.generate_new_name(i, ext)
            self.ui.preview_list.setItem(i, 0, QTableWidgetItem(fname))
            self.ui.preview_list.setItem(i, 1, QTableWidgetItem(new_name))

        self.ui.statusbar.showMessage(
            u'共找到 {} 个图片文件，请确认预览后点击执行重命名'.format(len(files))
        )

    def execute_rename(self):
        files = self.get_image_files()
        if files is None:
            return
        if not files:
            info_win(u'文件夹中没有匹配的图片文件', self)
            return

        self.file_list = files
        folder = self.ui.folder_path.text()
        total = len(files)
        success_count = 0
        fail_list = []

        self.progress_bar.setRange(0, total)
        self.progress_bar.setValue(0)

        rename_map = []
        for i, fname in enumerate(files):
            _, ext = os.path.splitext(fname)
            new_name = self.generate_new_name(i, ext)
            rename_map.append((fname, new_name))

        conflict_check = set()
        for _, new_name in rename_map:
            if new_name in conflict_check:
                critical_win(
                    u'重命名后存在同名文件冲突：{}，请调整规则后重试'.format(new_name),
                    self
                )
                return
            conflict_check.add(new_name)

        for idx, (old_name, new_name) in enumerate(rename_map):
            old_path = os.path.join(folder, old_name)
            new_path = os.path.join(folder, new_name)

            if os.path.exists(new_path) and old_name != new_name:
                fail_list.append(u'{} -> {} (目标文件已存在)'.format(old_name, new_name))
            else:
                try:
                    os.rename(old_path, new_path)
                    success_count += 1
                except OSError as e:
                    fail_list.append(u'{} -> {} ({})'.format(old_name, new_name, str(e)))

            self.progress_bar.setValue(idx + 1)
            self.ui.statusbar.showMessage(
                u'正在处理: {}/{} ...'.format(idx + 1, total)
            )

        self.progress_bar.setValue(total)

        if fail_list:
            fail_msg = u'重命名完成：成功 {} 个，失败 {} 个\n\n失败详情：\n{}'.format(
                success_count, len(fail_list), '\n'.join(fail_list[:20])
            )
            if len(fail_list) > 20:
                fail_msg += u'\n... 还有 {} 个失败项未显示'.format(len(fail_list) - 20)
            critical_win(fail_msg, self)
        else:
            info_win(u'重命名完成！共成功处理 {} 个文件'.format(success_count), self)

        self.preview_rename()