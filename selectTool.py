#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time

from PyQt5 import QtWidgets, uic

# import second capture tool screen
from captureTool2 import CaptureTool2

SelectToolUI, SelectToolWindowBase = uic.loadUiType("selectTool.ui")


class SelectTool(SelectToolUI, SelectToolWindowBase):
    def __init__(self, parent: QtWidgets.QWidget = None):
        SelectToolWindowBase.__init__(self, parent=parent)
        self.setupUi(self)

        # UI items event connection
        self.exitButton.clicked.connect(self.closescr)
        #self.captureButton.clicked.connect(self.secondCaptureScreen)
        self.startButton.clicked.connect(self.startExample)

    def secondCaptureScreen(self):
        self.captureTool2 = CaptureTool2()
        self.captureTool2.show()

    def closescr(self):
        # hide screen on exit button click
        self.hide()
        
    def torqueout(self):
        EMULATE_HX711 = False

        referenceUnit = 0.073

        if not EMULATE_HX711:
            import RPi.GPIO as GPIO
            from hx711 import HX711
        else:
            from emulated_hx711 import HX711

        def cleanAndExit():
            print("Cleaning...")

            if not EMULATE_HX711:
                GPIO.cleanup()

            print("Clean!")
            #sys.exit()

        hx = HX711(5, 6)

        hx.set_reading_format("MSB", "MSB")

        hx.set_reference_unit(referenceUnit)

        hx.reset()

        hx.tare()

        print("Tare done! Add weight now...")

        count = 0

        while (count < 11):
            
            value = hx.get_weight(5)
            print(value)
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
            count = count + 1
            self.torqueNumber.setText(str(value))
            
            
        print("Your final value is: ", value)
       
        cleanAndExit()
        
        self.torqueNumber.setText(str(value))
    
    def startExample(self):
        
        # print("In startExample!")
        # x = 2 ** 5
        # self.torqueNumber.setText(str(x))

        #print(self.selectToolBox.currentText())
        model = self.selectToolBox.currentText()
        if model == "2867-20":
            tq = 1200
            tqhi = tq * 1.1
            tqlow = tq * .9
            self.modelNumber.setText(str(model))
            self.hiNumber.setText(str(tqhi))
            self.lowNumber.setText(str(tqlow))
            self.torqueout()
            tqactual = self.torqueNumber.text()
            if str(tqhi) > tqactual > str(tqlow):
                print("Pass")
            else:
                print("Fail")

        if model == "2865-20":
            tq = 750
            tqhi = tq * 1.1
            tqlow = tq * .9
            self.modelNumber.setText(str(model))
            self.hiNumber.setText(str(tqhi))
            self.lowNumber.setText(str(tqlow))
            self.torqueout()
            tqactual = self.torqueNumber.text()
            if str(tqhi) > tqactual > str(tqlow):
                print("Pass")
            else:
                print("Fail")

        if model == "2820-20":
            tq = 775
            tqhi = tq * 1.1
            tqlow = tq * .9
            self.modelNumber.setText(str(model))
            self.hiNumber.setText(str(tqhi))
            self.lowNumber.setText(str(tqlow))
            # call function to read torque
            self.torqueout()
            tqactual = self.torqueNumber.text()
            if str(tqhi) > tqactual > str(tqlow):
                print("Pass")
            else:
                print("Fail")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    selectTool = SelectTool()
    selectTool.show()
    sys.exit(app.exec_())
