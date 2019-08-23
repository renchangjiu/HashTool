import hashlib, sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QIcon, QKeyEvent, QColor
from PyQt5.QtWidgets import QWidget, QListWidgetItem

from src.main_window import Ui_Form
from src.hash_util import HashUtil
from src.clipboard_util import ClipboardUtil

null = None


class MainWindow(QWidget, Ui_Form):
    def __init__(self, file_path):
        QWidget.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        self.listWidget.installEventFilter(self)
        self.setWindowTitle("HashUtil")
        self.init_style()
        if not os.path.isfile(file_path):
            widget_item = QListWidgetItem(self.listWidget)
            widget_item.setTextAlignment(Qt.AlignCenter)
            widget_item.setForeground(QColor("red"))
            widget_item.setText("文件不存在")
            return


        print(sys.argv)
        widget_item = QListWidgetItem(self.listWidget)
        widget_item.setText(os.path.basename(file_path))
        widget_item.setTextAlignment(Qt.AlignCenter)
        widget_item = QListWidgetItem(self.listWidget)
        widget_item.setText(file_path)
        widget_item.setTextAlignment(Qt.AlignCenter)
        widget_item = QListWidgetItem(self.listWidget)
        widget_item.setText(format_size(os.path.getsize(file_path)))

        widget_item.setTextAlignment(Qt.AlignCenter)

        self.listWidget.addItem(self.gen_list_item("MD5", HashUtil.MD5(file_path)))
        self.listWidget.addItem(self.gen_list_item("SHA1", HashUtil.SHA1(file_path)))
        self.listWidget.addItem(self.gen_list_item("SHA256", HashUtil.SHA256(file_path)))

        self.listWidget.itemClicked.connect(self.item_click)

    def gen_list_item(self, hash_type: str, hash_value: str) -> QListWidgetItem:
        widget_item = QListWidgetItem()
        widget_item.setText("%s:   %s" % (hash_type, hash_value))
        widget_item.setData(Qt.UserRole, hash_value)
        widget_item.setToolTip("点击复制")
        # widget_item.setTextAlignment(Qt.AlignHCenter)
        return widget_item

    def init_style(self):
        self.setWindowIcon(QIcon("./resource/image/app.png"))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.listWidget.setStyleSheet(
            "QListWidget{outline:0px; color:#5c5c5c; background:#f5f5f7;border-top:none;border-left:none;"
            "font-size:13px;border-right:1px solid #e1e1e2;border-bottom:1px solid #e1e1e2}"
            "QListWidget::Item{height:32px;border:0px solid gray;padding-left:19px;font-size:13px;}"
            "QListWidget::Item:hover{color:#000000;background:transparent;border:0px solid gray;}"
            "QListWidget::Item:selected{background:#e6e7ea;color:#000000;border-left: 1px solid #c62f2f;}")
        self.listWidget.setCursor(Qt.PointingHandCursor)

    def item_click(self, list_item: QListWidgetItem):
        data = list_item.data(Qt.UserRole)
        if data is not null:
            ClipboardUtil.set_text(data)
            print("已复制到剪贴板: %s" % data)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Space:
                self.close()
        return False


def format_size(size: int) -> str:
    """ 返回以KB 或 MB表示的文件大小, size: 字节数"""
    if size < 1024 * 1024:
        size = str(int(size / 1024)) + "KB"
    else:
        size = str(round(size / 1024 / 1024, 1)) + "MB"
    return size


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(sys.argv[1])
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
