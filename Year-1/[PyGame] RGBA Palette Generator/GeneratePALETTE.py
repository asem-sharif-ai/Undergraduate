import os, sys, random, pygame

from Utils        import NULL_PNG, CleanUp
from Functions    import *
from ColorPIXEL   import colorize, getColor

PALETTE = None
PIN = pinX = pinY = None
showInfo = False

WHITE = (255, 255, 255)
BACKGROUND = pygame.image.load(NULL_PNG())

MAPS = ['RGB', 'RGBA', 'R', 'G', 'B', 'W', 'K', 'RG', 'GB', 'RB', 'BW', 'FAV']

def generate(PALETTE, P, L):
    global PIN, pinX, pinY

    pygame.init()
    SCREEN = pygame.display.set_mode((L, L))
    FONT1 = pygame.font.SysFont('Helvetica', 18)
    FONT2 = pygame.font.SysFont('Helvetica', 11)
    FONT3 = pygame.font.SysFont('Courier', 20)

    # pygame.display.set_icon()
    pygame.display.set_caption(f'{getName(P).split('.')[0][1:]} Model Generator - © AS')

    RUN = True
    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                RUN = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    PIN = event.pos
                    posX, posY = pygame.mouse.get_pos()
                    pinX, pinY = posX, posY
                elif event.button == 3:
                    PIN = None
                elif event.button == 2:
                    P = MAPS[(MAPS.index(P) + 1) % len(MAPS)]
                    PALETTE = None
                elif event.button in [4, 5]:
                    PIN = (random.randint(0, L), random.randint(0, L))
                    posX, posY = PIN
                    pinX, pinY = posX, posY

        SCREEN.blit(pygame.transform.scale(BACKGROUND, (L, L)), (0, 0))

        if PALETTE is not None: # Load
            SCREEN.blit(pygame.image.load(PALETTE), (0, 0))
        elif os.path.exists(getName(P)): # Was Generated In Previous Excution
            PALETTE = getName(P)
        else: # Generate & Save
            for x in range(L):
                for y in range(L):
                    Pixel = pygame.Surface((1, 1), pygame.SRCALPHA)
                    Pixel.fill(colorize(L, x, y, P))
                    SCREEN.blit(Pixel, (x, y))
            pygame.image.save(SCREEN, getName(P))
            PALETTE = getName(P)
            pygame.display.set_caption(f'{getName(P).split('.')[0][1:]} Model Generator - © AS')

        tupleFrame = pygame.Surface((L, 55), pygame.SRCALPHA)
        tupleFrame.fill((0, 0, 0, 175))
        SCREEN.blit(tupleFrame, ((L - tupleFrame.get_width()) // 2, 20))

        matrixFrame = pygame.Surface((213, 93), pygame.SRCALPHA)
        matrixFrame.fill((0, 0, 0, 175))
        SCREEN.blit(matrixFrame, (10, L - 102))

        if PIN is None: # Follow cursor position
            posX, posY = pygame.mouse.get_pos()
            posTuple = getColor(L, posX, posY, P)
        else: # Stick to pin position
            SCREEN.set_at(PIN, WHITE)
            l = L // 35 # Square L
            pygame.draw.rect(SCREEN, WHITE, ((pinX - l // 2), (pinY - l // 2), l, l), 1)
            
            posInfo = detect_info(getColor(L, pinX, pinX, P))
            for i, row in enumerate(posInfo):
                matrixText = FONT2.render(str(row), True, WHITE)
                SCREEN.blit(matrixText, (8, 22 + i * matrixText.get_height()))
                
            posTuple = getColor(L, pinX, pinY, P)

        # if min(pygame.mouse.get_pos()) == 0 or max(pygame.mouse.get_pos()) == L-1:
        #     PIN = (random.randint(0, L), random.randint(0, L))
        #     posX, posY = PIN
        #     pinX, pinY = posX, posY
        #     pygame.event.wait(3000)

        tupleText = ' '.join(tuple(f'{item:03d}' for item in posTuple))
        tupleText = FONT1.render(f'({tupleText})', True, WHITE)
        SCREEN.blit(tupleText, ((L - tupleText.get_width()) // 2, 25))

        colorText = f'Pixel ({posX:03} | {posY:03}) is {detect(posTuple)}'
        colorText = FONT1.render(colorText, True, WHITE)
        SCREEN.blit(colorText, ((L - colorText.get_width()) // 2, 50))

        for i, row in enumerate(getMatrix(posTuple)):
            matrixText = FONT3.render(str(row), True, WHITE)
            SCREEN.blit(matrixText, (15, L - 17 - 20 * (4 - i)))

        pygame.display.flip()
        
    CleanUp() # You may want to uncomment this
    pygame.quit()
    sys.exit()