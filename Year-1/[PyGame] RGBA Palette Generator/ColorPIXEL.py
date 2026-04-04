import math, random

import Functions as F

def colorize(L, x, y, P):
    
    P = P.upper()
        
    if all(i in P for i in ['R', 'G', 'B', 'A']):
        R = F.limit(255 * (L - x) / L * (L - y) / L)
        G = F.limit(255 * (y / L) * (L - x) / L)
        B = F.limit(255 * (x / L) * (L - y) / L)
        A = F.limit(255 - (10 * (x + y) / (L / 2)))
    
    elif all(i in P for i in ['R', 'G', 'B']):
        R = F.limit(255 * (L - x) / L * (L - y) / L)
        G = F.limit(255 * (y / L) * (L - x) / L)
        B = F.limit(255 * (x / L) * (L - y) / L)
        A = 255

    elif P in ['R', 'G' ,'B', 'W', 'K']:
        R = 255 if P in ['R', 'W'] else 0
        G = 255 if P in ['G', 'W'] else 0
        B = 255 if P in ['B', 'W'] else 0
        A = F.limit(255 - ((x + y) / (L / 50)))

    elif all(i in P for i in ['R', 'G']):
        R = G = 255
        B = 0
        A = F.limit(255 - ((x + y) / (L / 50)))
    
    elif all(i in P for i in ['G', 'B']):
        R = 0
        G = B = 255
        A = F.limit(255 - ((x + y) / (L / 50)))
        
    elif all(i in P for i in ['R', 'B']):
        R = B = 255
        G = 0
        A = F.limit(255 - ((x + y) / (L / 50)))

    elif all(i in P for i in ['B', 'W']):
        R = G = B = F.limit(((y + x) * (y - x)) / math.sqrt(2) * L)
        A = F.limit(255 - ((x + y) / (L / 35)))
        
    elif P == 'FAV':
        R = F.limit(math.sin(x / L * math.pi) * 255)
        G = F.limit(math.cos(y / L * math.pi) * 255)
        B = F.limit((math.sin(x / L * math.pi) + math.cos(y / L * math.pi)) * 127 + 128)
        A = 255
        
    else:
        RI = random.randint
        R = F.limit(RI(0, 255))
        G = F.limit(RI(0, 255))
        B = F.limit(RI(0, 255))
        A = F.limit(RI(0, 255))
        
    return (R, G, B, A)


def getColor(L, x, y, P):
    return colorize(L, x, y, P)