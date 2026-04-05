import numpy as np
from PIL import Image, ImageFilter

from Utils.GUI.Data import *


def edge_detection_manager(image, info):
    algorithm, do_enhance = info[0], info[1]

    if algorithm == 'Laplacian':
        image = laplacian(image=image)
    elif algorithm == 'Gradient':
        image = gradient(image=image)
    elif algorithm == 'Roberts':
        image = roberts(image=image)
    elif algorithm == 'Prewitt':
        image = prewitt(image=image)
    elif algorithm == 'Sobel':
        image = sobel(image=image)

    return (image if not do_enhance else enhance(image))

def gradient(image):
    image = image.convert(L)
    diff_x, diff_y = Image.new(L, image.size), Image.new(L, image.size)

    for y in range(image.height):
        for x in range(image.width):
            if x > 0: 
                diff_x.putpixel((x, y), abs(image.getpixel((x, y)) - image.getpixel((x-1, y))))
            if y > 0: 
                diff_y.putpixel((x, y), abs(image.getpixel((x, y)) - image.getpixel((x, y-1))))

    return Image.fromarray(np.add(np.array(diff_x), np.array(diff_y)).astype('uint8'))


def laplacian(image):
    input_matrix = np.array(image.convert(L))
    padded_matrix = np.pad(input_matrix, 1, mode='constant', constant_values=0)
    output_matrix = np.zeros_like(input_matrix, dtype=int)

    for i in range(input_matrix.shape[0]):
        for j in range(input_matrix.shape[1]):
            neighborhood_matrix = padded_matrix[i:i+3, j:j+3] * LAPLACIAN
            output_matrix[i, j] = np.clip(np.round(np.mean(neighborhood_matrix)), 0, 255)
            
    return Image.fromarray(output_matrix.astype('uint8'))


def sobel(image):
    image = np.array(image.convert(L))
    sobel_x = sobel_y = np.zeros_like(image, dtype=int)
    
    for y in range(1, image.shape[0]-1):
        for x in range(1, image.shape[1]-1):
            sobel_x[y, x] = np.clip(np.sum(SOBEL_X * image[y-1:y+2, x-1:x+2]), 0, 255)
            sobel_y[y, x] = np.clip(np.sum(SOBEL_Y * image[y-1:y+2, x-1:x+2]), 0, 255)

    return Image.fromarray(np.sqrt(np.array(sobel_x)**2 + np.array(sobel_y)**2).astype('uint8'))


def prewitt(image):
    image = np.array(image.convert(L))
    prewitt_x = prewitt_y = np.zeros_like(image, dtype=int)

    for y in range(1, image.shape[0]-1):
        for x in range(1, image.shape[1]-1):
            prewitt_x[y, x] = np.clip(np.sum(PREWITT_X * image[y-1:y+2, x-1:x+2]), 0, 255)
            prewitt_y[y, x] = np.clip(np.sum(PREWITT_Y * image[y-1:y+2, x-1:x+2]), 0, 255)

    return Image.fromarray(np.sqrt(np.array(prewitt_x)**2 + np.array(prewitt_y)**2).astype('uint8'))


def roberts(image):
    image = np.array(image.convert(L))
    roberts_x = roberts_y = np.zeros_like(image, dtype=int)

    for y in range(1, image.shape[0]-1):
        for x in range(1, image.shape[1]-1):
            roberts_x[y, x] = np.clip(np.abs(np.sum(ROBERTS_X * image[y:y+2, x:x+2])), 0, 255)
            roberts_y[y, x] = np.clip(np.abs(np.sum(ROBERTS_Y * image[y:y+2, x:x+2])), 0, 255)

    return Image.fromarray(np.sqrt(np.array(roberts_x)**2 + np.array(roberts_y)**2).astype('uint8'))


def enhance(image):
    return image.filter(ImageFilter.EDGE_ENHANCE)