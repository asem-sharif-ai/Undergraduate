import numpy as np

from ColorPIXEL import colorize

def limit(value):
    return min(max(int(value), 0), 255)

def getVector(value):
    String = bin(limit(value))[2:].zfill(8)
    Vector = np.array([int(bit) for bit in String])
    return Vector

def getMatrix(colorTuple):
    colorMatrix = np.zeros((len(colorTuple), 8), dtype = np.uint8)
    for i, value in enumerate(colorTuple):
        colorMatrix[i] = getVector(value)
    return colorMatrix

def getMatrix_info(Matrix):
    RGBA = ['R', 'G', 'B', 'A']
    textLines = []
    for i in range(Matrix.shape[0]):
        textLines.append(f'{RGBA[i]} : {Matrix[i]}')
    info = '\n'.join(textLines)
    return info

def detect(colorTuple):
    MAXs = sorted(colorTuple[:-1], reverse = True)
    
    if MAXs[0] - MAXs[1] < 50 and MAXs[1] - MAXs[2] < 50:
        if max(MAXs) <= 10:
            return f'Black.'
        elif max(MAXs) <= 25:
            return f'almost Black (RGB).'
        elif max(MAXs) <= 200:
            return f'based on Grey (RGB).'
        elif max(MAXs) <= 240:
            return f'almost White (RGB).'
        elif max(MAXs) <= 255:
            return f'White.'
    
    if MAXs[0] == colorTuple[0]:
        if MAXs[0] - MAXs[1] >= 100:
            return f'based on Red.'
        elif MAXs[1] == colorTuple[1]:
            return f'based on Red & Green.'
        elif MAXs[1] == colorTuple[2]:
            return f'based on Red & Blue.'
        
    elif MAXs[0] == colorTuple[1]:
        if MAXs[0] - MAXs[1] >= 100:
            return f'based on Green.'
        elif MAXs[1] == colorTuple[0]:
            return f'based on Green & Red.'
        elif MAXs[1] == colorTuple[2]:
            return f'based on Green & Blue.'
        
    elif MAXs[0] == colorTuple[2]:
        if MAXs[0] - MAXs[1] >= 100:
            return f'based on Blue.'
        elif MAXs[1] == colorTuple[0]:
            return f'based on Blue & Red.'
        elif MAXs[1] == colorTuple[1]:
            return f'based on Blue & Green.'

def detect_info(colorTuple):
    try:
        R = round(((colorTuple[0] / (colorTuple[0] + colorTuple[1] + colorTuple[2])) * 100), 2)
        G = round(((colorTuple[1] / (colorTuple[0] + colorTuple[1] + colorTuple[2])) * 100), 2)
        B = round(((colorTuple[2] / (colorTuple[0] + colorTuple[1] + colorTuple[2])) * 100), 2)
    except:   # ZeroDivisionError (Black Case)
        R = G = B = 0
    A = round(((colorTuple[3] / 255) * 100), 2)

    info = [
        f'R: {R:05.2f}%',
        f'G: {G:05.2f}%',
        f'B: {B:05.2f}%',
        f'A: {A:05.2f}%'
    ]
    return info


# Palette Map: ['RGB' 'RGBA' 'R' 'G' 'B' 'W' 'K' 'RG' 'GB' 'RB' 'BW' 'FAV']

def getFontColor(P, i):
    if P.upper() in ['RGB', 'RGBA', 'K']:
        return (255, 255, 255)
    if P.upper() in ['R', 'G', 'B', 'W', 'RG', 'GB', 'RB']:
        return (0, 0, 0)
    if P.upper() in  ['BW', 'WB']:
        return (255, 255, 255) if i == 1 else (0, 0, 0)
    if P.upper() == 'FAV':
        return (0, 0, 0) if i == 1 else (255, 255, 255)


def getName(P):
        return f'_{P.upper()}.png'