# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
import config

class LoginForm(QtWidgets.QDialog):
    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("login.ui", self)
        self.ui.show()
    @pyqtSlot()
    def toconfig(self):
        if self.ui.pw.text() =='qntmwkfehofk':
            tmp = config.ConfigForm()
            tmp.exec_()
        else:
            msg = QMessageBox.warning(self, "로그인에 실패하였습니다." , '비밀번호를 확인해주세요, 혹시 참여하시는 분이라면 시도하지 마시고 부스 관계자만 이거 여세요 ㅠㅠ 나중에 당신 눈 앞에 있는 사람들이 골치 썩어요',QMessageBox.Ok )