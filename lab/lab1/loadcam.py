from cv2.cv import *

capture = CaptureFromCAM(0)

frame = QueryFrame(capture)
ShowImage("loadcam", frame)

WaitKey(0)
