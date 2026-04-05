import numpy as np
from PIL import Image
from skimage.filters import threshold_otsu

from Utils.GUI.Data import *

def OTSU(image):
    return threshold_otsu(np.array(image.convert(L)))

def AUTO(image):
    matrix = np.array(image.convert(L)).flatten()
    theta = np.mean(matrix)

    while True:
        a = matrix[matrix <= theta]
        b = matrix[matrix >  theta]

        pre_theta = theta
        theta = 0.5 * (np.mean(a) + np.mean(b))

        if abs(theta - pre_theta) <= 0.25:
            break

    return round(theta)


def average(matrix):
    return round(np.ptp(matrix) / 2)

def get_mode(mode_string):
    if mode_string == MEAN:
        return np.mean
    elif mode_string == MEDIAN:
        return np.median
    else:
        return average


def thresholding_manager(image, info: tuple[str, str]):
    mode = info[0]

    if mode == THRESHOLDING_OPTIONS_LIST[2]:
        return global_n_layer(image=image, num_of_layers=int(info[1]))
    
    image = image.convert(L)
    
    if mode == THRESHOLDING_OPTIONS_LIST[0]:
        try:
            return global_single(image=image, threshold=int(info[1]))
        except:
            return global_single(image=image, threshold={'auto': AUTO(image), 'otsu': OTSU(image)}[info[1].lower()])

    if mode == THRESHOLDING_OPTIONS_LIST[1]: # Douple TH Value: 'low high choise'
        data = tuple(int(i) for i in info[1].split())
        return global_double(image, low=data[0], high=data[1], choise=data[2])

    else:
        return local_thresholding(image=image, mode=info[0].split()[1], size=int(info[1]))


def global_single(image, threshold):
    return image.point(lambda p: 0 if p < threshold else 255, '1')


def global_double(image, low, high, choise):
    if choise == 0:
        return image.point(lambda p: 255 if p < low or p > high else 0, '1')
    if choise == 1:
        return image.point(lambda p: 0 if p < low or p > high else 255, '1')


def global_n_layer(image, num_of_layers):
    if image.mode == L:
        step = 255 // num_of_layers
        lut_cls = [i // step for i in range(256)]
        lut = [lut_cls[i % len(lut_cls)] * step for i in range(256)]
        image = Image.eval(image.convert('L'), lambda x: lut[x])
    else:
        image = image.quantize(colors=num_of_layers)
    return image


def local_thresholding(image, mode, size):
    input_matrix = np.array(image.convert('L'))
    padded_matrix = np.pad(input_matrix, size // 2, mode='constant', constant_values=0)
    output_matrix = np.zeros_like(input_matrix, dtype=int)

    mode = get_mode(mode.lower())

    for i in range(input_matrix.shape[0]):
        for j in range(input_matrix.shape[1]):
            neighborhood_matrix = padded_matrix[i:i+size, j:j+size]            
            output_matrix[i, j] = 255 if input_matrix[i, j] > mode(neighborhood_matrix) else 0

    return Image.fromarray(output_matrix.astype(np.uint8))