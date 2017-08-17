import cv2
from PyQt5 import QtGui
from PyQt5.QtGui import QImage


def conv2QPixmap(frame):
    height, width, byteValue = frame.shape
    byteValue = byteValue * width
    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
    frame = QImage(frame, width, height, byteValue, QImage.Format_RGB888)
    return QtGui.QPixmap(frame)