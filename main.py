import sys
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QIcon, QColor, QMouseEvent
from PyQt5.QtWidgets import QWidget, QListWidgetItem

from src.app_attribute import AppAttribute as app
from src.main_window import Ui_Form
from src.hash_util import HashUtil
from src.clipboard_util import ClipboardUtil
from src.thread_cal_hash import ThreadCalHash

null = None


class MainWindow(QWidget, Ui_Form):
    def __init__(self, file_path):
        QWidget.__init__(self)
        Ui_Form.__init__(self)
        self.setupUi(self)
        self.listWidget.installEventFilter(self)
        self.label.installEventFilter(self)
        self.point = QtCore.QPoint()
        self.setWindowTitle("HashUtil")
        self.init_style()
        if not os.path.isfile(file_path):
            widget_item = QListWidgetItem(self.listWidget)
            widget_item.setTextAlignment(Qt.AlignCenter)
            widget_item.setForeground(QColor("red"))
            widget_item.setText("未检测到文件")
            return

        widget_item = QListWidgetItem(self.listWidget)
        widget_item.setText(os.path.basename(file_path))
        widget_item.setFlags(Qt.NoItemFlags)

        widget_item = QListWidgetItem(self.listWidget)
        widget_item.setText(file_path)
        widget_item.setFlags(Qt.NoItemFlags)

        widget_item = QListWidgetItem(self.listWidget)
        widget_item.setText(format_size(os.path.getsize(file_path)))
        widget_item.setFlags(Qt.NoItemFlags)

        item0 = self.gen_list_item("MD5   ", "Calculating...")
        self.listWidget.addItem(item0)
        item1 = self.gen_list_item("SHA1  ", "Calculating...")
        self.listWidget.addItem(item1)
        item2 = self.gen_list_item("SHA256", "Calculating...")
        self.listWidget.addItem(item2)

        # 开启3个线程分别计算hash值
        self.thread0 = ThreadCalHash(HashUtil.MD5, file_path, "MD5    : ", item0)
        self.thread0.start()
        self.thread0.cal_end.connect(self.cal_end_callback)

        self.thread1 = ThreadCalHash(HashUtil.SHA1, file_path, "SHA1   : ", item1)
        self.thread1.start()
        self.thread1.cal_end.connect(self.cal_end_callback)

        self.thread2 = ThreadCalHash(HashUtil.SHA256, file_path, "SHA256 : ", item2)
        self.thread2.start()
        self.thread2.cal_end.connect(self.cal_end_callback)

        self.listWidget.itemClicked.connect(self.item_click)

    def cal_end_callback(self, hash_value: str, pre_text: str, item: QListWidgetItem):
        item.setText(pre_text + hash_value)
        item.setData(Qt.UserRole, hash_value)

    def gen_list_item(self, hash_type: str, hash_value: str) -> QListWidgetItem:
        widget_item = QListWidgetItem()
        widget_item.setText("%s : %s" % (hash_type, hash_value))
        widget_item.setData(Qt.UserRole, hash_value)
        widget_item.setToolTip("点击复制")
        return widget_item

    def init_style(self):
        self.setWindowIcon(QIcon(app.root + "/resource/image/app.png"))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.listWidget.setStyleSheet(
            "QListWidget{font-family:Consolas;outline:0px; color:#5c5c5c; background:#f5f5f7;font-size:15px;border:0px}"
            "QListWidget::Item{height:32px;border:0px solid gray;padding-left:19px;font-size:13px;}"
            "QListWidget::Item:hover{color:#000000;background:transparent;border:0px solid gray;}"
            "QListWidget::Item:selected{background:#e6e7ea;color:#000000;border-left: 1px solid #c62f2f;}")
        self.listWidget.horizontalScrollBar().setVisible(False)
        self.listWidget.setCursor(Qt.PointingHandCursor)

        self.label.setStyleSheet(
            "QLabel{font-family:Consolas;color:#5c5c5c;font-size:13px;background:#f5f5f7;border:0px;}")
        self.label.setText("Click to copy. Press any key to close.")
        self.label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

    def item_click(self, list_item: QListWidgetItem):
        data = list_item.data(Qt.UserRole)
        if data is not null and data != "Calculating...":
            ClipboardUtil.set_text(data)
            self.label.setText("Copied.")

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QtCore.QEvent.KeyPress:
            self.close()
        return False

    def mousePressEvent(self, mouse_event: QMouseEvent):
        if mouse_event.button() == QtCore.Qt.LeftButton:
            self.point = mouse_event.globalPos() - self.frameGeometry().topLeft()
        elif mouse_event.button() == QtCore.Qt.RightButton:
            self.close()

    def mouseMoveEvent(self, mouse_event: QMouseEvent):
        # 按下左键时移动鼠标
        if mouse_event.buttons() & QtCore.Qt.LeftButton:
            self.move(mouse_event.globalPos() - self.point)


def format_size(size: int) -> str:
    """ 返回以KB 或 MB表示的文件大小, size: 字节数"""
    if size < 1024 * 1024:
        size = str(int(size / 1024)) + "KB"
    else:
        size = str(round(size / 1024 / 1024, 1)) + "MB"
    return size


def init_app_attribute():
    app.root = os.path.split(sys.argv[0])[0]


def main():
    app_ = QtWidgets.QApplication(sys.argv)
    init_app_attribute()
    file_path = ""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    main_window = MainWindow(file_path)
    main_window.show()
    sys.exit(app_.exec_())


if __name__ == "__main__":
    main()
