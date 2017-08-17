# -*- coding: utf-8 -*-
import urllib2
from imutils import face_utils
import cv2
import numpy as np
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox, QWidget
import myutility
import json
import dlib
import os
res_x = 1280
res_y = 720

def applyAffineTransform(src, srcTri, dstTri, size):
    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))

    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine(src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_REFLECT_101)

    return dst

def binarysearch(what, array):
    l=0
    r=255
    while(l<r):
        m=(l+r)//2
        if(what>array[m]):
            l=m+1
        else:
            r=m-1
    return m

def calculateDelaunayTriangles(rect, points):
    # create subdiv
    subdiv = cv2.Subdiv2D(rect)

    # Insert points into subdiv
    for p in points:
        subdiv.insert(p)

    triangleList = subdiv.getTriangleList()

    delaunayTri = []

    pt = []

    count = 0

    for t in triangleList:
        pt.append((t[0], t[1]))
        pt.append((t[2], t[3]))
        pt.append((t[4], t[5]))

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rectContains(rect, pt1) and rectContains(rect, pt2) and rectContains(rect, pt3):
            count = count + 1
            ind = []
            for j in xrange(0, 3):
                for k in xrange(0, len(points)):
                    if (abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0):
                        ind.append(k)
            if len(ind) == 3:
                delaunayTri.append((ind[0], ind[1], ind[2]))

        pt = []

    return delaunayTri

def rectContains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[0] + rect[2]:
        return False
    elif point[1] > rect[1] + rect[3]:
        return False
    return True

def check_validate(rect):
    (x,y,w,h) = rect
    bef_x_w = x+w
    bef_y_h = y+h
    x = max(0, min(x, res_x))
    y = max(0, min(y, res_y))
    bef_x_w = max(0, min(bef_x_w, res_x))
    bef_y_h = max(0, min(bef_y_h, res_y))
    return (x,y,bef_x_w-x , bef_y_h-y )

def warpTriangle(img1, img2, t1, t2):
    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    #x,y,w,h


    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    t2RectInt = []

    for i in xrange(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
    r2 = check_validate(r2)
    if r1[2] >0 and r1[3]>0 and r2[2]>0 and r2[3]>0:
        # Get mask by filling triangle
        zeromask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
        cv2.fillConvexPoly(zeromask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0);
        # Apply warpImage to small rectangular patches
        img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
        # img2Rect = np.zeros((r2[3], r2[2]), dtype = img1Rect.dtype)

        size = (r2[2], r2[3])

        img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)
        img2Rect = img2Rect * zeromask
        # Copy triangular region of the rectangular patch to the output image
        img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * (
        (1.0, 1.0, 1.0) - zeromask)
        img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] + img2Rect

def putsticker(sticker ,base):
    tmpalpha = sticker[:, :, 3]
    tmpalpha = cv2.cvtColor(tmpalpha, cv2.COLOR_GRAY2BGR)
    tmpalpha = tmpalpha.astype(float) / 255
    front = sticker[:, :, 0:3].astype(float)
    front = cv2.multiply(tmpalpha, front)
    back = base.astype(float)
    back = cv2.multiply(1.0 - tmpalpha, back)
    #back = cv2.cvtColor(np.uint8(back), cv2.COLOR_BGR2RGB)
    outimage = cv2.add(front, back)
    return cv2.cvtColor(np.uint8(outimage), cv2.COLOR_RGB2BGR)

class ConfirmForm(QtWidgets.QDialog):
    def __init__(self, originframe, sticker, predictor, rx,ry, parent = None):
        QDialog.__init__(self, parent)
        self.ui = uic.loadUi("confirm.ui", self)
        print('a')
        global res_x, res_y
        self.sticker =sticker
        self.frame = originframe
        print('b')
        if self.sticker is not None:
            self.sticker = cv2.cvtColor(self.sticker, cv2.COLOR_RGBA2BGRA)
            self.saved = putsticker(self.sticker,self.frame)
        else:
            self.saved = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
        print('c')
        self.ui.comboBox.addItem("적용하지 않습니다.")
        print('d')
        for i in os.listdir("./save"):
            self.ui.comboBox.addItem(i)
        print('e')
        self.ui.show()
        print('asdf')
        self.ui.label.setPixmap(myutility.conv2QPixmap(self.saved))
        print('zxcv')
        self.predictor = predictor
        self.faces = []
        self.face_landmarks = []
        self.detected = False
        res_x = rx
        res_y = ry



    def apply_mask(self):
        self.saved= self.frame
        currentind = self.ui.comboBox.currentIndex()
        currenttext = self.ui.comboBox.currentText()
        if currentind != 0:
            mask_landmarks = []

            if not self.detected:
                _, content = cv2.imencode('.png', self.frame)
                try:
                    req = urllib2.Request("https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=false",
                                          content, {'Content-Type': 'application/octet-stream'})
                    req.add_header('Ocp-Apim-Subscription-Key', 'b6b816dda0814cbba32c033f7b30fb83')
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
                    for (i, theface) in enumerate(self.faces):
                        f_y = theface[0]
                        f_x = theface[1]
                        f_w = theface[2]
                        f_h = theface[3]
                        gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
                        shape = self.predictor(gray, dlib.rectangle(f_x, f_y, f_x + f_w, f_y + f_h))
                        shape = face_utils.shape_to_np(shape)
                        lands = []
                        for (x, y) in shape:
                            lands.append((x, y))
                        self.face_landmarks.append(lands)
                except urllib2.URLError, e:
                    QMessageBox.warning(self, "에러 발생",
                                        '망했어요, 부스 관계자가 갈리는 소리가 들리는군요. 이걸 부스 관계자에게 보여주시죠! (공밀레..)'+str(e.reason),
                                        QMessageBox.Ok)

            with open("./save/" + currenttext + "/fileLoc.txt", 'r') as f:
                fileloc = f.readline()
                print(fileloc)
            mask = cv2.imread(fileloc)

            with open("./save/" + currenttext + "/landmarks.txt", 'r') as f:
                for line in f:
                    if line != '':
                        x, y = line.split()
                        mask_landmarks.append((int(x), int(y)))
            for fid in self.face_landmarks:
                srcWarped= np.copy(self.frame)
                hull1 = []
                hull2 = []

                hullIndex = [15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,18,19,20,23,25,26]
                for i in xrange(0, len(hullIndex)):
                    hull1.append(mask_landmarks[int(hullIndex[i])])
                    hull2.append(fid[int(hullIndex[i])])

                dt=[(5, 8, 9), (8, 5, 7), (13, 18, 1), (18, 13, 14), (5, 9, 4), (0, 1, 18), (7, 5, 6), (1, 2, 13), (2, 3, 11),
                 (3, 4, 9), (3, 9, 10), (3, 10, 11), (2, 11, 12), (2, 12, 13), (18, 14, 16), (18, 16, 17), (16, 14, 15),
                 (0, 18, 19), (0, 19, 21), (21, 19, 20)]

                if len(dt) !=0:
                    for i in xrange(0, len(dt)):
                        t1 = []
                        t2 = []
                        # get points for img1, img2 corresponding to the triangles
                        for j in xrange(0, 3):
                            t1.append(hull1[dt[i][j]])
                            t2.append(hull2[dt[i][j]])
                        warpTriangle(mask, srcWarped, t1, t2)
                    hull8U = []
                    for i in xrange(0, len(hull2)):
                        hull8U.append((hull2[i][0], hull2[i][1]))
                    mask_zeros = np.zeros(self.frame.shape, dtype=self.frame.dtype)
                    cv2.fillConvexPoly(mask_zeros, np.int32(hull8U), (255, 255, 255))
                    r = cv2.boundingRect(np.float32([hull2]))
                    r = check_validate(r)
                    # Clone seamlessly.
                    center = ((r[0] + int(r[2] / 2), r[1] + int(r[3] / 2)))
                    self.saved = cv2.seamlessClone(cv2.cvtColor(np.uint8(srcWarped),cv2.COLOR_RGB2BGR), self.saved, mask_zeros, center, cv2.NORMAL_CLONE)
            if self.sticker is not None:
                print('asdf')
                self.saved = putsticker(self.sticker, self.saved)
            else:
                print('zxcv')
                self.saved = cv2.cvtColor(self.saved, cv2.COLOR_RGB2BGR)
            self.ui.label.setPixmap(myutility.conv2QPixmap(self.saved))



    @pyqtSlot()
    def save(self):
        if self.ui.fileName.text()!='':
            cv2.imwrite('./done/'+self.ui.fileName.text()+'.jpg', cv2.cvtColor(self.saved,cv2.COLOR_BGR2RGB))
        else:
            QMessageBox.warning(self, "이름이 공백입니다.",
                                '이름이 공백입니다.',
                                QMessageBox.Ok)