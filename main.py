# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot,Qt
import cv2
import sched,time
import numpy as np
import sys
import os
import dlib
import Camera, login, bringImage,drawimage, draw_sticker

fps = 30
res_x = 640
res_y = 480
cap_num = 0

class Form(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.ui = uic.loadUi("form.ui",self)
        self.ui.show()
    @pyqtSlot()
    def draw_image(self):
        tmp = drawimage.drawimage()
        tmp.exec_()

    @pyqtSlot()
    def take_camera(self):
        tmp=Camera.Camera_Form()
        tmp.exec_()

    @pyqtSlot()
    def configure(self):
        tmp = login.LoginForm()
        tmp.exec_()

    @pyqtSlot()
    def get_image(self):
        tmp = bringImage.ImageForm()
        tmp.exec_()

    @pyqtSlot()
    def draw_sticker(self):
        tmp = draw_sticker.draw_sticker()
        tmp.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w=Form()
    sys.exit(app.exec_())