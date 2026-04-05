import numpy as np
import PIL.Image as Image

from Utils.GUI.Data import *
from Utils.GUI.GetUserMatrix import get_user_matrix


def get_rank(Matrix, Rank):
    return np.sort(Matrix.flatten())[Rank - 1]

def get_mode(Matrix):
    values, counts = np.unique(Matrix.ravel(), return_counts=True)
    return values[np.argmax(counts)]

def get_kernel_mode(kernel_string):
    kernel_string = kernel_string.lower()
    if kernel_string == MODE:
        return get_mode
    elif kernel_string.startswith(RANK):
        return kernel_string
    elif kernel_string.startswith(OUTLIER):
        return kernel_string
    else:
        return KERNELS[kernel_string]

def get_kernel_matrix(kernel_string):
    kernel_matrix = kernel_string.upper().split()[0]
    if kernel_matrix == 'LPF':
        kernel_matrix = LPF
    elif kernel_matrix == 'HPF':
        kernel_matrix = HPF
    else:
        kernel_matrix = get_user_matrix()
    try:
        return kernel_matrix * float(kernel_string.upper().split()[1])
    except:
        return kernel_matrix


def neighborhood_operations_manager(image, info: tuple):
    kernel_mode = get_kernel_mode(info[0])

    if info[1].isdigit():
        kernel_size = int(info[1])
        if image.mode == L:
            return Image.fromarray(neighborhood_operations(image, kernel_mode, kernel_size).astype(U8))
        else:
            return Image.merge(RGB,
                [Image.fromarray(neighborhood_operations(i, kernel_mode, kernel_size).astype(U8)) for i in image.split()])
    else:
        kernel_matrix = get_kernel_matrix(info[1])
        if image.mode == L:
            return Image.fromarray(weighted_neighborhood_operations(image, kernel_mode, kernel_matrix).astype(U8))
        else:
            return Image.merge(RGB,
                [Image.fromarray(weighted_neighborhood_operations(i, kernel_mode, kernel_matrix).astype(U8)) for i in image.split()])


def neighborhood_operations(image, kernel_mode: callable, kernel_size: int):
    input_matrix = np.array(image)
    padded_matrix = np.pad(input_matrix, kernel_size // 2, mode=CONST, constant_values=0)
    output_matrix = np.zeros_like(input_matrix, dtype=int)

    if isinstance(kernel_mode, str):
        if kernel_mode.startswith(RANK):
            Rank = int(kernel_mode.split()[-1]) # e.g. 'Rank 3'
            for i in range(input_matrix.shape[0]):
                for j in range(input_matrix.shape[1]):
                    neighborhood_matrix = padded_matrix[i:i+kernel_size, j:j+kernel_size]
                    output_matrix[i, j] = np.clip(np.round(get_rank(neighborhood_matrix, Rank)), 0, 255)

        elif kernel_mode.startswith(OUTLIER):
            Threshold = int(kernel_mode.split()[-1]) # e.g. 'Outlier 10'
            for i in range(input_matrix.shape[0]):
                for j in range(input_matrix.shape[1]):
                    neighborhood_matrix = padded_matrix[i:i+kernel_size, j:j+kernel_size]
                    pixel = input_matrix[i, j]
                    neighbors_mean = np.mean(neighborhood_matrix[neighborhood_matrix != pixel])
                    output_matrix[i, j] = np.round(neighbors_mean) if abs(pixel - neighbors_mean) > Threshold else pixel
    else:
        for i in range(input_matrix.shape[0]):
            for j in range(input_matrix.shape[1]):
                neighborhood_matrix = padded_matrix[i:i+kernel_size, j:j+kernel_size]
                output_matrix[i, j] = np.clip(np.round(kernel_mode(neighborhood_matrix)), 0, 255)
    return output_matrix

def weighted_neighborhood_operations(image, kernel_mode: callable, kernel_matrix: callable):
    kernel_size = kernel_matrix.shape[0]
    input_matrix = np.array(image)
    padded_matrix = np.pad(input_matrix, kernel_size // 2, mode=CONST, constant_values=0)
    output_matrix = np.zeros_like(input_matrix, dtype=int)

    if isinstance(kernel_mode, str) and kernel_mode.startswith(RANK):
        Rank = int(kernel_mode.split()[-1])
        for i in range(input_matrix.shape[0]):
            for j in range(input_matrix.shape[1]):
                neighborhood_matrix = padded_matrix[i:i+kernel_size, j:j+kernel_size] * kernel_matrix
                output_matrix[i, j] = np.clip(np.round(get_rank(neighborhood_matrix, Rank)), 0, 255)
    else:
        for i in range(input_matrix.shape[0]):
            for j in range(input_matrix.shape[1]):
                neighborhood_matrix = padded_matrix[i:i+kernel_size, j:j+kernel_size] * kernel_matrix
                output_matrix[i, j] = np.clip(np.round(kernel_mode(neighborhood_matrix)), 0, 255)

    return output_matrix

# `spatial_filtering` is `weighted_neighborhood_operations` with either `kernel_matrix= HPF | LPF` and `kernel_mode=np.sum`