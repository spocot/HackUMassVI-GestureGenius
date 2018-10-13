import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorKNN()

skin_detection = [np.array([0, 0.28 * 255, 0]), np.array([25, 0.68 * 255, 255])]

while(1):
    # Read next frame from cam and create copies for drawing different types of contours
    _, frame = cap.read()
    skin_frame = frame.copy()
    combined_frame = frame.copy()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    skin_mask = cv2.inRange(hsv, skin_detection[0], skin_detection[1])

    # Blur the skin mask
    skin_mask = cv2.blur(skin_mask, (10, 10))

    # Apply background subtraction filter
    fgmask = fgbg.apply(frame)

    # Blur to reduce noise
    fgmask= cv2.blur(fgmask, (8,8))

    # Combine the masks and find contours using the new mask
    combined_mask = cv2.bitwise_or(fgmask, skin_mask)
    _, thresh = cv2.threshold(combined_mask, 200, 255, cv2.THRESH_BINARY)
    _, combined_contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bigboi = sorted(combined_contours, key=cv2.contourArea)[-1]
    cv2.drawContours(combined_frame, [bigboi], -1, (0, 255, 0), 3)


    # Find contours from both masks
    _, contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0,255,0), 3)

    _, skin_contours, _ = cv2.findContours(skin_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bigskinboi = sorted(skin_contours, key=cv2.contourArea)[-1]
    cv2.drawContours(skin_frame, [bigskinboi], -1, (0,255,0), 3)


    # Show
    cv2.imshow('background-contours', frame)
    cv2.imshow('skin-contours', skin_frame)
    cv2.imshow('combined-contours', combined_frame)
    k =  cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()