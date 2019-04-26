import numpy as np
from skimage import io, util, color
from scipy import ndimage as nd
import sys

img = util.img_as_float(color.rgb2gray(io.imread(sys.argv[1])))
sd = float(sys.argv[2])
"""
4 is multiplum of 2, when subtracting 1
filtersize will always be odd
"""
flt_size = int(4*sd)-1


""" Function dist, gaussian_smooth from https://github.com/lavima/
itd33517_examples/
blob/master/lecture13_edge_detection.py
"""


def dist(i, j):
    center = flt_size//2
    return (i-center, j-center)


def gaussian_smooth():
    flt = np.ndarray((flt_size, flt_size), dtype=np.float)
    const = 1/(2*np.pi*sd**2)
    for i in range(0, flt_size):
        for j in range(0, flt_size):
            x, y = dist(i, j)
            flt[i, j] = const * np.exp(-(x**2 + y**2) / (2*sd**2))
    return flt


flt = gaussian_smooth()
gaussian_image = nd.convolve(img, flt, mode="nearest")
io.imsave("lena_gaussian.png", util.img_as_uint(gaussian_image))

# Prewitt operators
prk_x = np.asarray([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
prk_y = np.asarray([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])

grad_x = nd.convolve(gaussian_image, prk_x, mode='nearest')
grad_y = nd.convolve(gaussian_image, prk_y, mode='nearest')

io.imsave("grad_x.png", util.img_as_uint(grad_x))
io.imsave("grad_y.png", util.img_as_uint(grad_y))
