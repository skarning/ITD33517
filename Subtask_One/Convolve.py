import scipy
import sys
import numpy as np
from skimage import io, util, color


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


# User selects what padding method he will use
def opt(pdng_optn):
    return{
        1: zero_pad(img, flt, pdng_rws, pdng_clms),
        2: np.pad(img, (pdng_rws, pdng_clms), 'reflect')
        }.get(pdng_optn, zero_pad(img, flt,
                                  pdng_rws, pdng_clms))


# Convolving through image with provided filter
def convolve(img, flt, pdng_func, pdng_rws, pdng_clms):
    padded_img = pdng_func

    nmb_of_pxl_in_flt = flt.shape[0]*flt.shape[1]
    for i in range(pdng_rws, padded_img.shape[0]-pdng_rws):
        for j in range(pdng_clms, padded_img.shape[1]-pdng_clms):
            flt_i = -1
            flt_j = -1
            pxl_vlu = 0
            for k in range(i-pdng_rws, i-pdng_rws+flt.shape[0]):
                flt_i = flt_i+1
                for l in range(j-pdng_clms, j-pdng_clms+flt.shape[1]):
                    flt_j = flt_j+1
                    pxl_vlu = (flt[flt_i, flt_j] * padded_img[k, l]) + pxl_vlu
                flt_j = -1
            padded_img[i, j] = pxl_vlu/nmb_of_pxl_in_flt
    io.imsave('lena_out.png', padded_img)


# Script starts here
if len(sys.argv) < 2:
    print('No image as argument')
    sys.exit()

img = util.img_as_float(color.rgb2gray(io.imread(sys.argv[1])))
while True:
    rws = int(input('Number of rows in filter:'))
    clms = int(input('Number of clms in filter'))
    if rws % 2 == 0 or clms % 2 == 0:
        print('Filter size have to be odd')
        continue
    break

flt = np.zeros((rws, clms))

# User select filter values
for i in range(0, rws):
    for j in range(0, clms):
        flt[i, j] = float(input('Type(Row:{},'
                                ' column:{}) value: '.format(i, j)))
flt = np.asmatrix(flt)
flt = np.rot90(flt, 2)

# Calculating number of colums and rows to pad
pdng_rws = int((rws-1)/2)
pdng_clms = int((clms-1)/2)

pdng_optn = int(input('1.Zero-padding\n2.Reflecting-padding\n: '))
convolve(img, flt, opt(pdng_optn), pdng_rws, pdng_clms)


"""
By Sivert M. Skarning
"""
