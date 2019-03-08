import scipy
import numpy as np
import sys
import skimage
from skimage import io, util, color
from scipy import ndimage


# Reads file and returns histogram
def get_hstg_from_file(fl_path):
    fl = open(fl_path, 'r')
    array = []
    for x in fl:
        array.append(int(x))
    return array


# Converts every value in array to probability
def cnv_to_prob(array, sum):
    array = array.astype(float)
    for i in range(len(array)):
        array[i] = array[i]/sum
    return array


# Reads image and returns array of intensity
def get_hstg_from_img(img):
    hstg = np.zeros(256)
    hstg = hstg.astype(int)
    for i in range(0, img.shape[0]-1):
        for j in range(0, img.shape[1]-1):
            hstg[img[i, j]] += 1
    return hstg


# Testing hstg func
img = util.img_as_ubyte(color.rgb2gray(io.imread('barbara.png')))
nmb_of_pxls = img.shape[0]*img.shape[1]
img_hstg = get_hstg_from_img(img)
img_hstg_prob = cnv_to_prob(img_hstg, nmb_of_pxls)
