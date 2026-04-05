import numpy as np
import PIL.Image as Image
import matplotlib.pyplot as plt

from Utils.GUI.Data import *


def histogram_operations_manager(image, operation):
    if operation == STRETCH: 
        return histogramStretching(image=image)
    if operation == EQUALIZE:
        return histogramEqualizing(image=image)


def histogramStretching(image, return_data=False):
    def stretch(Pixel: int, Min: int, Max: int):
        return np.clip(np.round((255.0 * (Pixel - Min) / (Max - Min))), 0, 255)

    if image.mode == IMG_MODES[1]: # L
        Min, Max = np.min(image), np.max(image)
        LUT = [stretch(p, Min, Max) for p in range(256)]
        image = Image.eval(image, lambda p: LUT[p])
    elif image.mode == IMG_MODES[0]:
        image = Image.merge(RGB, [histogramStretching(c) for c in image.split()])
    return (image if not return_data else (image, (Min, Max, LUT)))


def histogramEqualizing(image, return_data=False):
    if image.mode == IMG_MODES[1]: # L 
        Histogram = image.histogram()
        SUM = np.sum(Histogram)
        PDF = [i / SUM for i in Histogram]
        CDF = np.cumsum(PDF)
        LUT = [round(i * 255) for i in CDF]
        image = Image.eval(image, lambda p: LUT[p])
    elif image.mode == IMG_MODES[0]:
        image = Image.merge(RGB, [histogramEqualizing(c) for c in image.split()])
    return (image if not return_data else (image, (PDF, CDF, LUT)))


def histogram_operations_plot_manager(image, operation):
    if operation == STRETCH: 
        return histogramStretching_plot(image=image)
    if operation == EQUALIZE:
        return histogramEqualizing_plot(image=image)


def histogramStretching_plot(image):
    image = image.convert('L')
    Histogram = image.histogram()
    stretched_image, (Min, Max, LUT) = histogramStretching(image=image, return_data=True)
    stretched_Histogram = stretched_image.histogram()
    stretched_Min, stretched_Max = np.min(stretched_image), np.max(stretched_image)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

    ax1.plot(range(256), Histogram, color=RED, linewidth=0.75)
    ax1.plot(range(256), stretched_Histogram, color=BLK, linewidth=0.75)
    
    for edge in [Min, Max]: ax1.axvline(x=edge, color=RED, linewidth=0.75, linestyle='--')
    for edge in [stretched_Min, stretched_Max]: ax1.axvline(x=edge, color=BLK, linewidth=0.75, linestyle='--')
    
    ax2.plot(range(256), LUT, color='black', linewidth=0.75)

    axs, lbls = [ax1, ax2], ['Histogram', 'LUT']
    for i in range(len(axs)):
        axs[i].set_title(lbls[i])
        axs[i].grid()
    plt.show()


def histogramEqualizing_plot(image):
    image = image.convert('L')
    Histogram = image.histogram()
    equalized_image, (PDF, CDF, LUT) = histogramEqualizing(image=image, return_data=True)
    equalized_Histogram = equalized_image.histogram()

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8, 8))

    ax1.plot(range(256), Histogram, color=RED, linewidth=0.75)
    ax1.plot(range(256), equalized_Histogram, color=BLK, linewidth=0.75)

    ax2.bar(range(256), PDF, color='black', width=0.75, linewidth=0.75)
    ax3.plot(range(256), CDF, color='black', linewidth=0.75)
    ax4.plot(range(256), LUT, color='black', linewidth=0.75)


    axs, lbls = [ax1, ax2, ax3, ax4], ['Histogram', 'PDF', 'CDF', 'LUT']
    for i in range(len(axs)):
        axs[i].set_title(lbls[i])
        axs[i].grid()

    plt.tight_layout()
    plt.show()