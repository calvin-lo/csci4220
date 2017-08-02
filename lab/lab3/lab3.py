import numpy as np
import scipy as sp
from scipy import signal
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('../messi.jpg', 0) # Load in grayscale
sobel_x = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
img_x = sp.signal.convolve(img, sobel_x, mode='same')
plt.figure(figsize=(5,5))
plt.imshow(img_x,'gray')

from PIL import Image

im = Image.open("../messi.jpg")
matrix = np.array(im.getdata()).reshape(im.size)
print matrix
