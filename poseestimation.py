import cv2
import mediapipe as mp

cap = cv2.VideoCapture("Videos/bicep.mp4")

#initializing the MediaPipe pose estimation model
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

while True:
    success, frame = cap.read()



    if success:
        # mediapipe library takes input as RGB image instead of BGR like open cv
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(frameRGB)
        # print(results.pose_landmarks) pose landmarks are those points which actually points the real body (x, y, z)

        lmList = []
        if results.pose_landmarks:
            mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

            for id, lm in enumerate(results.pose_landmarks.landmark):

                h,w,c = frame.shape
                # print(id, lm)         prints the id of the point of the body like for eyes its 4,5,6 etc out of 33 points
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])

                #drawing circle to the point
                # cv2.circle(frame, (cx, cy), 5, (255,55,0), cv2.FILLED)

            #14 is pointer to left elbow thus we can see
            cv2.circle(frame, (lmList[14][1], lmList[14][2]), 5, (0,225,55), cv2.FILLED)
        #show the videos
        cv2.imshow("out", frame)

        if cv2.waitKey(25) & 0xFF == ord("1"):
            break

    else:
        break

cv2.destroyAllWindows()