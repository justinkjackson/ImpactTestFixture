#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtWidgets, uic

os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen

import re
import cv2
import numpy as np
from pytesseract import image_to_string
from PIL import Image  # To install: conda install -c anaconda pillow
from time import sleep
from picamera import PiCamera
import matplotlib.pyplot as plt
import time

# import second capture tool screen

CaptureToolUI, CaptureToolWindowBase = uic.loadUiType("captureTool.ui")


class CaptureTool(CaptureToolUI, CaptureToolWindowBase):
    def __init__(self, parent: QtWidgets.QWidget = None):
        CaptureToolWindowBase.__init__(self, parent=parent)
        self.setupUi(self)

        # UI items event connection
        self.captureButton_2.clicked.connect(self.capturecode)
        self.startButton_2.clicked.connect(self.tooltest)
        self.exitButton.clicked.connect(self.closescr)

    # def secondCaptureScreen(self):
    # self.captureTool2 = CaptureTool2()
    # self.captureTool2.show()

    def capturecode(self):

        def load_image(fname):
            # Load image
            # print("Loading image", fname)
            x = Image.open(fname)
            x = np.array(x).astype('float32')

            return x

        #
        # Convert RGB image to grayscale
        #
        def rgb_to_grayscale(x):
            # Extract R,G,B channels
            r = x[:, :, 0]
            g = x[:, :, 1]
            b = x[:, :, 2]

            # Form grayscale image
            gr = 0.2989 * r + 0.5870 * g + 0.1140 * b

            gr_max = np.max(gr)
            gr_min = np.min(gr)

            gr = 255 * (gr - gr_min) / (gr_max - gr_min)
            gr = gr.astype(np.uint8)

            return gr

        # raspberry pi code to grab image
        camera = PiCamera()
        # camera.rotation = 180
        camera.start_preview()
        sleep(5)
        camera.capture('/home/pi/Desktop/image.jpg')
        camera.stop_preview()

        image_fname = ['/home/pi/Desktop/image']

        # image_fname = Image.ope('/home/pi/Desktop/image.jpg')

        # Set up path so pytesseract can run
        #
        # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

        #
        # Custom options pytesseract
        #
        custom_oem_psm_config = r' --psm 11 --user-patterns /home/pi/Desktop/GUIcode/SrDesign_Milwaukee/serial.patterns'

        #
        # Process images
        #
        for im in image_fname:

            # Load RGB image and convert to grayscale
            x = load_image(im + ".jpg")
            xg = rgb_to_grayscale(x)

            # The cat number should be in this portion of the image
            xg2 = xg[459:849, 599:1199]

            # Run contrast limited adpative histogram equalization (CLAHE)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            xgc = clahe.apply(xg2)
            
            #add in the matplotlib code to check for tool placement
            #fig = plt.figure(figsize=(14,8))
            #ax1 = plt.subplot(221)
            #ax2 = plt.subplot(222)
            #ax3 = plt.subplot(223)
            #ax4 = plt.subplot(224)
            #ax1.imshow(x[:,:,0])
            #ax2.imshow(xg)
            #ax3.imshow(xg2)
            #ax4.imshow(xgc)
            
            #ax1.set_title('Original:(red channel)' + im)
            #ax2.set_title('Grayscale')
            #ax3.set_title('Zoom')
            #ax4.set_title('CLAHE Zoom')
        
        #plt.draw()
        #plt.show(block=False)
        #plt.pause(1.0)

        #
        # Search for the Serial Number
        #
        text1 = image_to_string(xgc, config=custom_oem_psm_config)
        text2 = image_to_string(xg2, config=custom_oem_psm_config)
        text12 = text1 + text2

        num_match12 = re.findall("[\d][\d][\d][\d][-][\d][\d]", text12)

        # output can be linked to screen showing match (even without the text)
        if len(num_match12) > 0:
            # instead of printing to screen, print to text box on gui
            print(num_match12[0])
        else:
            print("No match.")

        print("\n")

        pre_out = num_match12[0]

        if pre_out == "2664-20":
            self.modelTextEdit.setText(str(pre_out))

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

        if model == "2664-20":
            tq = 525
            tqhi = tq * 1.1
            tqlow = tq * .9
            self.modelTextEdit.setText(str(model))
            self.hiTextEdit.setText(str(tqhi))
            self.lowTextEdit.setText(str(tqlow))

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
            # call function to read torque
            self.torqueout()
            tqactual = self.torqueNumber.text()
            if str(hi) > tqactual > str(low):
                print("Pass")
            else:
                print("Fail")

    def closescr(self):
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    captureTool = CaptureTool()
    captureTool.show()
    sys.exit(app.exec_())
