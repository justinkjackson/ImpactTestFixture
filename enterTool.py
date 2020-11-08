#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot

# import second capture tool screen
from captureTool2 import CaptureTool2

EnterToolUI, EnterToolWindowBase = uic.loadUiType("enterTool.ui")


class EnterTool(EnterToolUI, EnterToolWindowBase):
    def __init__(self, parent: QtWidgets.QWidget = None):
        EnterToolWindowBase.__init__(self, parent=parent)
        self.setupUi(self)

        # UI items event connection
        self.exitButton.clicked.connect(self.closescr)
        self.captureButton.clicked.connect(self.secondCaptureScreen)
        self.startButton.clicked.connect(self.tooltest)

    @pyqtSlot(name="closescr")
    def closescr(self):
        # hide screen on exit button click
        self.hide()

    @pyqtSlot(name="secondCaptureScreen")
    def secondCaptureScreen(self):
        self.captureTool2 = CaptureTool2()
        self.captureTool2.show()
        
    def torqueout(self):

        EMULATE_HX711 = False

        referenceUnit = 430

        if not EMULATE_HX711:
            import RPi.GPIO as GPIO
            from hx711 import HX711
        else:
            from emulated_hx711 import HX711

        def cleanAndExit():
            print("Cleaning...")

            if not EMULATE_HX711:
                GPIO.cleanup()

            print("Bye!")
            #sys.exit()

        hx = HX711(5, 6)

        hx.set_reading_format("MSB", "MSB")

        hx.set_reference_unit(referenceUnit)

        hx.reset()

        hx.tare()

        print("Tare done! Add weight now...")

        count = 0

        while (count < 11):
            val = hx.get_weight(5)
            print(val)
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
            count = count + 1
        print("Your final value is: ", val)
        cleanAndExit()
        self.torqueNumber.setText(str(val))


    def tooltest(self):

        model = self.modelTextEdit.toPlainText()
        hi = self.hiTextEdit.toPlainText()
        low = self.lowTextEdit.toPlainText()
        # insert code to pull data from sensor
        self.torqueout()
        tqactual = self.torqueNumber.text()
        if str(hi) > tqactual > str(low):
            print("Pass")
        else:
            print("Fail")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    EnterToolWindow = EnterTool()
    EnterToolWindow.show()
    sys.exit(app.exec_())
