from skimage import io, util, color, feature
import sys
from scipy import ndimage as nd
import numpy as np

img = util.img_as_float(color.rgb2gray(io.imread(sys.argv[1])))

# Canny edge detecor
gaussian_img = nd.gaussian_filter(img, int(sys.argv[2]))
canny = feature.canny(gaussian_img)
# io.imsave(sys.argv[3], util.img_as_uint(canny))



# Prewitt operators
prk_x = np.asarray([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
prk_y = np.asarray([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])

"""
# Sobel
prk_x = np.asarray([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
prk_y = np.asarray([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
"""

grad_x = nd.convolve(gaussian_img, prk_x, mode='nearest')
grad_y = nd.convolve(gaussian_img, prk_y, mode='nearest')

grad_x_y = np.sqrt(grad_x**2 + grad_y**2)

io.imsave('prewitt.png', util.img_as_uint(grad_x_y))
