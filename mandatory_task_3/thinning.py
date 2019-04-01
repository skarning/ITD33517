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


# thinning iteration runs until the image converges
def thinning_iteration(img, struct_elem, angle):
    struct_elem = ndimage.interpolation.rotate(struct_elem, angle)
    img = np.pad(img, 1, mode='constant')

    for i in range(1, img.shape[0] - 1):
        for j in range(1, img.shape[1] - 1):
            apply_strct_elem(j, i, img, struct_elem)
    return img


# Applying structuring element
def apply_strct_elem(j, i, img, struct_elem):
    j -= 1
    i -= 1
    org_j = j
    for k in range(3):
        for v in range(3):
            print(img[j, i])
            j += 1
        i += 1
        j = org_j
    return 1


img = read_binary_image_from_file()
print(img)
img = thinning_iteration(img, [[0, 0, 0], [-1, 1, -1],
                               [1, 1, 1]], 0)
print(img)
io.imsave('binary_image.pbm', util.img_as_ubyte(img))
