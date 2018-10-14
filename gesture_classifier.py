import cv2
import numpy as np
import math

gaussian_k = 11
box_count = 9
cap_x = 500
cap_y = 150
cap_size = 20

cap = cv2.VideoCapture(0)

def generate_histogram(f, box_x, box_y):
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    region = np.zeros([cap_size * box_count, cap_size, 3], dtype=hsv.dtype)
    for i in range(box_count):
        region[i*cap_size:i*cap_size+cap_size,0:cap_size] = hsv[box_y[i]:box_y[i]+cap_size,box_x[i]+cap_size]

    histo = cv2.calcHist([region],[0,1], None, [180,256], [0,180,0,256])
    cv2.normalize(histo, histo, 0, 255, cv2.NORM_MINMAX)
    return histo

def threshold(f, hand_hist):
    f = cv2.medianBlur(f, 3)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    hsv[0:int(cap_x_end * hsv.shape[0]),0:int(cap_x)]

while(1):
    _, frame = cap.read();

    frame = cv2.flip(frame, 1)

    cv2.imshow('Main', frame)

    v = cv2.waitKey(5) & 0xFF;
    if v == ord('q'):
        break
    elif v == ord('b'):
        break
    elif v == ord('c'):
        break

cap.release()
cv2.destroyAllWindows()