import pygame, random, os

def image(name):
    DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(DIR, f'_{name}.png')

#! ----------------------------------------------------------------------------------------------------

class Piece(pygame.sprite.Sprite):
    def __init__(self, piece_type, x, y):
        super().__init__()
        self.type = piece_type
        self.image = self.get_image(piece_type)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = random.uniform(-2.5, 5)
        self.velocity_y = random.uniform(-2.5, 5)

#? --------------------------------------------------

    @classmethod
    def initialize(cls, piece_types, piece_number, width, height):
        piece_group = pygame.sprite.Group()
        piece_count = {type: 0 for type in piece_types}

        for type in piece_types:
            for _ in range(piece_number):
                x = random.randint(0, width - 50)
                y = random.randint(0, height - 50)
                piece = cls(type, x, y)
                piece_group.add(piece)
                piece_count[type] += 1

        return piece_group, piece_count

#? --------------------------------------------------

    @classmethod
    def reset_counters(cls, piece_group):
        piece_count = {piece_type: 0 for piece_type in PIECE_TYPES}
        for piece in piece_group:
            piece_count[piece.type] += 1
        return piece_count

#? --------------------------------------------------

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        self.velocity_x += random.uniform(-0.1, 0.1)        # add some randomness to velocity changes
        self.velocity_y += random.uniform(-0.1, 0.1)

        if self.rect.left <= 0 or self.rect.right >= WIDTH: # consider screen edges
            self.velocity_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.velocity_y *= -1

#? --------------------------------------------------

    def resolve(self, piece_group):
        collisions = pygame.sprite.groupcollide(piece_group, piece_group, False, False)
        for piece_A in collisions:
            for piece_B in collisions[piece_A]:
                if piece_A.type == 'Rock' and piece_B.type == 'Scissors':
                    piece_B.set_type('Rock')
                elif piece_A.type == 'Scissors' and piece_B.type == 'Paper':
                    piece_B.set_type('Scissors')
                elif piece_A.type == 'Paper' and piece_B.type == 'Rock':
                    piece_B.set_type('Paper')

#? --------------------------------------------------

    def set_type(self, new_piece_type):
        self.type = new_piece_type
        self.image = self.get_image(new_piece_type)

#? --------------------------------------------------

    def get_image(self, piece_type):
        return {
            'Rock'    : ROCK_IMAGE,
            'Paper'   : PAPER_IMAGE,
            'Scissors': SCISSORS_IMAGE
        } [piece_type]

#! ----------------------------------------------------------------------------------------------------
   #* - Set Game Configurations:

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT   = pygame.font.Font(None, 30)

COLOR, WHITE = (64, 0, 64), (255, 255, 255)

pygame.display.set_caption('Rock - Paper - Scissors')

#! ----------------------------------------------------------------------------------------------------
   #* - Create & Distribute Pieces:

PIECE_TYPES  = ['Rock', 'Paper', 'Scissors']
PIECE_NUMBER = 15                                 # For Each Type
R = 40                                            # Each Piece Radius

ROCK_IMAGE = pygame.transform.scale(pygame.image.load(image('Rock')).convert_alpha(), (R, R))
PAPER_IMAGE = pygame.transform.scale(pygame.image.load(image('Paper')).convert_alpha(), (R, R))
SCISSORS_IMAGE = pygame.transform.scale(pygame.image.load(image('Scissors')).convert_alpha(), (R, R))

GAME_TIME = 15                                       # In Seconds
HELP = {'Apply': True, 'Number': 2, 'Duration': 4}   # Add MIN_TYPE Pieces

#! --------------------------------------------------

PIECE_GROUP, PIECE_COUNT = Piece.initialize(PIECE_TYPES, PIECE_NUMBER, WIDTH, HEIGHT)

#! ----------------------------------------------------------------------------------------------------
   #* - Set Timers:

start_time = pygame.time.get_ticks()
game_timer = pygame.time.Clock()
help_timer = start_time

#! ----------------------------------------------------------------------------------------------------
   #* - Main Loop:

RUN = True
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

#! --------------------------------------------------
   #* - Update Timers:

    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000
    remaining_time = max(0, GAME_TIME - elapsed_time)

#! --------------------------------------------------
   #* - Move Pieces:

    PIECE_GROUP.update()
    SCREEN.fill(COLOR)

#! --------------------------------------------------
   #* - Check For Help:

    if HELP['Apply']:
        if current_time - help_timer >= HELP['Duration'] * 1000:
            for _ in range(HELP['Number']):
                x = random.randint(0, WIDTH - 50)
                y = random.randint(0, HEIGHT - 50)
                piece_type = min(PIECE_COUNT, key= PIECE_COUNT.get)
                piece = Piece(piece_type, x, y)
                PIECE_GROUP.add(piece)
                PIECE_COUNT[piece_type] += 1
            # HELP['Duration'] += 1
            help_timer = current_time

#! --------------------------------------------------
   #* - Resolve Collisions & Reset Counters:

    for piece in PIECE_GROUP:
        piece.resolve(PIECE_GROUP)

    PIECE_COUNT = Piece.reset_counters(PIECE_GROUP)

#! --------------------------------------------------
    #* - Display Everything:

    PIECE_GROUP.draw(SCREEN)
    
    for i, (type, count) in enumerate(PIECE_COUNT.items()):
        displayScore = FONT.render(f'{type}: {count}', True, WHITE)
        SCREEN.blit(displayScore, (10, 10 + i * 30))

    displayTime = FONT.render(f'Time Remaining: {int(remaining_time)}', True, WHITE)
    SCREEN.blit(displayTime, (WIDTH - 200, 10))

#! --------------------------------------------------

    pygame.display.flip() # Display
    game_timer.tick(60)   # FPS

#! --------------------------------------------------
    #* - Reset || Freeze || Exit Game:

    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        start_time = help_timer = pygame.time.get_ticks()
        game_timer = pygame.time.Clock()
        PIECE_GROUP, PIECE_COUNT = Piece.initialize(PIECE_TYPES, PIECE_NUMBER, WIDTH, HEIGHT)
    if key[pygame.K_TAB]:
        pygame.time.wait(1000)
    if key[pygame.K_ESCAPE]:
        RUN = False     

#! --------------------------------------------------
    #* - End Game:

    if elapsed_time >= GAME_TIME or sum(count != 0 for count in PIECE_COUNT.values()) == 1:
        if elapsed_time >= GAME_TIME:
            winner = max(PIECE_COUNT, key=PIECE_COUNT.get)
        elif sum(count != 0 for count in PIECE_COUNT.values()) == 1:
            winner = next((type for type, count in PIECE_COUNT.items() if count != 0), None)

        winner_text = FONT.render(f'{winner} Win.', True, WHITE)
        winner_text_rect = winner_text.get_rect(center= (WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(winner_text, winner_text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        RUN = False

pygame.quit()