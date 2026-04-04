import pygame, os, shutil

def NULL_PNG(L = 500):
    pygame.init()
    
    SIZE = 5
    NUMBER = round(L / SIZE)
    SCREEN = pygame.Surface((L, L))
    BACKGROUND = [(255, 255, 255), (200, 200, 200)]

    for R in range(NUMBER):
        for C in range(NUMBER):
            PIXEL = BACKGROUND[(R + C) % 2]
            pygame.draw.rect(SCREEN, PIXEL, (C * SIZE, R * SIZE, SIZE, SIZE))

    NAME = '_NULL.png'
    pygame.image.save(SCREEN, NAME)

    pygame.quit()
    return NAME


def Clean(dir, signs):
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            if dir == '__pycache__':
                pycache_path = os.path.join(root, dir)
                shutil.rmtree(pycache_path)

    for file in os.listdir(os.getcwd()):
        if any(file.startswith(sign) for sign in signs):
            os.remove(os.path.join(os.getcwd(), file))

def CleanUp():
    return Clean('.', ('_', 'temp'))