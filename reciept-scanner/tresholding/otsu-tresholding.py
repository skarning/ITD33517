import numpy as np
from skimage import io, util, color
from scipy import ndimage as nd
import sys

img = util.img_as_ubyte(color.rgb2gray(io.imread(sys.argv[1])))

N = img.shape[0]
M = img.shape[1]

norm_hist = np.zeros(256)

for i in range(0, N):
    for j in range(0, M):
        norm_hist[img[i, j]] += 1

for i in range(0, len(norm_hist)):
    norm_hist[i] = norm_hist[i] / (M*N)

global_mean = 0
for i in range(0, len(norm_hist)):
    global_mean += i * norm_hist[i]

variance_buff = 0
k_buff = 0
# Computes a treshold
for k in range(0, len(norm_hist)):
    cumul_sum = 0
    cumul_mean = 0
    for i in range(0, k):
        cumul_sum += norm_hist[i]
        cumul_mean += i * norm_hist[i]

    # Computing between-class variance
    in_class_variance = ((global_mean * cumul_sum - cumul_mean)**2) / (cumul_sum * (1 - cumul_sum))
    if in_class_variance > variance_buff:
        k_buff = k
        variance_buff = in_class_variance

print('K^*: {}'.format(k_buff))

# Compute global_variance
global_variance = 0
for i in range(0, len(norm_hist)):
    global_variance += ((i - global_mean)**2) * norm_hist[i]

n_k = variance_buff / global_variance

print('Seperability measure: {}'.format(n_k))

for i in range(0, N):
    for j in range(0, M):
        if img[i, j] < k_buff:
            img[i, j] = 255
        else:
            img[i, j] = 0

io.imsave('otsu-treshold-flag.png', img)
    
