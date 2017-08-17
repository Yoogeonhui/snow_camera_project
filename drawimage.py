# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
import numpy as np
import cv2, os
import myutility
from definederror import definederror
import shutil
import subprocess

class drawimage(QtWidgets.QDialog):
    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("drawimage.ui", self)
        self.ui.show()


    @pyqtSlot()
    def savephoto(self):
        try:
            dirname = self.ui.maskname.text()
            if dirname == '':
                raise definederror("이름이 비어있습니다. 이름을 지정해주세요.")
            directory = "./save/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            directory = directory+dirname+'/'
            if os.path.exists(directory):
                raise definederror("동일한 이름이 존재합니다.")
            os.makedirs(directory)
            with open(directory+"fileLoc.txt",'w') as file:
                file.write(os.path.abspath(directory+dirname+'.png'))
            shutil.copy2("./landmark_checked.txt", directory+"landmarks.txt")
            shutil.copy2("./landmark_checked.png", directory+dirname+'.png')
            with open('sai_tool.txt', 'r') as f:
                sai_root = f.readline()
            subprocess.Popen([sai_root, os.path.abspath(directory+dirname+'.png')], shell=True, stdin=None, stdout=None, stderr=None,
                                close_fds=True)
        except definederror as e:
            QMessageBox.warning(self, e.__str__(), e.__str__(), QMessageBox.Ok)

