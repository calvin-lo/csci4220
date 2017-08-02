# filter.py
import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal

def filter(img):
    # Complete this method according to the tasks listed in the lab handout.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    n = 111
    mean =  np.array([0, 0])
    mean = mean.reshape(2,1)
    cov = np.array([[20,0],[0,20]])
    g2d_kernel, xc, yc = gaussian2_n(mean, cov, 11)
    g2d_kernel_normalized = g2d_kernel / np.sum(g2d_kernel)
    img = signal.convolve2d(img, g2d_kernel_normalized, mode='same', boundary='fill')  
    
    return img

def process_img1(imgfile):
    print 'Opening ', imgfile
    img = cv2.imread(imgfile)

    img = np.uint8(img)
    # You should implement your functionality in filter function
    filtered_img = filter(img)

    cv2.imshow('Input image',img)
    cv2.imshow('Filtered image',filtered_img)

    print 'Press any key to proceed'   
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_img2(imgfile):
    print 'Opening ', imgfile
    img = cv2.imread(imgfile)

    # You should implement your functionality in filter function
    filtered_img = filter(img)

    # You should implement your functionality in filter function

    plt.subplot(121)
    plt.imshow(img)
    plt.title('Input image')
    plt.xticks([]), plt.yticks([])

    plt.subplot(122)
    plt.imshow(filtered_img, cmap = 'gray')
    plt.title('Filtered image')
    plt.xticks([]), plt.yticks([])

    plt.show()

def gaussian2_xy(mean, cov, xy):
    invcov = np.linalg.inv(cov)
    results = np.ones([xy.shape[0], xy.shape[1]])
    for x in range(0, xy.shape[0]):
        for y in range(0, xy.shape[1]):
            v = xy[x,y,:].reshape(2,1) - mean
            results[x,y] = np.dot(np.dot(np.transpose(v), invcov), v)
    results = np.exp( - results / 2 )
    return results 

def gaussian2_n(mean, cov, n):
    s = int(n/2)
    x = np.linspace(-s,s,n)
    y = np.linspace(-s,s,n)
    xc, yc = np.meshgrid(x, y)
    xy = np.zeros([n, n, 2])
    xy[:,:,0] = xc
    xy[:,:,1] = yc

    return gaussian2_xy(mean, cov, xy), xc, yc

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CSCI 4220U Lab 2.')
    parser.add_argument('--use-plotlib', action='store_true', help='If specified uses matplotlib for displaying images.')
    parser.add_argument('--task=1', action='store_true')
    parser.add_argument('--task=2', action='store_true')
    parser.add_argument('--task=3', action='store_true')
    parser.add_argument('--task=4', action='store_true')
    parser.add_argument('--task=5', action='store_true')
    parser.add_argument('imgfile', help='Image file')
    args = parser.parse_args()

    if args.use_plotlib:
        process_img2(args.imgfile)
    else:
        process_img1(args.imgfile) 
