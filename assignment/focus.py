import numpy as np
import scipy as sp
from scipy import signal
import cv2
import matplotlib.pyplot as plt
import argparse
import time

# calculate the average frequency of a block
# higher frequency = sharper
# lower frequency = blurrier 
def calcSharpness(I):
    size = I.shape[0] * I.shape[1]
    blur_fft = np.abs(np.fft.fft2(I))
    blur_f = np.abs(blur_fft)
    sharpness = 0;
    for i in range(1, blur_f.shape[0]):
        for j in range(1, blur_f.shape[1]):
            sharpness = sharpness + blur_f[i][j]
    return sharpness/size
  
# divide image into blocks and find the average sharpness
# return list of tuples blocks (sharpness and position)
def divide_into_blocks(img, block_x, block_y):
    blocks = []
    
    for i in range(0, img.shape[0]-block_x, block_x):
        for j in range(0, img.shape[1]-block_y,block_y):
            T = np.zeros((block_x,block_y))
            T[:block_x,:block_y] = img[i:i+block_x, j:j+block_y]
            sharpness = calcSharpness(T)
            blocks.append((sharpness, (i, j)))
    return blocks

# Process the image
def process_img(imgfile):
    img = cv2.imread(imgfile, 0)
    
    # Laplacian (get the blurriness)
    laplacian = np.array([[0,1,0],[1,-4,1],[0,1,0]], dtype = 'float32')
    img = signal.convolve2d(img, laplacian, mode='same')

    # calculate the size of the block
    block_x = img.shape[0]/10
    block_y = img.shape[1]/10
    
    # divide image into blocks
    blocks = divide_into_blocks(img, block_x, block_y)

    highF = 0
    # find the highest frequency
    for i in range(0, len(blocks)):
        if blocks[i][0] > highF:
            highF = blocks[i][0]
    
    # calculate the threshold
    threshold = highF * 0.5

    # draw the rectangle of blocks have higher than frequency than threshold
    img = cv2.imread(imgfile, 0)
    for i in range(0, len(blocks)):
        if blocks[i][0] > threshold:
            v1 = blocks[i][1]
            v2 = (blocks[i][1][0] + block_x, blocks[i][1][1] + block_y)
            cv2.rectangle(img, v1, v2,(255,0,),2)
    return img
  
parser = argparse.ArgumentParser(description='CSCI 4220U Assignment 1 part 1.')
parser.add_argument('imgfile', help='Image file')
args = parser.parse_args()

start_time = time.time()
img = process_img(args.imgfile)
process_time = (time.time() - start_time) * 1000
print("Focus analysis took %s ms." % process_time)

plt.imshow(img, 'gray')
plt.show()
