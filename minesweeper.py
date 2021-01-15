import pygame, sys, random
from enum import Enum


# Pomocná třída enum
class MineEvent(Enum):
    HIDDEN = 0
    CLICKED = 1
    FLAGGED = 2


# konstanty a fce které neinteragují s pygame!
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WINDOW_WIDTH = 610
WINDOW_HEIGHT = 610

MINE_SIZE = 30
FPS = 45
MARGIN = 5


# fce které interagují s pygame!
def init_minefield():
    matrix = []
    for row in range(WINDOW_WIDTH // (MINE_SIZE + MARGIN)):
        matrix.append([])
        for column in range(WINDOW_HEIGHT // (MINE_SIZE + MARGIN)):
            matrix[row].append(MineEvent.HIDDEN)
    # pomocí fce random obarvíme odkryjeme jedno náhodné políčko ve hře jako výchozí bod
    matrix[random.randrange(0, WINDOW_WIDTH // (MINE_SIZE + MARGIN))][random.randrange(0, WINDOW_HEIGHT // (MINE_SIZE + MARGIN))] = MineEvent.CLICKED

    return matrix


def render_result():
    # procházíme celou matici a podle vnitřní hodnoty nastavujeme barvu k vykreslení
    for row in range(WINDOW_WIDTH // (MINE_SIZE + MARGIN)):
        for column in range(WINDOW_HEIGHT // (MINE_SIZE + MARGIN)):
            color = WHITE
            if minefield[row][column] == MineEvent.CLICKED:
                color = RED
            elif minefield[row][column] == MineEvent.FLAGGED:
                color = GREEN
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
                # Nastavím hodnotu, že bylo na pozici kliknuto
                minefield[row][column] = MineEvent.CLICKED
            elif event.button == 3:
                minefield[row][column] = MineEvent.FLAGGED



    # Update
    # my_sprites.update()

    # Render
    screen.fill(BLACK)

    render_result()

    # my_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
