import numpy as np
import PIL.Image as Image

def Noise(ImageMatrix, Ratio):
    if Ratio == 0: return ImageMatrix

    np.random.seed(0)
    NP_Image = np.array(ImageMatrix)

    NoisePixels_N = int(abs(Ratio) * NP_Image.size)
    NoisePixels_I = np.random.choice(NP_Image.size, size=NoisePixels_N, replace=False)

    if Ratio > 0:
        Color = (255, 255, 255)
    elif Ratio < 0:
        Color = (0, 0, 0)

    NP_Image.flat[NoisePixels_I] = Color
    return Image.fromarray(NP_Image)