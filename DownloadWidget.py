# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import qdarkstyle
from BilibiliSpider import BilibiliSpider


class DownloadWidget(QtWidgets.QWidget):
    is_reShowURL_signal = pyqtSignal(str)

    def __init__(self, url, parent=None):
        super(DownloadWidget, self).__init__(parent)
        self.url = url
        self.text = self.showInformation()
        self.setupUi()

    def setupUi(self):
        # 初始化
        self.resize(800, 600)  # 窗口大小
        font = QtGui.QFont()  # 统一字体

        # 主布局
        self.vbox = QtWidgets.QVBoxLayout(self)  # 设置垂直布局
        self.vbox.setSpacing(1)  # 垂直间距

        # 表布局
        self.formlayout = QtWidgets.QFormLayout(self)
        self.formlayout.setFormAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)  # 水平居中，垂直靠上
        self.formlayout.setHorizontalSpacing(0)  # 水平间隔
        self.formlayout.setVerticalSpacing(5)  # 垂直间隔

        # 标题
        self.titleLabel = QtWidgets.QLabel(self)
        font.setPointSize(30)
        font.setBold(True)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignHCenter)  # 水平方向居中
        self.formlayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.titleLabel)

        # 搜索文本框
        self.fontEdit = QtWidgets.QLineEdit(self)
        font.setPointSize(12)
        font.setBold(False)
        self.fontEdit.setFont(font)
        self.fontEdit.setAlignment(QtCore.Qt.AlignHCenter)  # 水平方向居中
        self.fontEdit.setPlaceholderText("请输入B站网址连接")  # 输入框中提示
        self.formlayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fontEdit)

        # 搜索按钮
        self.searchButton = QtWidgets.QPushButton(self)
        self.searchButton.setFont(font)
        self.formlayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.searchButton)

        # 显示文本框
        self.textEdit = QtWidgets.QLabel(self)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 250, 250))  # 自适应换行
        self.textEdit.setWordWrap(True)
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setAlignment(QtCore.Qt.AlignLeft)  # 水平方向居左
        self.formlayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.textEdit)
        self.vbox.addLayout(self.formlayout)

        # 水平布局：功能按键
        self.hbox = QtWidgets.QHBoxLayout(self)
        self.hbox.setSpacing(1)
        font.setPointSize(12)

        self.txtButton = QtWidgets.QPushButton(self)
        self.txtButton.setMaximumSize(QtCore.QSize(120, 30))
        self.txtButton.setFont(font)
        self.hbox.addWidget(self.txtButton)
        self.imageButton = QtWidgets.QPushButton(self)
        self.imageButton.setMaximumSize(QtCore.QSize(120, 30))
        self.imageButton.setFont(font)
        self.hbox.addWidget(self.imageButton)
        self.audioButton = QtWidgets.QPushButton(self)
        self.audioButton.setMaximumSize(QtCore.QSize(120, 30))
        self.audioButton.setFont(font)
        self.hbox.addWidget(self.audioButton)
        self.videoButton = QtWidgets.QPushButton(self)
        self.videoButton.setMaximumSize(QtCore.QSize(120, 30))
        self.videoButton.setFont(font)
        self.hbox.addWidget(self.videoButton)

        self.vbox.addLayout(self.hbox)

        # 导入文本
        self.transferText()

        # 事件触发
        QtCore.QMetaObject.connectSlotsByName(self)
        self.searchButton.clicked.connect(self.reShowInformation)
        self.imageButton.clicked.connect(self.downloadImage)
        self.audioButton.clicked.connect(self.downloadAudio)
        self.videoButton.clicked.connect(self.downloadVideo)

    def transferText(self, ):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("DownloadWidget", "bilibilispider"))
        self.titleLabel.setText(_translate("DownloadWidget", "bilibilispider"))
        self.searchButton.setText(_translate("DownloadWidget", "Search"))
        self.textEdit.setText(_translate("DownloadWidget", self.text))
        self.txtButton.setText(_translate("DownloadWidget", "Waiting"))
        self.imageButton.setText(_translate("DownloadWidget", "DownloadImage"))
        self.audioButton.setText(_translate("DownloadWidget", "DownloadAudio"))
        self.videoButton.setText(_translate("DownloadWidget", "DownloadVideo"))

    def showInformation(self):
        bilibiliSpider = BilibiliSpider(self.url)
        if str(bilibiliSpider.response)[:17] == "404 Client Error:":
            print(QMessageBox.warning(self, "警告", "找不到该视频,请重新输入", QMessageBox.Yes))
            return
        text = bilibiliSpider.title + "\n" + bilibiliSpider.getText()
        return text

    def reShowInformation(self):
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
        self.is_reShowURL_signal.emit(url)  # 返回url信号，重调用downloadWidget


    def downloadImage(self):
        print(self.url)
        bilibiliSpider = BilibiliSpider(self.url)
        bilibiliSpider.downloadImage()

    def downloadAudio(self):
        bilibiliSpider = BilibiliSpider(self.url)
        bilibiliSpider.downloadAudio()

    def downloadVideo(self):
        bilibiliSpider = BilibiliSpider(self.url)
        bilibiliSpider.downloadVideo()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.ico"))  # 图标
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())  # 界面美化
    mainMindow = DownloadWidget("https://www.bilibili.com/video/BV1yS411K7s7/")
    mainMindow.show()
    sys.exit(app.exec_())  # 结束
