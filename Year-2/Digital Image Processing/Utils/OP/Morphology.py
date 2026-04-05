import numpy as np
from PIL import Image

from Utils.GUI.Data import *
from Utils.GUI.GetUserMatrix import get_structering_element

from scipy.ndimage import binary_dilation, binary_erosion, binary_fill_holes


def complement(image):
    return Image.eval(image, lambda p: 255 - p)

def dilation(A, B):
    return binary_dilation(A, structure=B, origin=0).astype('uint8')

def erosion(A, B):
    return binary_erosion(A, structure=B, origin=0).astype('uint8')

def morphology_manager(image, operation, structering=None):
    structering = get_structering_element()

    if structering is None:
        return image

    if operation == DILATION:
        image = dilation(A=image, B=structering)
    elif operation == EROSION:
        image = erosion(A=image, B=structering)
    elif operation == OPENING:
        image = dilation(A=morphology_manager(image=image, operation=EROSION, structering=structering), B=structering)
    elif operation == CLOSING:
        image = erosion(A=morphology_manager(image=image, operation=DILATION, structering=structering), B=structering)
    elif operation == IN_BOUNDRY:
        image = abs(np.array(image) // 255 - erosion(A=image, B=structering))
    elif operation == EX_BOUNDRY:
        image = abs(dilation(A=image, B=structering) - np.array(image) // 255)
    elif operation == MORPH_GRADIENT:
        image = abs(dilation(A=image, B=structering) - erosion(A=image, B=structering))
    elif operation == FILL_HOLES:
        image = binary_fill_holes(image, structure=structering)

    return Image.fromarray((image * 255).astype(U8))