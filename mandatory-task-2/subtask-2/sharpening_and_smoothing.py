import numpy as np
import sys
from skimage import util, io, color, exposure
from scipy import fftpack

"""
Most of this code is taken from lavima on github, ITD53317 examples
"""


# Function for finding the distance to center by lavima
def dist(i, j):
    center_i, center_j = (height*2//2, width*2//2)
    return ((i-center_i)**2 + (j-center_j)**2)**0.5


img = util.img_as_float(color.rgb2gray(io.imread(sys.argv[1])))
height, width = img.shape
padded_img = np.pad(img, (height*2, width*2), 'constant')
img_trans = np.zeros(padded_img.shape)

for i in range(padded_img.shape[0]):
    for j in range(padded_img.shape[1]):
        img_trans[i, j] = padded_img[i, j]*((-1)**(i+j))

fft = fftpack.fft2(img_trans)

flt = np.zeros(img_trans.shape)
for i in range(flt.shape[1]):
    for j in range(flt.shape[0]):
        if(dist(i, j) <= 50):
            flt[i, j] = 0.0
        else:
            flt[i, j] = 1.0

# In the frequency domain multiplication is the same as
# convolution in spatial domain

flt_img = flt * fft
flt_img = fftpack.ifft2(flt_img)

flt_img_translated = np.zeros(padded_img.shape)

for i in range(2*height):
    for j in range(2*width):
        flt_img_translated[i, j] = flt_img[i, j]*((-1)**(i+j))

depadded_filtered_img = flt_img_translated[0:height, 0:width]
io.imsave('out.png', np.clip(flt_img_translated, 0, 1))
