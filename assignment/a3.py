import cv2
import numpy as np


def track(frame):

    blur = cv2.GaussianBlur(frame, (5,5),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40,70,70])
    upper_green = np.array([80,200,200])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    # Display full-color image
    cv2.imshow("A3", frame)
    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        center = None
    # Return coordinates of centroid
    return center
# Test with input from camera
if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    while True:
        okay, image = capture.read()
        if okay:
            if not track(image):
                break
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
           print('Capture failed')
           break
