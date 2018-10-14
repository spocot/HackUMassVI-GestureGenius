import numpy as np
import cv2
import math
from win32com.client import Dispatch

capture = cv2.VideoCapture(0)


lower_skin = np.array([10,0.28 * 255,0])
upper_skin = np.array([25,0.68 * 255,255])

curr_progression = 0
curr_gesture = None
gesture_progression = [2, 1, 0]
accuracy = 0
needed_accuracy = 8
speak = Dispatch('SAPI.SpVoice')



while capture.isOpened():

    # Capture frames from the camera
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    # Change color-space from BGR -> HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask1 = cv2.inRange(hsv, np.array([2, 0, 0]), np.array([20, 255, 255]))
    mask2 = cv2.inRange(hsv, lower_skin, upper_skin)
    mask = cv2.bitwise_or(mask1, mask2)

    # Kernel for morphological transformation
    kernel = np.ones((3, 3))

    # Apply Gaussian Blur and Threshold
    first_filter = cv2.medianBlur(mask, 5)
    filtered = cv2.GaussianBlur(first_filter, (7,7), 0)

    # Apply morphological transformations to filter out the background noise
    dilation = cv2.dilate(filtered, kernel, iterations=2)
    erosion = cv2.erode(dilation, kernel, iterations=2)
    cv2.imshow('erosion', erosion)
    extracted = cv2.bitwise_and(frame, frame, mask=erosion)
    cv2.imshow('extracted', extracted)
    bw = cv2.cvtColor(extracted, cv2.COLOR_BGR2GRAY)


    new_filt = cv2.dilate(bw, np.ones((2,1)), iterations=21)

    ret, thresh = cv2.threshold(new_filt, 30, 255, 0)

    # Find contours
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    try:
        bigboi = max(contours, key=cv2.contourArea)
        cv2.drawContours(frame, [bigboi], -1, (0, 255, 0), 3)
        hull = cv2.convexHull(bigboi)
        cv2.drawContours(frame, [hull], -1, (255, 0, 255), 3)

        # print(hull)
        # for h in hull:
        #     try:
        #         x = h[0][0]
        #         y = h[0][1]
        #         print("x: ", x, "y: ", y)
        #         cv2.circle(frame, (x, y), 3, (40, 10, 40), -1)
        #     except:
        #         pass

        defects = cv2.convexityDefects(bigboi, cv2.convexHull(bigboi, returnPoints=False))
        num_defect = 0
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]

            start = tuple(bigboi[s][0])
            end = tuple(bigboi[e][0])
            far = tuple(bigboi[f][0])

            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

            if angle <= 60:
                num_defect += 1
                cv2.circle(frame, far, 3, (0, 0, 255), -1)
                if num_defect > 4:
                    break

            cv2.line(frame, start, end, (0, 255, 0), 1)
        if curr_gesture != num_defect and accuracy < needed_accuracy:
            curr_gesture = num_defect
            accuracy = 0
        if curr_gesture == num_defect and accuracy < needed_accuracy:
            accuracy += 1
        if curr_gesture == num_defect and accuracy >= needed_accuracy:
            if curr_gesture == gesture_progression[curr_progression]:
                curr_progression += 1
                if curr_progression >= len(gesture_progression):
                    curr_progression = 0
                    speak.Speak("Ok Google")
                accuracy = 0
                curr_gesture = None
                print(curr_progression)
            else:
                if curr_progression > 0 and gesture_progression[curr_progression - 1] == curr_gesture:
                    print('Redundant gesture detected, ignoring because Connor hates racing the AI')
                else:
                    print('Not a valid sequence, resetting...')
                    curr_progression = 0
                accuracy = 0
                curr_gesture = None
    except Exception as e:
        pass


    # Show required images
    cv2.imshow("Gesture", frame)
    #all_image = np.hstack((drawing, crop_image))
    #cv2.imshow('Contours', all_image)

    # Close the camera if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()