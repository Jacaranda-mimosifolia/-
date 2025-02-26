# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys
import qdarkstyle
from SearchWidget import searchWidget
from DownloadWidget import DownloadWidget
import sip


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.widget = None  # widget界面指针
        self.setupUi()

    def setupUi(self):
        # 初始化
        self.resize(800, 600)  # 窗口大小

        # 创建菜单栏
        bar = self.menuBar()
        self.Menu = bar.addMenu("menu")
        # 创建动作
        self.searchAction = QAction("search", self)
        self.downloadAction = QAction("download", self)
        self.quitAction = QAction("quit", self)
        # 将动作添加至菜单栏
        self.Menu.addAction(self.searchAction)
        self.Menu.addAction(self.downloadAction)
        self.Menu.addAction(self.quitAction)

        # 初始化界面
        self.reSearchWidget()

        # 导入文本
        self.transferText()

        # 事件触发
        QtCore.QMetaObject.connectSlotsByName(self)  # 将控件的信号自动与槽函数根据名称objectName进行匹配
        self.Menu.triggered[QAction].connect(self.menuTriggered)

    def transferText(self, ):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("InputURLWidget", "bilibilispider"))
        self.Menu.setTitle(_translate("MainWindow", "menu"))
        self.searchAction.setText(_translate("MainWindow", "search"))
        self.downloadAction.setText(_translate("MainWindow", "download"))
        self.quitAction.setText(_translate("MainWindow", "quit"))

    def reSearchWidget(self):
        self.widget = searchWidget()
        self.setCentralWidget(self.widget)

        # 获取用户输入所返回的信号量，is_url_signal调用reDownloadWidget
        self.widget.is_url_signal.connect(self.reDownloadWidget)

        self.searchAction.setEnabled(False)
        self.downloadAction.setEnabled(False)
        self.quitAction.setEnabled(True)

    def reDownloadWidget(self, url):
        sip.delete(self.widget)
        self.widget = DownloadWidget(url)
        self.setCentralWidget(self.widget)

        # 更新操作,自己调用自己
        self.widget.is_reShowURL_signal.connect(self.reDownloadWidget)

        self.searchAction.setEnabled(True)
        self.downloadAction.setEnabled(False)
        self.quitAction.setEnabled(True)

    def menuTriggered(self, q):
        if q.text() == "search":
            sip.delete(self.widget)
            self.reSearchWidget()
        if q.text() == "quit":
            qApp = QApplication.instance()
            qApp.quit()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.ico"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    mainMindow = mainWindow()
    mainMindow.show()
    sys.exit(app.exec_())
