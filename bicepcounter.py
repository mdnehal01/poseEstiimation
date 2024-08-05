import cv2
import poseestimationmodule as pm
import numpy as np
import time

cap = cv2.VideoCapture(0)
dir=0
detector = pm.PoseDetector()
count = 0
while True:
    ret, frame = cap.read()

    if ret:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (1200, 900))
        frame = detector.findPose(frame)
        lmList = detector.findPosition(frame)
        print(lmList)
        angle = detector.findAngle(frame, 16,14,12)
        print(angle)

        per = np.interp(angle, (155, 30), (0,100))
        bar = np.interp(angle, (110, 160), (650,100))
        color=(255,100,100)
        if per==0 and dir==0:
            if dir==0:
                count += 0.5
                dir=1
                color=(100, 255, 100)

        if per==100 and dir==1:
            if dir==1:
                count += 0.5
                dir=0
                color=(100,100,255)

        pos = [30, 450]
        ox, oy = pos[0], pos[1]
        offset = 10
        text = str(int(count))

        (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 3, 3)
        x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 244), cv2.FILLED)
        cv2.putText(frame, text, (ox, oy), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        #display bar count
        cv2.rectangle(frame, (1100, 100), (1175, 650), color, 2)
        # cv2.rectangle(frame, (1100, int(bar)), (1175, 650), color, cv2.FILLED)


        cv2.imshow("Bicep Counter", frame)

        if cv2.waitKey(10) & 0xFF==ord("1"):
            break

    else:
        break

cv2.destroyAllWindows()