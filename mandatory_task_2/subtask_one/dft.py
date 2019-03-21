import numpy as np
from skimage import io, util, color, exposure
import sys
from scipy import fftpack


# Import an image from path
def imprt_img(img_pth):
    return util.img_as_ubyte(color.rgb2gray(io.imread(img_pth)))


# Perform a dft trasnformation on a image
def dft_trnsf(img):
    N = img.shape[0]
    M = img.shape[1]
    print(N)
    dft_img = np.zeros((N, M), dtype=complex)
    print(dft_img)
    for k in range(0, M):
        for l in range(0, N):
            sum = 0
            for i in range(0, M):
                for j in range(0, N):
                    exp_fac = -2j * np.pi
                    exp_frac_fac = ((k*i)/M) + ((l*j)/N)
                    sum = sum + img[i, j] * np.exp(exp_fac * exp_frac_fac)
                dft_img[k, l] = sum
    return dft_img


# Save the image
def save_img(img, fname='my_saved_img.png'):
    io.imsave(fname, np.clip(img, 0, 255))


# Converting from fourier transform to image (Code from lavima Github)
def cnvrt_from_cmplx(img):
    img = np.absolute(img)
    out = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            out[i, j] = np.log(1+img[i, j])
    return out


if len(sys.argv) < 1:
    print('Not enough arguments')
    exit

img = imprt_img(sys.argv[1])
dft_img = dft_trnsf(img)
dft_img = cnvrt_from_cmplx(dft_img)
print(img)
print(dft_img)

# np function for fft
print(img)
fft = fftpack.fft2(img)
fft = cnvrt_from_cmplx(fft)
print(fft)

io.imsave('dft_out.png', exposure.rescale_intensity(dft_img))
