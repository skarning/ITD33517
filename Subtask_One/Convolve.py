import scipy
import sys
import numpy as np
from skimage import io,util,color

def zero_pad(img,flt,pdng_rws,pdng_clms):
    height = img.shape[0]
    width = img.shape[1]
    rws = height+(2*pdng_clms)
    clms = width+(2*pdng_rws)
    padded_img = np.zeros((rws,clms))

    for i in range(pdng_clms,pdng_clms+width):
        for j in range(pdng_rws,pdng_rws+height):
            padded_img[i,j] = img[i-pdng_clms,j-pdng_rws]
    return padded_img

def rflct_pad(img,flt,pdng_rws,pdng_clms):
    pass

def convolve(img, flt, pdng_func,pdng_rws,pdng_clms):
    padded_img = pdng_func

    for i in range(pdng_rws,padded_img.shape[0]-pdng_rws):
        for j in range(pdng_clms,padded_img.shape[1]-pdng_clms):
            padded_img[j,i] = 0.9
    io.imsave('lena_out.png',padded_img)

#Script starts here
if len(sys.argv)<2:
    print('No image as argument')
    sys.exit()
    
img = util.img_as_float64(color.rgb2gray(io.imread(sys.argv[1])))
rws = int(input('Number of rows in filter:'))
clms = int(input('Number of clms in filter'))
flt = np.zeros((rws,clms))

"""
for i in range(0,rws):
    for j in range(0,clms):
        flt[i,j] = int(input('Type(Row:{}, column:{}) value: '.format(i,j)))
"""
pdng_rws = int((rws-1)/2)
pdng_clms = int((clms-1)/2)
       
while(True):
    pdng_optn = int(input('1.Zero-padding\n2.Reflecting-padding\n: '))
    
    if pdng_optn == 1:
        pdng_func = zero_pad(img,flt,pdng_rws,pdng_clms)
        break
    elif pdng_optn == 2:
        pdng_func = rflct_pad(img,flt,pdng_rws,pdng_clms)
        break
    else:
        print('{} not an option..'.format(pdng_optn))

convolve(img,flt,pdng_func,pdng_rws,pdng_clms)
