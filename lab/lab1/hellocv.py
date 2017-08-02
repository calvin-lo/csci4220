from cv2.cv import *

img = LoadImage("test.jpg")
NamedWindow("opencv")
ShowImage("opencv",img)
WaitKey(0)