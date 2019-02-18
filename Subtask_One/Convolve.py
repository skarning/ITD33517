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
    #Saving image to test zero_padding function
    io.imsave('lena_out.png',padded_img)

def rflct_pad(img,flt,pdng_rws,pdng_clms):
    pass

def convolve(img, flt, pdng_func):
    pass

img = util.img_as_float64(color.rgb2gray(io.imread(sys.argv[1])))
rws = int(input('Number of rows in filter:'))
clms = int(input('Number of clms in filter'))
flt = np.zeros((rws,clms))

for i in range(0,rws):
    for j in range(0,clms):
        flt[i,j] = int(input('Type(Row:{}, column:{}) value: '.format(i,j)))

pdng_rws = (rws-1)/2
pdng_clms = (clms-1)/2
       
while(True):
    pdng_optn = int(input('1.Zero-padding\n2.Reflecting-padding'))
    
    if(pdng_optn == 1):
        pdng_func = zero_pad(img,flt,pdng_rws,pdng_clms)
        end
    elif(pdng_optn == 2):
        pdng_func = rflct_pad(img,flt,pdng_rws,pdng_clms)
        end
    else:
        print('{} not an option..'.format(pdng_optn))
