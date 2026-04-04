import pygame, sys, math

pygame.init()

#! -------------------------------------------------------- Player's Customization --------------------------------------------------------

Colors = {
    'Black':(0,0,0),
    'White':(255, 255, 255),
    'Red':(255, 0, 0),
    'Light_Blue':(125,158,192)
}

BackGround_Color    = Colors['Light_Blue']
Attacker_Color      = Colors['Red']
Defender_Color      = Colors['White']
Defending_Color     = Colors['Black']

Font = pygame.font.Font(None, 36)

Game_Mode = 'Normal'                   #? ['Normal', 'Hard'  , 'Impossible', 'Extreme Impossible': (Modifies Speed, Loop, secTime, & winScore)]
Game_Speed = 'Normal'                  #? ['Slow', 'Normal', 'Fast']
Loop = True                            #? [True, False]

secTime = 80
Time = secTime * 1000
startTime = pygame.time.get_ticks()

Score = 0
winScore = 1000

#! ----------------------------------------------------------------------------------------------------------------------------------------

screenWidth , screenHeight = 950 , 650

Clock = pygame.time.Clock()
Screen = pygame.display.set_mode((screenWidth, screenHeight))
Caption = pygame.display.set_caption(f'Escape To Survive - {Game_Mode}')

Attacker_Triangle = [(0, 0), (50, 25), (0, 50)]
Attacker = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.polygon(Attacker, (255, 0, 0), Attacker_Triangle)
Attacker_iPosition = (screenWidth * 4 / 5, screenHeight * 4 / 5)
Attacker_Rect = Attacker.get_rect(bottomright=Attacker_iPosition)
Attacker_Angel = 0

Defender_r = 25
Defender_iPosition = (screenWidth // 5 - Defender_r, screenHeight // 5 - Defender_r)
Defender_Rect = pygame.Rect(Defender_iPosition[0], Defender_iPosition[1], Defender_r * 2, Defender_r * 2)

Run = True
while Run:
    Screen.fill(BackGround_Color)

#! ----------------------------------------------------------- Game Mode & Speed ----------------------------------------------------------

    if Game_Mode == 'Normal':
        Attacker_Speed = 2
        Defender_Speed = 1
    elif Game_Mode == 'Hard':
        Attacker_Speed = 2.5
        Defender_Speed = 1
    elif Game_Mode == 'Impossible':
        Attacker_Speed = 5
        Defender_Speed = 1
 
    elif Game_Mode == 'Extreme Impossible':
        Attacker_Speed = 5
        Defender_Speed = 1
        Game_Speed = 'Fast'
        Loop = False
        Time = 60 * 1000
        winScore = 500

    if Game_Speed == 'Slow':
        Clock.tick(250)
    elif Game_Speed == 'Normal':
        Clock.tick(500)
    elif Game_Speed == 'Fast':
        Clock.tick(1000)

#! --------------------------------------------------------------- Attacker --------------------------------------------------------------

    #* Attacker Moving
    vectorDistance = (Defender_Rect.centerx - Attacker_Rect.centerx, Defender_Rect.centery - Attacker_Rect.centery)
    Distance = math.hypot(vectorDistance[0], vectorDistance[1])
    if Distance != 0:
        vectorDistance = (vectorDistance[0] / Distance, vectorDistance[1] / Distance)

    Move = (Attacker_Speed * vectorDistance[0], Attacker_Speed * vectorDistance[1])
    if Distance > 0:
        Move = (int(Move[0]), int(Move[1]))
        Attacker_Rect.move_ip(Move[0], Move[1])

    #* Attacker Aiming
    angle = math.degrees(math.atan2(vectorDistance[1], vectorDistance[0]))
    Attacker_Rotated = pygame.transform.rotate(Attacker, -angle)
    Attacker_Rect = Attacker_Rotated.get_rect(center=Attacker_Rect.center)
    
    #* Attacker Displaying
    Screen.blit(Attacker_Rotated, Attacker_Rect)

#! --------------------------------------------------------------- Defender ----------------------------------------------------------------
    key = pygame.key.get_pressed()
    
    if Loop == False:
        #* Defender Moving
        if key[pygame.K_LEFT] and Defender_Rect.left > 0:
            Defender_Rect.move_ip(-1, 0)
        elif key[pygame.K_RIGHT] and Defender_Rect.right < screenWidth:
            Defender_Rect.move_ip(1, 0)
        elif key[pygame.K_UP] and Defender_Rect.top > 0:
            Defender_Rect.move_ip(0, -1)
        elif key[pygame.K_DOWN] and Defender_Rect.bottom < screenHeight:
            Defender_Rect.move_ip(0, 1)

        if key[pygame.K_UP] and key[pygame.K_LEFT] and Defender_Rect.left > 0 and Defender_Rect.top > 0:
            Defender_Rect.move_ip(-1, -1)
        elif key[pygame.K_UP] and key[pygame.K_RIGHT] and Defender_Rect.right < screenWidth and Defender_Rect.top > 0:
            Defender_Rect.move_ip(1, -1)
        elif key[pygame.K_DOWN] and key[pygame.K_LEFT] and Defender_Rect.left > 0 and Defender_Rect.bottom < screenHeight:
            Defender_Rect.move_ip(-1, 1)
        elif key[pygame.K_DOWN] and key[pygame.K_RIGHT] and Defender_Rect.right < screenWidth and Defender_Rect.bottom < screenHeight:
            Defender_Rect.move_ip(1, 1)

    elif Loop == True:
        #* Defender Moving
        if key[pygame.K_LEFT]:
            Defender_Rect.move_ip(-1, 0)
        elif key[pygame.K_RIGHT]:
            Defender_Rect.move_ip(1, 0)
        elif key[pygame.K_UP]:
            Defender_Rect.move_ip(0, -1)
        elif key[pygame.K_DOWN]:
            Defender_Rect.move_ip(0, 1)

        if key[pygame.K_UP] and key[pygame.K_LEFT]:
            Defender_Rect.move_ip(-1, -1)
        elif key[pygame.K_UP] and key[pygame.K_RIGHT]:
            Defender_Rect.move_ip(1, -1)
        elif key[pygame.K_DOWN] and key[pygame.K_LEFT]:
            Defender_Rect.move_ip(-1, 1)
        elif key[pygame.K_DOWN] and key[pygame.K_RIGHT]:
            Defender_Rect.move_ip(1, 1)

        #* Defender Looping
        if Defender_Rect.left > screenWidth:
            Defender_Rect.right = 0
        elif Defender_Rect.right < 0:
            Defender_Rect.left = screenWidth
        elif Defender_Rect.top > screenHeight:
            Defender_Rect.bottom = 0
        elif Defender_Rect.bottom < 0:
            Defender_Rect.top = screenHeight
            
    #* Defender Displaying
    pygame.draw.circle(Screen, Defender_Color, Defender_Rect.center, Defender_r)

#! ------------------------------------------------------------- Play Status -------------------------------------------------------------

    #* Attacking Mode
    if Attacker_Rect.colliderect(Defender_Rect) and not key[pygame.K_SPACE]:
        Defender_Color = Attacker_Color

        #* Update Score and Result
        if Score < winScore   and Game_Mode == 'Normal':
            Score += 0.10
        elif Score < winScore and Game_Mode == 'Hard':
            Score += 0.15
        elif Score < winScore and Game_Mode == 'Impossible':
            Score += 0.20
        elif Score < winScore and Game_Mode == 'Extreme Impossible':
            Score += 0.25
        else:
            Result = Font.render('Attacker Wins!', True, (255, 255, 255))
            Screen.blit(Result, (screenWidth // 2 - 100, screenHeight // 2 - 20))
            pygame.display.flip()
            pygame.time.wait(2000)
            Run = False
            
    #* Defending Mode
    elif key[pygame.K_SPACE]:
        Defender_Color = Defending_Color
        
        #* Update Score and Result
        if Score < winScore   and Game_Mode == 'Normal':
            Score += 0.05
        elif Score < winScore and Game_Mode == 'Hard':
            Score += 0.10
        elif Score < winScore and Game_Mode == 'Impossible':
            Score += 0.15
        elif Score < winScore and Game_Mode == 'Extreme Impossible':
            Score += 0.20
        else:
            Result = Font.render('Defender Loses!', True, (255, 255, 255))
            Screen.blit(Result, (screenWidth // 2 - 100, screenHeight // 2 - 20))
            pygame.display.flip()
            pygame.time.wait(3000)
            Run = False

    else:
        Defender_Color = Colors['White']

#! --------------------------------------------------------- Display Score & Time --------------------------------------------------------- 

    displayScore = Font.render(f'Score: {round(Score, 2)} / {winScore}', True, (255, 255, 255))
    Screen.blit(displayScore, (10, 10))

    elapsedTime = pygame.time.get_ticks() - startTime
    elapsedSeconds = elapsedTime // 1000
    displayTime = Font.render(f'Time: {elapsedSeconds} / {secTime}', True, (255, 255, 255))
    Screen.blit(displayTime, (screenWidth - 160, 10))
    
#! -------------------------------------------------------------- Reset Game --------------------------------------------------------------
 
    key = pygame.key.get_pressed()
    if key[pygame.K_TAB]:
        Attacker_Rect.bottomright = Attacker_iPosition
        Attacker_Angel = 0
        Defender_Rect.topleft = Defender_iPosition
        startTime = pygame.time.get_ticks()
        Score = 0

#! --------------------------------------------------------------- End Game --------------------------------------------------------------- 

    if elapsedTime > Time:
        Result = Font.render('Defender Wins!', True, (255, 255, 255))
        Screen.blit(Result, (screenWidth // 2 - 100, screenHeight // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(3000)
        Run = False
        
    elif key[pygame.K_ESCAPE]:
        Run = False

#! -------------------------------------------------------------- Quit Game --------------------------------------------------------------- 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Run = False

#! ---------------------------------------------------------------------------------------------------------------------------------------- 

    pygame.display.update()
    
pygame.quit()
sys.exit()