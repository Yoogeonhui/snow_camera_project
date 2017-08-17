from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot,Qt
import main



class ConfigForm(QtWidgets.QDialog):
    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("config.ui", self)
        self.ui.show()

    @pyqtSlot()
    def apply(self):
        main.res_x = int(self.ui.resx.text())
        main.res_y = int(self.ui.resy.text())
        main.fps = int(self.ui.fps.text())
        main.cap_num = int(self.ui.capnum.text())
