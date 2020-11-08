#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import pyqtSlot

# import capture tool screen
from captureTool import CaptureTool
# import enter tool screen
from enterTool import EnterTool
# import select tool screen
from selectTool import SelectTool

MainWindowUI, MainWindowBase = uic.loadUiType("main.ui")


class Ui_MainWindow(MainWindowBase, MainWindowUI):
    def __init__(self, parent: QtWidgets.QWidget = None):
        MainWindowBase.__init__(self, parent=parent)
        self.setupUi(self)

        # UI items event connection
        self.captureToolButton.clicked.connect(self.captureToolScreen)
        self.selectToolButton.clicked.connect(self.selectToolScreen)
        self.enterToolButton.clicked.connect(self.enterToolScreen)

    @pyqtSlot(name="captureToolButton")
    def captureToolScreen(self):
        # code for capture tool screen here!
        self.captureTool = CaptureTool()
        self.captureTool.show()

    @pyqtSlot(name="selectToolScreen")
    def selectToolScreen(self):
        # code for select tool screen here!
        self.selectTool = SelectTool()
        self.selectTool.show()

    @pyqtSlot(name="enterToolScreen")
    def enterToolScreen(self):
        # code for enter tool screen here!

        self.enterTool = EnterTool()
        self.enterTool.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.captureToolButton.setText(_translate("MainWindow", "Capture Tool"))
        self.selectToolButton.setText(_translate("MainWindow", "Select Tool"))
        self.enterToolButton.setText(_translate("MainWindow", "Enter Tool"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
