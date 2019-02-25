import scipy
import numpy as np
import sys
import skimage
from skimage import io, util, color
from scipy import ndimage


"""
Some code in these functions is taken
from  itd33517_examples/lecture04_gaussian_alt.py
lavima on github
"""


# A function for converting top-left aligned coordinates to center aligned
def dist(i, j, flt_size):
    center = flt_size//2
    return (i-center, j-center)


# Applies gaussian_blure to image
def gaussian_blure():
    sigma = float(input('Sigma: '))
    flt_size = int(6*sigma)-1
    flt = np.ndarray((flt_size, flt_size), dtype=np.float)
    cnst = 1/(2*np.pi*sigma**2)
    # Loop through all the pixels of the mask
    for i in range(0, flt_size):
        for j in range(0, flt_size):
            # Find the center-aligned coordinates for the current pixel
            x, y = dist(i, j, flt_size)
            # Calculate the pixel value
            flt[i, j] = cnst * np.exp(-(x**2 + y**2)/(2*sigma**2))
    return flt


# Applies median_smoothing to image
def median_blure():
    print('Median')


def smth_opt(opt):
    return{
        1: gaussian_blure,
        2: median_blure
    }.get(opt, gaussian_blure)


# Script start here
if len(sys.argv) < 3:
    print('No enough arguments')
    sys.exit()

opt = int(input('1.Gaussian\n2.Median\n:'))
smth_func = smth_opt(opt)
img = util.img_as_float(color.rgb2gray(io.imread(sys.argv[1])))
flt = smth_func()

img = ndimage.convolve(img, flt, mode='nearest')
io.imsave(sys.argv[2], img)


"""
By Sivet M. Skarning
"""
