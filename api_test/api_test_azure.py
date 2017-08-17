# -*- coding: utf-8 -*-

import urllib2
from PyQt5 import QtWidgets
import json
import dlib
import cv2
import numpy as np
from imutils import face_utils


name = r'C:\Users\pc\Pictures\Trump1-1.jpg'
with open(name, 'rb') as f:
    content = f.read()
req = urllib2.Request(
    "https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=false&returnFaceLandmarks=false",
    content, {'Content-Type': 'application/octet-stream'})
req.add_header('Ocp-Apim-Subscription-Key', 'b6b816dda0814cbba32c033f7b30fb83')
try:
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
        faces.append(save)
    print(faces)
    mat = np.fromstring(content, dtype=np.uint8)
    img_np = cv2.imdecode(mat, cv2.CV_LOAD_IMAGE_COLOR)

    #imgnp => 이미지
    for (i, theface) in enumerate(faces):
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
        shape = predictor(gray, dlib.rectangle(f_x, f_y, f_x + f_w, f_y + f_h ))
        shape = face_utils.shape_to_np(shape)
        lands = []
        for (x, y) in shape:
            cv2.circle(img_np, (x, y), 1, (0, 0, 255), -1)
            lands.append((x,y))
        face_landmarks.append(lands)
    print(face_landmarks)


except urllib2.URLError, e:
    print(e.reason)