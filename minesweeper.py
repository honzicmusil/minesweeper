import pygame, sys, random
from enum import Enum
from tkinter import *
from tkinter import messagebox


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
    matrix[random.randrange(0, row_range)][random.randrange(0, column_range)] = MineFieldPositionStatus.CLICKED

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

# Grafika!


# Definice spritu


# Nastaveni okna aj.
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Triple Jan Minesweeper :D")
# table = load_tile_table()

# hodiny - FPS CLOCK / heart rate
clock = pygame.time.Clock()

# Kolecke spritů
# my_sprites = pygame.sprite.Group()


# start:
running = True

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

    # Render
    screen.fill(BLACK)

    render_result()

    # my_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
