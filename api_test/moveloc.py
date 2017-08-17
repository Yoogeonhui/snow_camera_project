import cv2
import numpy as np

lands = []
with open('landmarks.txt') as f:
    for line in f:
        a,b = line.split()
        lands.append((int(a),int(b)))

(x,y,w,h) = cv2.boundingRect(np.float32(lands))

for a in range(len(lands)):
    (curx,cury)= lands[a]
    lands[a] = (curx-x+10, cury-y+10)

with open('landmark_checked.txt','w') as f:
    for line in lands:
        f.write(str(line[0])+' '+str(line[1])+'\n')

newimage = np.zeros((w+20,h+20,3), dtype=np.uint8)

for a in lands:
    cv2.circle(newimage, (a[0],a[1] ), 1, (11, 53, 64), -1)

#cv2.imwrite('landmark_checked.png', newimage)