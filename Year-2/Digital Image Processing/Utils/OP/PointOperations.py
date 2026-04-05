import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from Utils.GUI.Data import *


def point_operations_manager(image, info: tuple):
    operation = info[0]
    channel = info[1]
    factor = int(info[2])

    if is_expression(operation):
        return apply_expression(image=image, expression=operation)

    if operation == ELIMINATE:
        return eliminate_channels(image, channel)
    elif operation == SWAP:
        return swap_channels(image, channel)

    if len(channel) == 3 or channel == L:
        return point_operations_combined(image, operation, factor)
    else:
        return point_operations_separated(image, operation, channel, factor)


def get_point_operations_LUT(operation, factor):
    if operation == ADD:
        LUT = [x + factor for x in range(256)]
    elif operation == SUBTRACT:
        LUT = [x - factor for x in range(256)]
    elif operation == MULTIPLY:
        LUT = [x * max(factor, 1) for x in range(256)]
    elif operation == DIVIDE:
        LUT = [x // max(factor, 1) for x in range(256)]
    elif operation == COMPLEMENT:
        LUT = [255 - x for x in range(256)]
    elif operation == SOLARIZE_D:
        LUT = [x if x >= factor else 255 - x for x in range(256)]
    elif operation == SOLARIZE_L:
        LUT = [x if x <= factor else 255 - x for x in range(256)]
    elif is_expression(operation):
        LUT = [eval_expression(operation, i) for i in range(256)]
    else: raise
    return LUT


def apply_expression(image, expression):
    LUT = get_point_operations_LUT(operation=expression, factor=None)
    image = Image.eval(image, lambda x: LUT[x])
    return image


def point_operations_combined(image, operation, factor):
    LUT = get_point_operations_LUT(operation=operation, factor=factor)
    image = Image.eval(image, lambda x: LUT[x])
    return image


def point_operations_separated(image, operation, channel, factor):
    R, G, B = image.split()
    if 'R' in channel:
        R = point_operations_combined(R, factor=factor, operation=operation)
    if 'G' in channel:
        G = point_operations_combined(G, factor=factor, operation=operation)
    if 'B' in channel:
        B = point_operations_combined(B, factor=factor, operation=operation)
    return Image.merge(RGB, (R, G, B))


def eliminate_channels(image, channels):
    R, G, B = image.split()
    if 'R' in channels:
        R = R.point(lambda p: 0)
    if 'G' in channels:
        G = G.point(lambda p: 0)
    if 'B' in channels:
        B = B.point(lambda p: 0)
    return Image.merge(RGB, (R, G, B))


def swap_channels(image, channels):
    R, G, B = image.split()
    if 'R' in channels and 'G' in channels:
        R, G = G, R
    if 'G' in channels and 'B' in channels:
        G, B = B, G
    if 'R' in channels and 'B' in channels:
        R, B = B, R
    return Image.merge(RGB, (R, G, B))


def plot_point_operations_LUT(operation, factor):
    LUT = get_point_operations_LUT(operation, factor)
    plt.figure(figsize=(5, 5))
    plt.plot(range(256), np.clip(LUT, 0, 255), color='red', linewidth=0.75)
    plt.xlim(0, 256)
    plt.ylim(0, 256)
    plt.axis('on')
    plt.grid(True)
    plt.show()


def point_operations_adv_manager(image, info):
    sub_image = info[0]
    operation = info[1]

    main_array = np.array(image)
    side_array = np.array(sub_image.resize(image.size))

    if operation == ADD:
        result_array = np.add(main_array, side_array)
    elif operation == SUBTRACT:
        result_array = np.subtract(main_array, side_array)
    elif operation == MULTIPLY:
        result_array = np.multiply(main_array, side_array)
    elif operation == DIVIDE:
        result_array = np.divide(main_array, np.maximum(side_array, 1))
    elif operation == AVERAGE:
        result_array = np.add(main_array, side_array) // 2
    elif operation == MIN:
        result_array = np.minimum(main_array, side_array)
    elif operation == MAX:
        result_array = np.maximum(main_array, side_array)
    elif operation == MATCH:
        from skimage.exposure import match_histograms
        result_array = match_histograms(main_array, side_array, channel_axis=-1)
    return Image.fromarray(result_array.astype('uint8'))