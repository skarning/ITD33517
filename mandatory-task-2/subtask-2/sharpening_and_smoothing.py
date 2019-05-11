import numpy as np
import sys
from skimage import util, io, color, exposure
from scipy import fftpack

img = util.img_as_float(color.rgb2gray(io.imread(sys.argv[2])))
M, N = (img.shape)
P = 2*M
Q = 2*N


def dist(u, v):
    u_point = (u - (P/2))**2
    v_point = (v - (Q/2))**2
    return np.sqrt(u_point + v_point)


def ideal_lowpass():
    flt = np.zeros((P, Q))
    for u in range(0, P):
        for v in range(0, Q):
            if dist(u, v) <= 90:
                flt[u, v] = 0.0
            else:
                flt[u, v] = 1.0
    return flt


""" Following step to center align image is taken from https://github.com/lavima/itd33517_examples/blob/master/lecture09_fourier_filtering.py"""
padded_img = np.zeros((P, Q))
padded_img[0:M, 0:N] = img
translated = np.zeros(padded_img.shape)
for i in range(P):
  for j in range(Q):
      translated[i,j] = padded_img[i,j]*((-1)**(i+j))


# FFT transform image
fft_img = fftpack.fft2(translated)
ideal_lowpass_img = fft_img * ideal_lowpass()
ifft_img = fftpack.ifft2(ideal_lowpass_img)


""" Following step to center align image is taken from https://github.com/lavima/itd33517_examples/blob/master/lecture09_fourier_filtering.py"""
re_translated = np.zeros(padded_img.shape)
for i in range(P):
  for j in range(Q):
    re_translated[i,j] = ifft_img[i,j]*((-1)**(i+j))

out = re_translated[0:img.shape[1], 0:img.shape[0]]
    
io.imsave(sys.argv[1], out)
