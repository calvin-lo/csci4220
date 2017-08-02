import numpy as np
import scipy as sp
from scipy import signal
import cv2
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='CSCI 4220U Assignment 1 part 2.')
parser.add_argument('alpha', help='alpha', type=float)
parser.add_argument('imgfile1', help='Image file 1')
parser.add_argument('imgfile2', help='Image file 2')

args = parser.parse_args()

img1 = cv2.imread(args.imgfile1, 0)
img2 = cv2.imread(args.imgfile2, 0)

# Same shape
if (img1.shape == img2.shape):
    I = img2
# img2 bigger than img1
elif (img2.shape[0] > img1.shape[0] and img2.shape[1] > img1.shape[1]):
    I = img2[:img1.shape[0], :img1.shape[1]]
# img2 smaller than img1
elif (img2.shape[0] < img1.shape[0] and img2.shape[1] < img1.shape[1]):
    I = np.zeros(img1.shape)
    I[:img2.shape[0], :img2.shape[1]] = img2
# img2 row bigger than img1, column smaller than img1
elif (img2.shape[0] >= img1.shape[0] and img2.shape[1] < img1.shape[1]):
    I = np.zeros(img1.shape)
    I[:img1.shape[0], :img2.shape[1]] = img2[:img1.shape[0], :img2.shape[1]]
    img2 = I
# img2 row smaller than img1, column bigger than img1
elif (img2.shape[0] < img1.shape[0] and img2.shape[1] >= img1.shape[1]):
    I = np.zeros(img1.shape)
    I[:img2.shape[0], :img1.shape[1]] = img2[:img2.shape[0], :img1.shape[1]]
    img2 = I
    
I = np.multiply(img1, args.alpha) + np.multiply(I,(1 - args.alpha))
plt.imshow(I, 'gray')
plt.show()
