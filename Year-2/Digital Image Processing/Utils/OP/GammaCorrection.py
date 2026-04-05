import PIL.Image as Image
import matplotlib.pyplot as plt


def gamma(Pixel: int, Gamma: float) -> int:
    return round(255 * ((Pixel / 255) ** Gamma))

def gamma_correction_manager(image, gamma_value: float):
    LUT = [gamma(p, gamma_value) for p in list(range(256))]
    return Image.eval(image, lambda p: LUT[p])

def plot_gamma_correction_LUT(gamma_value: float):
    LUT = [gamma(p, gamma_value) for p in list(range(256))]
    plt.figure(figsize=(5, 5))
    plt.plot(range(256), LUT, color='black', linewidth=0.75)
    plt.title(f'Gamma Correction IO-LUT For λ = {gamma_value}', y=1.05)
    plt.axis('on')
    plt.grid(True)
    plt.show()