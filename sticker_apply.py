# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal
import cv2
import sched,time
import numpy as np
import sys
import os
import dlib


class Form(QtWidgets.QDialog):
    applied = pyqtSignal(list)

    def __init__(self, mylist,  parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.checkstate=[]
        self.ui = uic.loadUi("sticker_apply.ui",self)
        self.ui.eyeBox.setCheckState(mylist[0])
        self.ui.noseBox.setCheckState(mylist[2])
        self.ui.mouthBox.setCheckState(mylist[4])
        for i in range(0, 3):
            self.checkstate.append(mylist[2 * i])
        if mylist[0]:
            for (i, name) in enumerate(os.listdir("./sticker/eye")):

                self.ui.eyeCombo.addItem(name)
                if name == mylist[1]:
                    self.ui.eyeCombo.setCurrentIndex(i)
        else:
            self.ui.eyeCombo.setEnabled(False)

        if mylist[2]:
            for (i, name) in enumerate(os.listdir("./sticker/nose")):

                self.ui.noseCombo.addItem(name)
                if name == mylist[3]:
                    self.ui.noseCombo.setCurrentIndex(i)
        else:
            self.ui.noseCombo.setEnabled(False)

        if mylist[4]:
            for (i, name) in enumerate(os.listdir("./sticker/mouth")):

                self.ui.mouthCombo.addItem(name)
                if name == mylist[5]:
                    self.ui.mouthCombo.setCurrentIndex(i)
        else:
            self.ui.mouthCombo.setEnabled(False)
        self.ui.show()

    def update_checked(self, combobox, loc):
        for i in os.listdir(loc):
            combobox.addItem(i)
    @pyqtSlot()
    def change_enabled(self):
        if self.checkstate[0] != self.ui.eyeBox.checkState():
            self.checkstate[0] = self.ui.eyeBox.checkState()
            if self.checkstate[0]:
                self.ui.eyeCombo.setEnabled(True)
                self.update_checked(self.ui.eyeCombo, "./sticker/eye")
            else:
                self.ui.eyeCombo.clear()
                self.ui.eyeCombo.setEnabled(False)
        if self.checkstate[1] != self.ui.noseBox.checkState():
            self.checkstate[1] = self.ui.noseBox.checkState()
            if self.checkstate[1]:
                self.ui.noseCombo.setEnabled(True)
                self.update_checked(self.ui.noseCombo, "./sticker/nose")
            else:
                self.ui.noseCombo.clear()
                self.ui.noseCombo.setEnabled(False)

        if self.checkstate[2] != self.ui.mouthBox.checkState():
            self.checkstate[2] = self.ui.mouthBox.checkState()
            if self.checkstate[2]:
                self.ui.mouthCombo.setEnabled(True)
                self.update_checked(self.ui.mouthCombo, "./sticker/mouth")
            else:
                self.ui.mouthCombo.clear()
                self.ui.mouthCombo.setEnabled(False)


    @pyqtSlot()
    def apply_button(self):
        res = []
        res.append(self.checkstate[0])
        res.append(self.ui.eyeCombo.currentText())
        res.append(self.checkstate[1])
        res.append(self.ui.noseCombo.currentText())
        res.append(self.checkstate[2])
        res.append(self.ui.mouthCombo.currentText())
        self.applied.emit(res)
        self.close()