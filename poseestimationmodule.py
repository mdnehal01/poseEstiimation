import cv2
import mediapipe as mp
import math
class PoseDetector():
    def __init__(self, mode=False, mcomplexity=1, slandmarks=True, esegmentation=False, ssegmentation=True, detconfidence=0.5, trackconfidence=0.5):
        self.mode=mode
        self.mcomplexity=mcomplexity
        self.slandmarks=slandmarks
        self.esegmentation=esegmentation
        self.ssegmentation=ssegmentation
        self.detconfidence=detconfidence
        self.trackconfidence=trackconfidence
        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose(self.mode, self.mcomplexity, self.slandmarks, self.esegmentation, self.ssegmentation, self.detconfidence, self.trackconfidence)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):

                h,w,c = img.shape
                 # print(id, lm)         prints the id of the point of the body like for eyes its 4,5,6 etc out of 33 points
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx,cy), 5, (255,0,100), cv2.FILLED)

        return self.lmList

    def findAngle(self, img, point1, point2, point3, draw=True):
        _, x1, y1 = self.lmList[point1]
        _, x2, y2 = self.lmList[point2]
        _, x3, y3 = self.lmList[point3]

        angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))
        if angle<0:
            angle += 360


        if draw:
            cv2.line(img, (x1,y1), (x2, y2), (255,255,255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10,(0,0,255), 2)
            cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, str(int(angle)),(x2-50, y2-50), cv2.FONT_HERSHEY_PLAIN, 2, (0,200,50), 2)

        return angle
def main():
    cap = cv2.VideoCapture("Videos/bicep.mp4")

    detector = PoseDetector()

    while True:

        ret, frame = cap.read()
        if ret:
            frame=detector.findPose(frame)
            lmlist = detector.findPosition(frame, draw=True)
            print(lmlist)
            cv2.imshow("Output", frame)

            if cv2.waitKey(25) & 0xFF==ord("1"):
                break

        else:
            break


if __name__ == '__main__':
    main()
