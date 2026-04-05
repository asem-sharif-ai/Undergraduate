import numpy as np
import matplotlib.pyplot as plt

from Utils.GUI.Data import *

def detectContrast(Histogram):
    MIN, MAX = 0, 255
    SUM, cumulativeSUM = sum(Histogram), 0
    lowTHRESHOLD, highTHRESHOLD = (0.10 * SUM), (0.90 * SUM)
    existMIN = existMAX = False
    for color, frequency in enumerate(Histogram):
        cumulativeSUM += frequency
        if not existMIN and cumulativeSUM >= lowTHRESHOLD:
            MIN = color
            existMIN = True
        if not existMAX and cumulativeSUM >= highTHRESHOLD:
            MAX = color
            existMAX = True
            break

    if   MAX - MIN < 100: return 'Low Contrast.'
    elif MAX - MIN > 200: return 'High Contrast.'
    else:                 return 'Normal Contrast.'


def Histogram(ImageMatrix):
    if ImageMatrix.mode in IMG_MODES[:-1]:
        if ImageMatrix.mode == RGB:
            R, G, B = ImageMatrix.split()
            fig, axs = plt.subplots(1, 3, figsize = (12, 6), sharey = True)
            ImageHistograms = {'r': np.array(R.histogram()),
                               'g': np.array(G.histogram()),
                               'b': np.array(B.histogram())}
        else: # RGBA
            R, G, B, A = ImageMatrix.split()
            fig, axs = plt.subplots(1, 4, figsize = (12, 6), sharey = True)
            ImageHistograms = {'r': np.array(R.histogram()),
                               'g': np.array(G.histogram()),
                               'b': np.array(B.histogram()),
                             '0.5': np.array(A.histogram())}

        for i, key in enumerate(ImageHistograms.keys()):
            axs[i].plot(ImageHistograms[key], color = key, linewidth=0.5)
            axs[i].fill_between(range(len(ImageHistograms[key])), ImageHistograms[key], color = key, alpha = 0.85)
            axs[i].set_xlim(0, 255)
            axs[i].set_xticks(np.arange(0, 256, step = 51))
            axs[i].set_ylim(0)

    else: # L
        ImageHistogram = np.array(ImageMatrix.convert('L').histogram())
        plt.figure()
        plt.plot(ImageHistogram, color = 'k', linewidth = 0.5)
        plt.fill_between(range(len(ImageHistogram)), ImageHistogram, color = 'k', alpha = 0.85)
        plt.xlim(0, 255) ; plt.xticks(np.arange(0, 256, step = 17))
        plt.ylim(0)
        plt.text(0.5, 1.05, detectContrast(ImageHistogram), transform = plt.gca().transAxes, ha = 'center', va = 'center')
        plt.subplots_adjust(wspace = 0.25)

    plt.show()