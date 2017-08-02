import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import scipy as sp

img_file = 'cn-tower-1.jpg'

img = cv2.imread(img_file)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
src = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

sift = cv2.SIFT()

detector = cv2.FeatureDetector_create("SIFT")
descriptor = cv2.DescriptorExtractor_create("SIFT")

src = np.uint8(src)
kp = detector.detect(src, None) 
