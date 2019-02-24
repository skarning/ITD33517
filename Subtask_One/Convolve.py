import scipy
import sys
import numpy as np
from skimage import io, util, color
from fractions import Fraction


# Pads image with zero padding
def zero_pad(img, flt, pdng_rws, pdng_clms):
    height = img.shape[0]
    width = img.shape[1]
    rws = height+(2*pdng_clms)
    clms = width+(2*pdng_rws)
    padded_img = np.zeros((rws, clms))

    # Takes a padded_img and fills it with the image
    for i in range(pdng_clms, pdng_clms+width):
        for j in range(pdng_rws, pdng_rws+height):
            padded_img[i, j] = img[i-pdng_clms, j-pdng_rws]
    return padded_img


# Pads img with reflection padding
def rflct_pad(img, flt, pdng_rws, pdng_clms):
    pass


# Convolving through image with provided filter
def convolve(img, flt, pdng_func, pdng_rws, pdng_clms):
    padded_img = pdng_func

    nmb_of_pxl_in_flt = flt.shape[0]*flt.shape[1]
    for i in range(pdng_rws, padded_img.shape[0]-pdng_rws):
        for j in range(pdng_clms, padded_img.shape[1]-pdng_clms):
            flt_i = 0
            flt_j = 0
            pxl_vlu = 0
            for k in range(i, flt.shape[0]):
                flt_i = flt_i+1
                for l in range(j-pdng_clms, flt.shape[1]):
                    flt_j = flt_j+1
                    pxl_vlu = flt[flt_i, flt_j] * padded_img[k, l] + pxl_vlu
            padded_img[i, j] = pxl_vlu/nmb_of_pxl_in_flt
    io.imsave('lena_out.png', padded_img)


# Script starts here
if len(sys.argv) < 2:
    print('No image as argument')
    sys.exit()

img = util.img_as_float64(color.rgb2gray(io.imread(sys.argv[1])))
rws = int(input('Number of rows in filter:'))
clms = int(input('Number of clms in filter'))
flt = np.zeros((rws, clms))

# User select filter values
for i in range(0, rws):
    for j in range(0, clms):
        flt[i, j] = float(input('Type(Row:{},'
                                ' column:{}) value: '.format(i, j)))
matx_scl = float(Fraction(input('Select a scalar to multiple filter'
                                'with for example(1/9) for Gaussian Blur: ')))
flt = np.asmatrix(flt)*matx_scl

# Calculating number of colums and rows to pad
pdng_rws = int((rws-1)/2)
pdng_clms = int((clms-1)/2)

# User selects what padding method he will use
while(True):
    pdng_optn = int(input('1.Zero-padding\n2.Reflecting-padding\n: '))
    if pdng_optn == 1:
        pdng_func = zero_pad(img, flt, pdng_rws, pdng_clms)
        break
    elif pdng_optn == 2:
        pdng_func = rflct_pad(img, flt, pdng_rws, pdng_clms)
        break
    else:
        print('{} not an option..'.format(pdng_optn))

convolve(img, flt, pdng_func, pdng_rws, pdng_clms)

"""
By Sivert M. Skarning
"""
