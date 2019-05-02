import numpy as np
from skimage import io, util
from scipy import ndimage


# Reads morphological image from a txt-file
def read_binary_image_from_file():
    img = []
    lst_buff = []

    with open('txt_img_morph.txt') as fl:
        for ln in fl:
            for char in ln:
                if(char == '\n'):
                    img.append(lst_buff)
                    lst_buff = []
                elif(char == '1'):
                    lst_buff.append(1)
                elif(char == '0'):
                    lst_buff.append(0)
                else:
                    lst_buff.append(-1)
    return np.asarray(img)


def rot_mat_45(mat):
    mat_buff = np.zeros((3, 3))
    mat_buff[0, 0] = mat[1, 0]
    mat_buff[0, 1] = mat[0, 0]
    mat_buff[0, 2] = mat[0, 1]
    mat_buff[1, 0] = mat[2, 0]
    mat_buff[1, 1] = mat[1, 1]
    mat_buff[1, 2] = mat[0, 2]
    mat_buff[2, 0] = mat[2, 1]
    mat_buff[2, 1] = mat[2, 2]
    mat_buff[2, 2] = mat[1, 2]
    return mat_buff


# Runs the apply SE for each pixel in image, returns result image
def thinning_iteration(img, struct_elem, n):
    for i in range(n):
        struct_elem = rot_mat_45(struct_elem)
    result_img = np.asarray((np.zeros(
        (img.shape[0], img.shape[1]))), dtype=int)
    for i in range(1, img.shape[0] - 1):
        for j in range(1, img.shape[1] - 1):
            result_img[i, j] = apply_strct_elem(j, i, img, struct_elem)
    print(f'Iterasjon: {n}')
    print('SE: ')
    print(struct_elem)
    print('Bilde')
    print(result_img)
    return result_img


# Applying structuring element
def apply_strct_elem(j, i, img, struct_elem):
    curr_pix = img[i, j]
    j -= 1
    i -= 1
    org_j = j
    eq_count = 0
    for k in range(3):
        for v in range(3):
            if img[i, j] == struct_elem[k, v] or struct_elem[k, v] == -1:
                eq_count += 1
            j += 1
        i += 1
        j = org_j
    if eq_count == 9:
        return 0
    else:
        return curr_pix


def iterate(img):
    n = 0
    SE = np.asarray([[0, 0, 0], [-1, 1, -1], [1, 1, 1]])
    while True:
        if n > 7:
            return img
        img = thinning_iteration(img, SE, n)
        n += 1


# Thinn a morphological image
def thinn(img):
    img_buffer = img
    while True:
        img = iterate(img)
        if is_imgs_equal(img, img_buffer):
            return img
        img_buffer = img


def is_imgs_equal(img1, img2):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img1[i, j] != img2[i, j]:
                return False
    return True


def convert_to_ubyte(img_in):
    width, length = img_in.shape
    for i in range(width):
        for j in range(length):
            if img_in[i, j] == 1:
                img_in[i, j] = 255
    return img_in


img = read_binary_image_from_file()
img_save_buffer = read_binary_image_from_file()
img_save_buffer = convert_to_ubyte(img_save_buffer)
io.imsave('read_binary_file.png', util.img_as_ubyte(img_save_buffer))
img = np.pad(img, 1, mode='constant')
img = thinn(img)
print(img)
img = convert_to_ubyte(img)
io.imsave('binary_image_thinned.png', util.img_as_ubyte(img))
