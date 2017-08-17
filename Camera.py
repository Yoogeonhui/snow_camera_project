# -*- coding: utf-8 -*-
import time
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtGui import *

from PyQt5.QtCore import *
import cv2
import numpy as np
import sys
import dlib
from imutils import face_utils
import os, myutility, sticker_apply, confirm, main

mask_determine = False
mask_landmarks = []
mask = None
fps = 30
res_x = 640
res_y = 480
compute_x = 640
compute_y = 480
cap_num = 0
faceTrackers = {}
eyeFeature = [41,21,46]
noseFeature = [28,31,35]
mouthFeature = [48,57,54]

def cap_res(cap,x=1280 ,y=720 , myfps=30):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
    cap.set(cv2.CAP_PROP_FPS, int(myfps))


class Camera_Thread(QThread):

    label_changed = pyqtSignal(list)

    def load_features(self,num):
        dir = './sticker/'
        if num == 0:
            dir+='eye/'
        if num ==1:
            dir+='nose/'
        if num==2:
            dir+='mouth/'
        dir+=self.mylist[num*2+1]
        print(dir)
        self.sticker_load[num] = cv2.imread(dir, cv2.IMREAD_UNCHANGED)
        for i in range(self.sticker_load[num].shape[0]):
            for j in range(self.sticker_load[num].shape[1]):
                if self.sticker_load[num][i,j][0] == 11 and self.sticker_load[num][i, j][1] == 53 and self.sticker_load[num][i, j][2] == 64:
                    self.sticker_load[num][i,j] = [0,0,0,0]


    def __init__(self, predictor, detector, mylist):
        global fps, res_x, res_y, cap_num
        fps = main.fps
        res_x = main.res_x
        res_y = main.res_y
        cap_num = main.cap_num
        QThread.__init__(self, parent=None)
        self.stickerapply = False
        self.cap = cv2.VideoCapture(cap_num)
        cap_res(self.cap, res_x, res_y, fps)
        self.predictor = predictor
        self.detector = detector
        self.count = 0
        self.currentFaceID = 0
        self.stop = False
        self.sticker_landmarks=[]
        self.sticker_tri =[[],[],[]]
        self.mylist=mylist
        self.sticker_load = [None, None, None]
        self.sticker_zero = None
        with open('landmark_checked.txt', 'r') as f:
            for line in f:
                a,b = line.split()
                self.sticker_landmarks.append((int(a), int(b)))
        for i in eyeFeature:
            self.sticker_tri[0].append(self.sticker_landmarks[i])
        for i in noseFeature:
            self.sticker_tri[1].append(self.sticker_landmarks[i])
        for i in mouthFeature:
            self.sticker_tri[2].append(self.sticker_landmarks[i])
        for i in range(0,3):
            if mylist[2*i]:
                self.load_features(i)

    @pyqtSlot(list)
    def sticker_changed(self, mylist):
        for i in range(0,3):
            if mylist[i*2] != self.mylist[i*2]:
                self.mylist[i*2]= mylist[i*2]
                self.mylist[i*2+1] = mylist[i*2+1]
                if(self.mylist[i*2]):
                    self.load_features(i)

    def apply(self):
        global mask, mask_landmarks, mask_determine
        fidsToDelete = []
        self.stickerapply = False
        # loop over the face detections
        frame_to_gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        for fid in faceTrackers.keys():
            trackingQuality = faceTrackers[fid].update(frame_to_gray)

            # If the tracking quality is good enough, we must delete
            # this tracker
            if trackingQuality < 6.5:
                fidsToDelete.append(fid)
        for fid in fidsToDelete:
            print("Removing fid " + str(fid) + " from list of trackers")
            faceTrackers.pop(fid, None)
        if self.count == 0:
            rects = self.detector.detectMultiScale(self.gray,1.5,6)
            for (i, rect) in enumerate(rects):
                '''
                rects = self.detector.detectMultiScale(self.gray)
                for (i, rect) in enumerate(rects):
                #(x, y, w, h) = face_utils.rect_to_bb(rect)
                (x,y,w,h) = rect
                x = int(x*float(res_x)/compute_x)
                w = int(w*float(res_x)/compute_x)
                y = int(y * float(res_y) / compute_y)
                h = int(h * float(res_y) / compute_y)
                '''
                (x, y, w, h) = rect
                x = int(x)
                y = int(y)
                w = int(w)
                h = int(h)
                x_bar = x + 0.5 * w
                y_bar = y + 0.5 * h
                matchedFid = None
                for fid in faceTrackers.keys():
                    tracked_position = faceTrackers[fid].get_position()

                    t_x = int(tracked_position.left())
                    t_y = int(tracked_position.top())
                    t_w = int(tracked_position.width())
                    t_h = int(tracked_position.height())

                    # calculate the centerpoint
                    t_x_bar = t_x + 0.5 * t_w
                    t_y_bar = t_y + 0.5 * t_h
                    if ((t_x <= x_bar <= (t_x + t_w)) and
                            (t_y <= y_bar <= (t_y + t_h)) and
                            (x <= t_x_bar <= (x + w)) and
                            (y <= t_y_bar <= (y + h))):
                        matchedFid = fid
                if matchedFid is None:
                    print("Creating new tracker " + str(self.currentFaceID))

                    # Create and store the tracker
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(frame_to_gray,
                                        dlib.rectangle(x - 10,
                                                       y - 20,
                                                       x + w + 10,
                                                       y + h + 20))

                    faceTrackers[self.currentFaceID] = tracker
                    self.currentFaceID += 1

        for fid in faceTrackers.keys():
            tracked_position = faceTrackers[fid].get_position()
            t_x = int(tracked_position.left())
            t_y = int(tracked_position.top())
            t_w = int(tracked_position.width())
            t_h = int(tracked_position.height())
            a = dlib.rectangle(t_x, t_y, t_x + t_w, t_y + t_h)
            shape = self.predictor(frame_to_gray, a)
            shape = face_utils.shape_to_np(shape)
            frame_landmarks = []
            for (x, y) in shape:
                frame_landmarks.append((x,y))
            self.sticker_zero = np.zeros([res_y,res_x,4],dtype = np.uint8)
            if self.mylist[0]:
                self.stickerapply = True
                eyeTri = []
                for i in eyeFeature:
                    eyeTri.append(frame_landmarks[i])
                M = cv2.getAffineTransform(np.float32(self.sticker_tri[0]), np.float32(eyeTri))
                Warped = cv2.warpAffine(self.sticker_load[0], M, (res_x,res_y))
                myalpha = cv2.cvtColor(Warped[:,:,3],cv2.COLOR_GRAY2BGR)/255.0
                Warped[:,:,:3] = cv2.multiply(myalpha,(Warped[:,:,:3]).astype(float))
                self.sticker_zero = cv2.add(self.sticker_zero, Warped)

            if self.mylist[2]:
                self.stickerapply = True
                noseTri = []
                for i in noseFeature:
                    noseTri.append(frame_landmarks[i])
                M = cv2.getAffineTransform(np.float32(self.sticker_tri[1]), np.float32(noseTri))
                Warped = cv2.warpAffine(self.sticker_load[1], M, (res_x,res_y))
                myalpha = cv2.cvtColor(Warped[:, :, 3], cv2.COLOR_GRAY2BGR) / 255.0
                Warped[:, :, :3] = cv2.multiply(myalpha, (Warped[:, :, :3]).astype(float))
                self.sticker_zero = cv2.add(self.sticker_zero, Warped)

            if self.mylist[4]:
                self.stickerapply = True
                mouthTri = []
                for i in mouthFeature:
                    mouthTri.append(frame_landmarks[i])
                M = cv2.getAffineTransform(np.float32(self.sticker_tri[2]), np.float32(mouthTri))
                Warped = cv2.warpAffine(self.sticker_load[2], M, (res_x,res_y))
                myalpha = cv2.cvtColor(Warped[:, :, 3], cv2.COLOR_GRAY2BGR) / 255.0
                Warped[:, :, :3] = cv2.multiply(myalpha, (Warped[:, :, :3]).astype(float))
                self.sticker_zero = cv2.add(self.sticker_zero, Warped)
            tmpalpha = self.sticker_zero[:, :, 3]
            tmpalpha = cv2.cvtColor(tmpalpha, cv2.COLOR_GRAY2BGR)/255.0
            front = self.sticker_zero[:,:,0:3].astype(float)
            front = cv2.multiply(tmpalpha, front)
            back= self.frame.astype(float)
            back = cv2.multiply(1.0-tmpalpha, back)
            outimage = cv2.add(front, back)
            self.frame = np.uint8(outimage)
        self.count= (self.count+1)%5

    def update_image(self):
        ret, self.frame = self.cap.read()
        if ret:
            if self.mylist[0] or self.mylist[2] or self.mylist[4]:
                compute = cv2.resize(self.frame, (compute_x,compute_y))
                self.gray = cv2.cvtColor(compute, cv2.COLOR_BGR2GRAY)
                self.apply()
            if self.stickerapply:
                self.label_changed.emit([self.frame, self.sticker_zero])
            else:
                self.label_changed.emit([self.frame, None])

    def stop_thread(self):
        self.stop = True
        self.cap.release()


    def run(self):
        while not self.stop:
            self.update_image()
            time.sleep(1/fps)


class Camera_Form(QtWidgets.QDialog):

    sticker_changed = pyqtSignal(list)

    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.count = 0
        self.ui = uic.loadUi("kiminokaoha.ui", self)
        self.ui.show()
        self.cap = None
        self.mylabel = self.ui.label
        #self.detector = dlib.get_frontal_face_detector()
        self.detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.mythread = None
        self.mylist = [False, None, False, None, False, None]
        self.sticker_zero = None
        self.out_frame = None

    @pyqtSlot()
    def start_capture(self):
        print('signal_Recieved')
        if self.mythread is not None:
            self.mythread.stop_thread()
            self.mythread.quit()
            self.mythread.wait()
            self.mythread = None
        self.mythread = Camera_Thread(self.predictor, self.detector, self.mylist)
        self.mythread.label_changed.connect(self.applyLabel)
        self.sticker_changed.connect(self.mythread.sticker_changed)
        self.mythread.start()

    @pyqtSlot(list)
    def applyLabel(self, array):
        self.out_frame = array[0]
        self.mylabel.setPixmap(myutility.conv2QPixmap(self.out_frame))
        self.sticker_zero = array[1]


    @pyqtSlot()
    def shot(self):
        if self.mythread is not None:
            tmp = confirm.ConfirmForm(self.out_frame, self.sticker_zero, self.predictor, res_x, res_y)
            tmp.exec_()

    @pyqtSlot()
    def stop_capture(self):
        if self.mythread is not None:
            self.mythread.stop_thread()
            self.mythread.quit()
            self.mythread.wait()
            self.mythread = None

    @pyqtSlot(list)
    def listapply(self, mylist):
        self.mylist = mylist
        self.sticker_changed.emit(mylist)

    @pyqtSlot()
    def opensticker(self):
        tmp = sticker_apply.Form(self.mylist)
        tmp.applied.connect(self.listapply)
        tmp.exec_()

    def closeEvent(self, event):
        if self.mythread is not None:
            self.mythread.stop_thread()
            self.mythread.quit()
            self.mythread.wait()
        event.accept()


#for debugging

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w=Camera_Form()
    sys.exit(app.exec_())