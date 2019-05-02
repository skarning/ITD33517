import numpy as np
from skimage import io, util, color
from scipy import fftpack


# Import an image from path as ubyte
def import_img(img_path):
    return util.img_as_ubyte(color.rgb2gray(io.imread(img_path)))


# Fast fourier transformation and log transformation on image
def fft_and_log_transform(img):
    fft = fftpack.fft2(img)

    # Log transform code is from Github lavima
    fft = np.absolute(fft)
    log_trns = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            log_trns = np.log(1+img[i, j])
    return np.around(log_trns, 5)
