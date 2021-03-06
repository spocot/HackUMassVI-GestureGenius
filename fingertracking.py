import numpy as np
import cv2
import math

capture = cv2.VideoCapture(0)

lower_skin = np.array([0,0.28 * 255,0])
upper_skin = np.array([25,0.68 * 255,255])

curr_gesture = None
accuracy = 0
curr_progression = 0
gesture_progression = [4, 3, 2, 1]

while capture.isOpened():

   # Capture frames from the camera
   ret, frame = capture.read()

   # Get hand data from the rectangle sub window
   #cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 0)

   # Apply Gaussian blur
   blur = cv2.GaussianBlur(frame, (3, 3), 0)

   # Change color-space from BGR -> HSV
   hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

   mask1 = cv2.inRange(hsv, np.array([2, 0, 0]), np.array([20, 255, 255]))
   mask2 = cv2.inRange(hsv, lower_skin, upper_skin)
   mask = cv2.bitwise_and(mask1, mask2)

   # Kernel for morphological transformation
   kernel = np.ones((10, 10))

   # Apply morphological transformations to filter out the background noise
   dilation = cv2.dilate(mask, kernel, iterations=1)
   erosion = cv2.erode(dilation, kernel, iterations=1)

   # Apply Gaussian Blur and Threshold
   filtered = cv2.GaussianBlur(erosion, (21, 21), 0)
   ret, thresh = cv2.threshold(filtered, 150, 255, 0)

   # Show threshold image
   cv2.imshow("Thresholded", thresh)

   # Find contours
   image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   try:
       bigboi = max(contours, key=cv2.contourArea)
       cv2.drawContours(frame, [bigboi], -1, (0, 255, 0), 3)
       hull = cv2.convexHull(bigboi)
       cv2.drawContours(frame, [hull], -1, (255, 0, 255), 3)

       # print(hull)
       # for h in hull:S
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

           if angle <= 90:
               num_defect += 1
               cv2.circle(frame, far, 3, (0, 0, 255), -1)

           cv2.line(frame, start, end, (0, 255, 0), 1)
       if curr_gesture != num_defect and accuracy < 30:
           curr_gesture = num_defect
           accuracy = 0
       if curr_gesture == num_defect and accuracy < 30:
           accuracy += 1
       if curr_gesture == num_defect and accuracy >= 30:
           if curr_gesture == gesture_progression[curr_progression]:
               curr_progression += 1
               accuracy = 0
               curr_gesture = None
           else:
               if curr_progression > 0 and gesture_progression[curr_progression-1] == curr_gesture:
                   print('Redundant gesture detected, ignoring because Connor hates racing the AI')
               else:
                   curr_progression = 0
               accuracy = 0
               curr_gesture = None

           print(curr_gesture+1)

       print(num_defect+1)
   except Exception as e:
       print(e)
       pass


   cv2.imshow("Gesture", frame)
   #all_image = np.hstack((drawing, crop_image))
   #cv2.imshow('Contours', all_image)

   # Close the camera if 'q' is pressed
   if cv2.waitKey(1) == ord('q'):
       break

capture.release()
cv2.destroyAllWindows()