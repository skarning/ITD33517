import numpy as np
from skimage import io, util, color
import sys


# Import an image from path
def imprt_img(img_pth):
    return util.img_as_ubyte(color.rgb2gray(io.imread(img_pth)))


# Perform a dft trasnformation on a image
def dft_trnsf(img):
    N1 = img.shape[0]
    N2 = img.shape[1]
    for k in range(0, img.shape[0]):
        for l in range(0, img.shape[1]):
            sum = 0
            for i in range(0, N1):
                for j in range(0, N2):
                    factor =  np.exp(-i*2*np.pi
                                     * (((i**2) / N1) * ((j**2) / N2)))
                    sum = sum + img[i, j]*factor
        img[k, l] = sum
    return img


# Save the image
def save_img(img, fname='my_saved_img.png'):
    io.imsave(fname, np.clip(img, 0, 255))


if len(sys.argv) < 1:
    print('Not enough arguments')
    exit

img = imprt_img(sys.argv[1])
dft_img = dft_trnsf(img)
save_img(dft_img, 'dft_transform.png')
