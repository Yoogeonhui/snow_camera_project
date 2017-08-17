# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from definederror import definederror
import os, main
import shutil

import subprocess

class draw_sticker(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi("draw_sticker.ui", self)
        self.ui.show()

        self.combo = self.ui.comboBox
        self.line = self.ui.lineEdit
        self.combo.addItem("눈") #0
        self.combo.addItem("코") #1
        self.combo.addItem("입") #2
    @pyqtSlot()
    def draw_sticker(self):
        try:
            if(self.line.text()==''):
                raise definederror("이름이 공백입니다. 기입해주세요")
            directory = './sticker/'
            origin = 'landmark_checked_'
            currIndex = self.combo.currentIndex()
            if currIndex== 0:
                directory +='eye/'
                origin += 'eye'
            if currIndex == 1:
                directory +='nose/'
                origin += 'nose'
            if currIndex ==2:
                directory+='mouth/'
                origin +='mouth'
            origin += r'.png'
            if not os.path.exists(directory):
                os.makedirs(directory)
            directory += self.line.text()+r'.png'
            if os.path.isfile(directory):
                raise definederror("동일한 이름의 스티커가 존재합니다! 이름을 바꿔주세요")
            shutil.copy2(origin, directory)
            with open('sai_tool.txt', 'r') as f:
                sai_root = f.readline()
            subprocess.Popen([sai_root, os.path.abspath(directory)],shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)

        except definederror as e:
            QMessageBox.warning(self, e.__str__(), e.__str__(), QMessageBox.Ok)
