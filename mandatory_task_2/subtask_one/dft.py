import numpy as np
from skimage import io, util, color
import sys


# Import an image from path
def imprt_img(img_pth):
    return util.img_as_ubyte(color.rgb2gray(io.imread(img_pth)))


# Perform a dft trasnformation on a image
def dft_trnsf(img):
    N = img.shape[0]
    dft_img = np.zeros((50, 50), dtype=int)
    for k in range(0, N):
        for l in range(0, N):
            sum = 0
            for i in range(0, N):
                for j in range(0, N):
                    exp_fac = -i * 2 * np.pi
                    exp_frac_fac = ((k*i)/N) * ((l*j)/N)
                    sum = sum + img[i, j] * np.exp(exp_fac * exp_frac_fac)
            sum = sum / N
            dft_img[k, l] = sum
            print(sum)
    return dft_img


# Save the image
def save_img(img, fname='my_saved_img.png'):
    io.imsave(fname, np.clip(img, 0, 255))


if len(sys.argv) < 1:
    print('Not enough arguments')
    exit
    
#img = np.asmatrix([[255, 255, 0, 255, 255], [255, 255, 0, 255, 255],
#                  [255, 255, 0, 255, 255], [255, 255, 0, 255, 255]])
img = imprt_img(sys.argv[1])
dft_img = dft_trnsf(img)
save_img(dft_img, 'dft_transform.png')
dft_img = np.clip(dft_img, 0, 255)
