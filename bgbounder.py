import numpy as np
import cv2

def normalize_gesture(g):
    print(g)
    normal_g = np.subtract(g, np.median(g, axis=0))
    print(normal_g)

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorKNN()

skin_detection = [np.array([0, 0.28 * 255, 0]), np.array([26, 0.68 * 255, 255])]

while(1):
    # Read next frame from cam and create copies for drawing different types of contours
    _, frame = cap.read()
    bound_frame = frame.copy()

    fgmask = fgbg.apply(frame)
    fgmask = cv2.GaussianBlur(fgmask, (3,3), 0)
    _, fgmask = cv2.threshold(fgmask, 195, 255, cv2.THRESH_BINARY)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    skin_mask = cv2.inRange(hsv, skin_detection[0], skin_detection[1])

    # Blur the skin mask
    skin_mask = cv2.blur(skin_mask, (10, 10))

    cv2.imshow('skin', fgmask)
    try:
        # Combine the masks and find contours using the new mask
        _, fgcontours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        bigboi = max(fgcontours, key=cv2.contourArea)
        cv2.drawContours(frame, [bigboi], -1, (0, 255, 0), 3)
        hull = cv2.convexHull(bigboi)
        cv2.drawContours(frame, [hull], -1, (255,0,0), 3)
        normalize_gesture(hull)
        rec = cv2.boundingRect(hull)
        x,y,w,h = rec
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), thickness=2)
    except:
        print("Error drawing...")

    # Show
    cv2.imshow('background-contours', frame)
    k =  cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
