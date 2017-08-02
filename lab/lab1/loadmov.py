import argparse
from cv2.cv import *
import numpy as np
import cv2

 
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
args = parser.parse_args()  

cap = cv2.VideoCapture(args.file)

while(cap.isOpened()):
    ret, frame = cap.read()


    ShowImage('title',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
