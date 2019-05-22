from skimage import util, io, color
import sys
import numpy as np
from scipy import ndimage as nd


def distance(i, j):
    cent = np.floor(flt_size / 2)
    return [i - cent, j - cent]


def gaussian(img):
    flt = np.ndarray((flt_size, flt_size))
    for i in range(flt_size):
        for j in range(0, flt_size):
            arr = distance(i, j)
            flt[i, j] = (1 / (2 * np.pi * sd**2)) * np.exp(-(arr[0]**2 + arr[1]**2) / (2 * sd**2))
    return nd.convolve(img, flt, mode='nearest')


img = util.img_as_float(color.rgb2gray(io.imread(sys.argv[1])))
sd = float(sys.argv[2])
flt_size = int(6 * sd) - 1
io.imsave('gaussian_blurred.png', util.img_as_float(np.clip(gaussian(img), -1, 1)))
