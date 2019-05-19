import numpy as np
from skimage import io, util, color
from scipy import ndimage as nd
import sys
from skimage.transform import (hough_line, hough_line_peaks)
from collections import Counter
from skimage.transform import rotate

img = util.img_as_float(color.rgb2gray(io.imread(sys.argv[1])))

n = img.shape[0]
m = img.shape[1]

for i in range(0, n):
    for j in range(0, m):
        if(img[i, j] > 0.75):
            img[i, j] = 0.0
        else:
            img[i, j] = 1.0

io.imsave('treshold.png', util.img_as_uint(img))

sobel_x = np.asarray([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
sobel_y = np.asarray([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

grad_x = nd.convolve(img, sobel_x, mode='nearest')
grad_y = nd.convolve(img, sobel_y, mode='nearest')

io.imsave('grad_x.png', util.img_as_uint(np.clip(grad_x, -1, 1)))
io.imsave('grad_y.png', util.img_as_uint(np.clip(grad_y, -1, 1)))

grad_x_y = np.zeros((n, m), dtype=float)
for i in range(0, n):
    for j in range(0, m):
        grad_x_y[i, j] = np.sqrt(np.arctan(grad_x[i, j]**2 + grad_y[i, j]**2))

io.imsave('grad_x_y.png', util.img_as_uint(np.clip(grad_x_y, -1, 1)))

h, theta, d = hough_line(grad_x_y)

for i in range(0, len(theta) - 1):
        if(theta[i]) != 0:
            print(theta[i])

h_p, theta_p, d_p = hough_line_peaks(h, theta, d)


print('--------------------------------')


for i in range(0, len(theta_p) - 1):
    print(theta_p[i])

for i in range(0, len(theta_p) - 1):
    theta_p[i] = np.round(theta_p[i], 2)

occ = Counter(theta_p)

print(occ)

angle = float(max(occ, key=occ.get))

rotated_img = rotate(grad_x_y, float((angle *  180) / np.pi ))

print('Angle: {}'.format(float((angle *  180) / np.pi )))
print(angle)

io.imsave('rotated_2.png', util.img_as_uint(np.clip(rotated_img, -1, 1)))
