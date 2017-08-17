# -*- coding: utf-8 -*-
import urllib2
import json
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import QMessageBox
import dlib
import numpy as np
import cv2
from imutils import face_utils
import myutility
import os
from definederror import definederror

class ImageForm(QtWidgets.QDialog):
    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi("bringImage.ui",self)
        self.faces = []
        self.face_landmarks = []
        self.name = ""
        self.mycombo = self.ui.combo
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    @pyqtSlot()
    def findphoto(self):
        try:
            self.name = QtWidgets.QFileDialog.getOpenFileName(self, '사진 지정하기')[0]
            if self.name == '':
                raise definederror("파일을 지정하지 않았습니다.")
            self.faces=[]
            self.face_landmarks = []

            with open(self.name, 'rb') as f:
                content=f.read()
            try:
                req = urllib2.Request("https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=false", content, {'Content-Type': 'application/octet-stream'})
                req.add_header('Ocp-Apim-Subscription-Key','b6b816dda0814cbba32c033f7b30fb83')
                response = urllib2.urlopen(req)
                gotdata = response.read()
                dict = json.loads(gotdata)
                for h in dict:
                    print(h)
                    tmp = h['faceRectangle']
                    save = []
                    save.append(int(tmp["top"]))
                    save.append(int(tmp["left"]))
                    save.append(int(tmp["width"]))
                    save.append(int(tmp["height"]))
                    self.faces.append(save)
                print(self.faces)
                mat = np.fromstring(content, dtype=np.uint8)
                img_np = cv2.imdecode(mat, cv2.IMREAD_COLOR)
                for (i, theface) in enumerate(self.faces):
                    f_y = theface[0]
                    f_x = theface[1]
                    f_w = theface[2]
                    f_h = theface[3]
                    cv2.rectangle(img_np, (f_x, f_y),
                                  (f_x + f_w, f_y + f_h),
                                  (0, 255, 0), 2)
                    cv2.putText(img_np, "Face #{}".format(i + 1), (f_x - 10, f_y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
                    shape = self.predictor(gray, dlib.rectangle(f_x, f_y, f_x + f_w, f_y + f_h))
                    shape = face_utils.shape_to_np(shape)
                    lands = []
                    for (x, y) in shape:
                        cv2.circle(img_np, (x, y), 1, (0, 0, 255), -1)
                        lands.append((x, y))
                    self.face_landmarks.append(lands)

                rect= self.ui.label.frameRect()
                display = cv2.resize(img_np, (rect.width(),rect.height()) )
                self.ui.label.setPixmap(myutility.conv2QPixmap(display))
                for i in range(1, len(self.faces)+1):
                    self.mycombo.addItem(str(i)+"번 얼굴")

            except urllib2.URLError, e:
                QMessageBox.warning(self, "에러 발생",
                                    '망했어요, 부스 관계자가 갈리는 소리가 들리는군요. 이걸 부스 관계자에게 보여주시죠! (공밀레..)'+str(e.reason),
                                    QMessageBox.Ok)
        except definederror as e:
            QMessageBox.warning(self,e.__str__(),e.__str__(),QMessageBox.Ok)
    @pyqtSlot()
    def savephoto(self):
        try:
            if self.name=="":
                raise definederror("파일을 불러온 적이 없습니다.")
            dirname = self.ui.maskname.text()
            facenum = self.mycombo.currentIndex()
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
                file.write(self.name)
            with open(directory+"landmarks.txt",'w') as file:
                locland = self.face_landmarks[facenum]
                for i in locland:
                    file.write(str(i[0])+' '+str(i[1])+'\n')
        except definederror as e:
            QMessageBox.warning(self, e.__str__(), e.__str__(), QMessageBox.Ok)

