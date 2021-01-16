import random
from enum import Enum
from tkinter import *
from tkinter import messagebox

import pygame

import sprite


# Pomocná třída enum na stav miny
class MineFieldPositionStatus(Enum):
    HIDDEN = 0
    CLICKED = 1
    FLAGGED = 2
    MINE = 3
    BOOM = 4


# konstanty a fce které neinteragují s pygame!
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (18, 173, 42)
RED = (202, 0, 42)
BLUE = (80, 133, 188)

WINDOW_WIDTH = 610
WINDOW_HEIGHT = 610

MINE_SIZE = 30
FPS = 45
FRAMES = FPS / 10
MARGIN = 5
NUMBER_OF_MINES = 20


# fce které interagují s pygame!
def init_minefield():
    matrix = []
    row_range = WINDOW_WIDTH // (MINE_SIZE + MARGIN)
    column_range = WINDOW_HEIGHT // (MINE_SIZE + MARGIN)

    for row in range(row_range):
        matrix.append([])
        for column in range(column_range):
            matrix[row].append(MineFieldPositionStatus.HIDDEN)
    # pomocí fce random obarvíme odkryjeme jedno náhodné políčko ve hře jako výchozí bod
    matrix[random.randrange(0, row_range)][
        random.randrange(0, column_range)] = MineFieldPositionStatus.CLICKED

    actual_number = 0

    while actual_number != NUMBER_OF_MINES:

        r = random.randrange(0, row_range)
        c = random.randrange(0, column_range)

        if matrix[r][c] == MineFieldPositionStatus.HIDDEN:
            matrix[r][c] = MineFieldPositionStatus.MINE
            actual_number = actual_number + 1

    return matrix


def render_result():
    # procházíme celou matici a podle vnitřní hodnoty nastavujeme barvu k vykreslení
    for row in range(WINDOW_WIDTH // (MINE_SIZE + MARGIN)):
        for column in range(WINDOW_HEIGHT // (MINE_SIZE + MARGIN)):
            color = WHITE
            if minefield[row][column] == MineFieldPositionStatus.CLICKED:
                color = BLUE
            elif minefield[row][column] == MineFieldPositionStatus.FLAGGED:
                color = GREEN
            elif minefield[row][column] == MineFieldPositionStatus.BOOM:
                color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + MINE_SIZE) * column + MARGIN,
                              (MARGIN + MINE_SIZE) * row + MARGIN,
                              MINE_SIZE,
                              MINE_SIZE])


minefield = init_minefield()

# Start pygame + start modulů!
pygame.init()
pygame.mixer.init()

# Nastaveni okna aj.
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Triple Jan Minesweeper :D")
# table = load_tile_table()

# Grafika!
atomic_explosion_path = 'resources/images/atomic_bomb_explosion.png'

# Definice spritu
# atomic explosion
sprites = [
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 0, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (321, 0, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (641, 0, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (961, 0, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (1281, 0, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 233, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (321, 233, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (641, 233, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (961, 233, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (1281, 233, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 465, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (321, 465, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (641, 465, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (961, 465, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (1281, 465, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 697, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (321, 697, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (641, 697, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (961, 697, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (1281, 697, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 929, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (321, 929, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (641, 929, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (961, 929, 320, 232), 1, 1, True, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (1281, 929, 320, 232), 1, 1, True, FRAMES)
]

# hodiny - FPS CLOCK / heart rate
clock = pygame.time.Clock()

# Kolecke spritů
my_sprites = pygame.sprite.Group()

# start:
running = True

# nastaveni animace
sprites[0].iter()
image = sprites[0].next()
exploded = False
# cyklus udrzujici okno v chodu
while running:
    # FPS kontrola / jeslti bezi dle rychlosti!
    clock.tick(FPS)

    # Event
    for event in pygame.event.get():
        # print(event) - pokud potrebujete info co se zmacklo.
        if event.type == pygame.QUIT:
            running = False
            break
            # kontrola zda byla stisknuta klávesa
        elif event.type == pygame.KEYDOWN:
            # pokud byl stisknut ESC opustíme hru
            if event.key == pygame.K_ESCAPE:
                running = False
                break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # sebereme pozici myši po kliku
            mouse_position = pygame.mouse.get_pos()
            # přepočteme na souřadnice našeho pole
            row = mouse_position[1] // (MINE_SIZE + MARGIN)
            column = mouse_position[0] // (MINE_SIZE + MARGIN)
            print("Position Clicked: {} Our array coordinates: row - {}, column - {} Button: {}".format(mouse_position, row, column, event.button))
            if event.button == 1:
                if minefield[row][column] == MineFieldPositionStatus.MINE:
                    minefield[row][column] = MineFieldPositionStatus.BOOM
                    Tk().wm_withdraw()  # to hide the main window
                    messagebox.showinfo("Thats pity pal", "Booooooooooooooooooooooom!!!!")
                else:
                    minefield[row][column] = MineFieldPositionStatus.CLICKED
            elif event.button == 3:
                minefield[row][column] = MineFieldPositionStatus.FLAGGED

    # Update
    # my_sprites.update()
    my_sprites.update()

    # Render
    # screen.fill(BLACK)
    # TODO vyhodit velikost obrazku / animace???? Nekam do konstant
    my_sprites.draw(screen)
    if exploded:
        image = sprites[0].next()
        screen.blit(image, ((WINDOW_WIDTH / 2) - 160, (WINDOW_HEIGHT / 2) - 116))
    if not exploded:
        render_result()
    pygame.display.flip()
    pygame.display.update()

    # my_sprites.draw(screen)

pygame.quit()
