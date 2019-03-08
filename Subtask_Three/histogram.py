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
    fl.close
    array = np.asarray(array)
    return array


# Returns number of pixels in histogram file
def get_nmb_of_pxls_in_hstg_file(array):
    sum = 0
    for x in array:
        sum = sum+x
    return sum


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


# Returns array with cumulative probability
def get_cmltv_prob(array):
    buff = 0
    for i in range(0, len(array)):
        array[i] = array[i]+buff
        buff = array[i]
    return array


# Placing a histogram from an image to a file
def wrt_hstg_to_file(file_path, img):
    hstg = get_hstg_from_img(img)
    hstg = np.asarray(hstg)
    fl = open(file_path, 'w')
    for i in range(0, len(hstg)):
        fl.write(str(hstg[i]))
        fl.write('\n')
    fl.close


# Getting Cumulative function for image
img = util.img_as_ubyte(color.rgb2gray(io.imread('barbara.png')))
nmb_of_pxls = img.shape[0]*img.shape[1]
img_hstg = get_hstg_from_img(img)
img_hstg_prob = cnv_to_prob(img_hstg, nmb_of_pxls)
img_hstg_cmlprob = get_cmltv_prob(img_hstg_prob)

# Getting Cumulateive function for histogram file
spc_hstg = get_hstg_from_file('file_histogram.txt')
spc_hstg_prob = cnv_to_prob(spc_hstg, get_nmb_of_pxls_in_hstg_file(spc_hstg))
spc_hstg_cmlprob = get_cmltv_prob(spc_hstg_prob)

print(spc_hstg_cmlprob)
print(img_hstg_cmlprob)
