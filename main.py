import numpy as np
import cv2

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2()

while(1):
   _, frame = cap.read()
   fgmask = fgbg.apply(frame)
   fgmask= cv2.blur(fgmask, (5, 5))
   new = cv2.bitwise_and(frame, frame, mask=fgmask)
   im2, contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   with_contour = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2RGB)
   cv2.drawContours(frame, contours, -1, (0,255,0), 3)
   #cv2.circle(new, (100, 100), 20, (0, 255, 0), thickness=5)
   cv2.imshow('original', frame)
   cv2.imshow('mask', fgmask)
   cv2.imshow('new', new)
   cv2.imshow('with contour', with_contour)
   k =  cv2.waitKey(5) & 0xFF
   if k == 27:
      break

cap.release()
cv2.destroyAllWindows()