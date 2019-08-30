from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QListWidgetItem


class ThreadCalHash(QThread):
    # hash_value, pre_text, list_widget_item
    cal_end = QtCore.pyqtSignal(str, str, QListWidgetItem)

    def __init__(self, hash_func, file_path: str, pre_text: str, list_widget_item: QListWidgetItem):
        super().__init__()
        self.hash_func = hash_func
        self.path = file_path
        self.pre_text = pre_text
        self.item = list_widget_item

    def run(self) -> None:
        hash_value = self.hash_func(self.path)
        self.cal_end.emit(hash_value, self.pre_text, self.item)
