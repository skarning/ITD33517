import numpy as np
from skimage import io, util, color, exposure
import sys
from scipy import fftpack


# Import an image from path
def imprt_img(img_pth):
    return util.img_as_ubyte(color.rgb2gray(io.imread(img_pth)))


# Perform a dft transformation on a image
def dft_trnsf(img):
    N = img.shape[0]
    dft_img = np.zeros((N, N), dtype=complex)
    for k in range(0, N):
        for l in range(0, N):
            sum = 0
            for i in range(0, N):
                for j in range(0, N):
                    exp_fac = -2j * np.pi
                    exp_frac_fac = ((k*i)/N) + ((l*j)/N)
                    sum = sum + img[i, j] * np.exp(exp_fac * exp_frac_fac)
                dft_img[k, l] = sum
    return dft_img


# Perform an inverse transformation on a image
def idft_trnsf(img):
    N = img.shape[0]
    idft_img = np.zeros((N, N), dtype=complex)
    for a in range(0, N):
        for b in range(0, N):
            sum = 0
            for i in range(0, N):
                for j in range(0, N):
                    exp_frac = 2j * np.pi
                    exp_frac_fac = ((a*i)/N) + ((b*j)/N)
                    sum = sum + img[i, j] * np.exp(exp_frac * exp_frac_fac)
                idft_img[a, b] = (1/N**2) * sum
    return idft_img


# Save the image
def save_img(img, fname='my_saved_img.png'):
    io.imsave(fname, np.clip(img, 0, 255))


# Converting from complex (Code from lavima Github)
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


# img = np.asarray([[0, 255, 0], [0, 255, 0], [0, 255, 0]])

# Dft transform image
dft_img = dft_trnsf(img)
dft_img_log = cnvrt_from_cmplx(dft_img)
dft_img_rounded = np.around(dft_img_log, 5)

# np function for fft
fft = fftpack.fft2(img)
fft_log = cnvrt_from_cmplx(fft)
fft_round = np.around(fft_log, 5)

# IDFT transform image
idft_img = idft_trnsf(dft_img)
idft_img = np.around(idft_img, 5)
idft_img = np.absolute(idft_img)
print(idft_img)

# Using numpy function for IDFT transformation
ifft = fftpack.ifft2(fft)
ifft = np.around(ifft, 5)
ifft = np.absolute(ifft)
print(ifft)

io.imsave('fft_transformed.png', exposure.rescale_intensity(fft_round))
io.imsave('dft_transformed.png', exposure.rescale_intensity(dft_img_rounded))
io.imsave('ifft_transformed.png', exposure.rescale_intensity(ifft))
io.imsave('idft_transformed.png', exposure.rescale_intensity(idft_img))
