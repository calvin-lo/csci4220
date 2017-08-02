 
import argparse
from cv2.cv import *
 
parser = argparse.ArgumentParser()
parser.add_argument('file', type=str)
args = parser.parse_args()  
 
img = LoadImage(args.file)
NamedWindow("opencv")
ShowImage("opencv",img)
WaitKey(0)
