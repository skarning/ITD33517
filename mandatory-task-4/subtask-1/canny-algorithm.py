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
"""
prk_x = np.asarray([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
prk_y = np.asarray([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
"""
# Sobel
prk_x = np.asarray([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
prk_y = np.asarray([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

grad_x = nd.convolve(gaussian_image, prk_x, mode='nearest')
grad_y = nd.convolve(gaussian_image, prk_y, mode='nearest')

grad_x_y = np.sqrt(grad_x**2 + grad_y**2)

io.imsave('grad_x_y.png', util.img_as_uint(grad_x_y))

# Non max supression
n_m_sup = np.zeros(img.shape)
grad_x_y = np.pad(grad_x_y, 0, mode='constant')
N, M = grad_x_y.shape


"""The basic structure of the non_max_supression is taken from:
https://towardsdatascience.com/canny-edge-detection-step-by-step-in-python-computer-vision-b49c3a2d8123
"""
for i in range(1, M-1):
    for j in range(1, N-1):
        d_k = np.rad2deg(np.arctan(grad_y[i, j] / grad_x[i, j]))
        if d_k < 0:
            d_k += 360

        if((0 <= d_k < 22.5) or (157.5 <= d_k <= 180)):
            nx2_1 = grad_x_y[i, j+1]
            nx2_2 = grad_x_y[i, j-1]

        elif(22.5 <= d_k < 67.5):
            nx2_1 = grad_x_y[i+1, j-1]
            nx2_2 = grad_x_y[i-1, j+1]

        elif(67.5 <= d_k < 112.5):
            nx2_1 = grad_x_y[i+1, j]
            nx2_2 = grad_x_y[i-1, j]

        elif(112.5 <= d_k < 157.5):
            nx2_1 = grad_x_y[i-1, j-1]
            nx2_2 = grad_x_y[i+1, j+1]

        if(grad_x_y[i, j] >= nx2_1 and grad_x_y[i, j] >= nx2_2):
            n_m_sup[i, j] = grad_x_y[i, j]
        else:
            n_m_sup[i, j] = 0

io.imsave("non_max_supression.png", util.img_as_uint(n_m_sup))
