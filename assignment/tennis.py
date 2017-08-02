import cv2
import numpy as np

def track(frame):
    blur = cv2.GaussianBlur(frame, (5,5),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower_green = np.array([40,70,70])
    upper_green = np.array([80,200,200])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    moments = cv2.moments(bmask)
    m00 = moments['m00']
    center_x, center_y = None, None
    if m00 != 0:
        center_x = int(moments['m10']/m00)
        center_y = int(moments['m01']/m00)
    center = (-1,-1)

    if center_x != None and center_y != None:
        center = (center_x, center_y)
        cv2.circle(frame, center, 20, (0,0,255))
    cv2.imshow("A3", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        center = None

    return center

if __name__ == '__main__':

    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        if ret:
            if not track(frame):
                break
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
           print('Capture failed')
           break
