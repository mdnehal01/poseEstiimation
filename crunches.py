import cv2
import time
import numpy as np
import poseestimationmodule as pm

cap = cv2.VideoCapture("Videos/crunches.webm")
detector = pm.PoseDetector()
dir = 0
count=0
ptime = 0
while True:
    ret, frame = cap.read()
    if ret:
        frame = detector.findPose(frame)
        lmList = detector.findPosition(frame, draw=False)
        #print(lmList)
        if len(lmList)!=0:
            angle=detector.findAngle(frame, 11, 23, 25, draw=True)
            #print(angle)
            per=np.interp(angle, (110,60), (0,100))
            bar = np.interp(angle, (200, 280), (650, 100))
            color=(255, 100, 100)
            if per == 100:
                color=(100, 255, 100)
                if dir==0:
                    count+=0.5
                    dir=1
            if per == 0:
                color=(100, 100, 255)
                if dir == 1:
                    count+=0.5
                    dir=0

            # Displaying Curl Count
            pos = [30, 450]
            ox, oy = pos[0], pos[1]
            offset = 10
            text = str(int(count))

            (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 11, 11)
            x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, text, (ox, oy), cv2.FONT_HERSHEY_PLAIN, 10, (255, 255, 255), 6)

            #Displating the Bar Count

            cv2.rectangle(frame, (1600, 100), (1675, 650),color, 3)
            cv2.rectangle(frame, (1600, int(bar)), (1675, 650), color, cv2.FILLED)
            cv2.putText(frame, f'{int(per)}%', (1600, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)


            # Displaying the FPS
            ctime = time.time()
            fps = 1/(ctime - ptime)
            ptime = ctime
            pos = [30, 60]
            ox, oy = pos[0], pos[1]
            offset=10
            text = "FPS: " + str(int(fps))

            (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 3,3)
            x1,y1, x2, y2 = ox-offset, oy+offset, ox+w+offset, oy-h-offset
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), cv2.FILLED)
            cv2.putText(frame, text, (ox, oy), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        frame = cv2.resize(frame, (0,0), None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)


        cv2.imshow("Video", frame)
        if cv2.waitKey(5) & 0xFF==ord('1'):
            break
    else:
        break