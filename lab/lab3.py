import numpy as np
import scipy as sp
from scipy import signal
import cv2
import matplotlib.pyplot as plt

sobel_x = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
fft_filter = np.fft.fft2(sobel_x)
fft_shift = np.fft.fftshift(fft_filter)
mag_spectrum = np.log(np.abs(fft_shift)+1)
plt.figure(figsize=(5,5))
plt.imshow(mag_spectrum, 'gray')
plt.show()
