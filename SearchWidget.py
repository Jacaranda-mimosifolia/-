# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import qdarkstyle
from BilibiliSpider import BilibiliSpider

class searchWidget(QtWidgets.QWidget):
    is_url_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(searchWidget, self).__init__(parent)
        self.setupUi()


    def setupUi(self):
        # 初始化
        self.resize(800, 600)  # 窗口大小
        font = QtGui.QFont()  # 统一字体

        # 主布局
        self.vbox = QtWidgets.QVBoxLayout(self)  # 设置垂直布局
        self.vbox.setSpacing(0)  # 垂直间距

        # 标题
        self.titleLabel = QtWidgets.QLabel(self)
        font.setPointSize(30)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)  # 居中
        self.vbox.addWidget(self.titleLabel)

        # 表布局
        self.formlayout = QtWidgets.QFormLayout(self)
        self.formlayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)  # 水平居中，垂直靠上
        self.formlayout.setHorizontalSpacing(10)
        self.formlayout.setVerticalSpacing(10)
        font.setPointSize(15)
        font.setBold(False)

        # 搜索文本框
        self.fontEdit = QtWidgets.QLineEdit(self)
        self.fontEdit.setFont(font)
        self.fontEdit.setAlignment(QtCore.Qt.AlignHCenter)
        self.fontEdit.setPlaceholderText("请输入B站网址连接")
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fontEdit)

        # 搜索按钮
        self.ensureButton = QtWidgets.QPushButton(self)
        # self.ensureButton.setMaximumSize(QtCore.QSize(100, 30))
        self.ensureButton.setFont(font)
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ensureButton)
        self.vbox.addLayout(self.formlayout)

        # 导入文本
        self.transferText()

        # 事件触发
        QtCore.QMetaObject.connectSlotsByName(self)
        self.ensureButton.clicked.connect(self.getURL)
        self.fontEdit.returnPressed.connect(self.getURL)

    def transferText(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("SearchWidget", "bilibilispider"))
        self.titleLabel.setText(_translate("SearchWidget", "bilibilispider"))
        self.ensureButton.setText(_translate("SearchWidget", "Search"))

    def getURL(self):
        url = self.fontEdit.text()
        for index, value in enumerate(url):
            if value == "?":
                url = url[:index]
        print(url)
        if url[:31] != "https://www.bilibili.com/video/":
            print(QMessageBox.warning(self, "警告", "请输入正确的b站视频网址", QMessageBox.Yes))
            self.fontEdit.setText("")
            return
        if BilibiliSpider(url).response[:17] == "404 Client Error:":
            print(QMessageBox.warning(self, "警告", "找不到该视频,请重新输入", QMessageBox.Yes))
            self.fontEdit.setText("")
            return
        self.is_url_signal.emit(url)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.ico"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    mainMindow = searchWidget()
    mainMindow.show()
    sys.exit(app.exec_())
