import random
from enum import Enum

import pygame

import size_mines_field as smf
from data import sprite


# Pomocná třída enum na stav miny
class MineFieldPositionStatus(Enum):
    HIDDEN = -1
    EMPTY = -2
    CLICKED = -3
    FLAGGED_AND_WAS_MINE = -4
    FLAGGED_AND_WAS_NOT_MINE = -5
    MINE = -6


# konstanty a fce které neinteragují s pygame!
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (18, 173, 42)
YELLOW = (255, 216, 1)
RED = (202, 0, 42)
BLUE = (80, 133, 188)
GREY = (127, 127, 127)

MINE_SIZE = 30
FPS = 60
FRAMES = FPS / 1
MARGIN = 5

MAX_WIDTH = 1200
MAX_HEIGHT = 1200
MIN_WIDTH = 600
MIN_HEIGHT = 600

game_count = 0
lost_game_count = 0
win_game_count = 0


def increment_games():
    global game_count
    game_count = game_count + 1


def increment_lost_games():
    global lost_game_count
    lost_game_count = lost_game_count + 1


def increment_win_games():
    global win_game_count
    win_game_count = win_game_count + 1


WINDOW_WIDTH, WINDOW_HEIGHT, NUMBER_OF_MINES = smf.get_games_option(MAX_WIDTH, MAX_HEIGHT, MINE_SIZE + MARGIN,
                                                                    MIN_WIDTH, MIN_HEIGHT)

ROW_RANGE = WINDOW_WIDTH // (MINE_SIZE + MARGIN)
COLUMN_RANGE = WINDOW_HEIGHT // (MINE_SIZE + MARGIN)

NEAR_NEIGHBORHOOD = [
    [-1, -1],
    [-1, 0],
    [-1, 1],
    [0, -1],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1]
]


def check_surrounding(cell, matrix):
    is_surrounded = False
    for move in NEAR_NEIGHBORHOOD:
        if len(matrix) > (cell[0] + move[0]) > 0 and len(matrix[0]) > (cell[1] + move[1]) > 0:
            if matrix[cell[0] + move[0]][cell[1] + move[1]] == MineFieldPositionStatus.MINE \
                    or matrix[cell[0] + move[0]][cell[1] + move[1]] == MineFieldPositionStatus.FLAGGED_AND_WAS_MINE:
                matrix[cell[0]][cell[1]] = MineFieldPositionStatus.CLICKED
                is_surrounded = True

    if not is_surrounded and len(matrix) > (cell[0]) >= 0 and len(matrix[0]) > (cell[1]) >= 0 \
            and matrix[cell[0]][cell[1]] != MineFieldPositionStatus.EMPTY \
            and matrix[cell[0]][cell[1]] != MineFieldPositionStatus.CLICKED:

        matrix[cell[0]][cell[1]] = MineFieldPositionStatus.EMPTY

        for move in NEAR_NEIGHBORHOOD:
            if len(matrix) > (cell[0] + move[0]) >= 0 and len(matrix[0]) > (cell[1] + move[1]) >= 0:
                target = [cell[0] + move[0], cell[1] + move[1]]
                check_surrounding(target, matrix)


# fce které interagují s pygame!
def init_minefield():
    matrix = []

    for row in range(ROW_RANGE):
        matrix.append([])
        for column in range(COLUMN_RANGE):
            matrix[row].append(MineFieldPositionStatus.HIDDEN)

    actual_number = 0

    while actual_number != NUMBER_OF_MINES:

        r = random.randrange(0, ROW_RANGE - 1)
        c = random.randrange(0, COLUMN_RANGE - 1)

        if matrix[r][c] == MineFieldPositionStatus.HIDDEN:
            matrix[r][c] = MineFieldPositionStatus.MINE
            actual_number = actual_number + 1

    return matrix


def get_number_of_mines_around(minefield, row, column):
    count = 0
    for neighbor in NEAR_NEIGHBORHOOD:
        if len(minefield) > (row + neighbor[0]) >= 0 and len(minefield[0]) > (column + neighbor[1]) >= 0:
            if minefield[row + neighbor[0]][column + neighbor[1]] == MineFieldPositionStatus.MINE \
                    or minefield[row + neighbor[0]][
                column + neighbor[1]] == MineFieldPositionStatus.FLAGGED_AND_WAS_MINE:
                count = count + 1
    return count


def render_result(minefield, is_exploded):
    # procházíme celou matici a podle vnitřní hodnoty nastavujeme barvu k vykreslení
    for row in range(ROW_RANGE):
        for column in range(COLUMN_RANGE):
            color = GREY
            if minefield[row][column] == MineFieldPositionStatus.CLICKED:
                color = BLUE
            elif minefield[row][column] == MineFieldPositionStatus.EMPTY:
                color = GREEN
            elif minefield[row][column] == MineFieldPositionStatus.FLAGGED_AND_WAS_MINE \
                    or minefield[row][column] == MineFieldPositionStatus.FLAGGED_AND_WAS_NOT_MINE:
                color = YELLOW
            elif minefield[row][column] == MineFieldPositionStatus.MINE and is_exploded:
                color = RED

            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + MINE_SIZE) * column + MARGIN,
                              (MARGIN + MINE_SIZE) * row + MARGIN,
                              MINE_SIZE,
                              MINE_SIZE])

    for row in range(ROW_RANGE):
        for column in range(COLUMN_RANGE):
            if minefield[row][column] == MineFieldPositionStatus.CLICKED:
                text = font.render(str(get_number_of_mines_around(minefield, row, column)), False, BLACK)
                screen.blit(text,
                            ((MARGIN + MINE_SIZE) * column + MARGIN + 11, (MARGIN + MINE_SIZE) * row + MARGIN + 3))


# Start pygame + start modulů!
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Nastaveni okna aj.
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The Triple Jan Minesweeper :D")
font = pygame.font.SysFont('Arial', 20)


# table = load_tile_table()
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(BLACK)

        button_font = pygame.font.SysFont("None", 50)
        statistic_font = pygame.font.SysFont("None", 25)

        title = button_font.render("Triple Jan MineSweeper", True, WHITE)

        statistic = statistic_font.render(
            "game count= " + str(game_count) + ", win count = " + str(win_game_count) + ", lose count = " + str(
                lost_game_count),
            True, WHITE)

        new_game_inactive = button_font.render("NEW GAME", True, WHITE)
        new_game_active = button_font.render("NEW GAME", True, RED)

        quit_game_inactive = button_font.render("QUIT GAME", True, WHITE)
        quit_game_active = button_font.render("QUIT GAME", True, RED)

        title_text = screen.blit(title, ((WINDOW_WIDTH / 2) - 200, 200))  # title is an image

        title_statistic = screen.blit(statistic, ((WINDOW_WIDTH / 2) - 180, 250))

        title_text.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))

        title_statistic.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))

        button((WINDOW_WIDTH / 2) - 100, 300, 200, 35, new_game_active, new_game_inactive, new_game)
        button((WINDOW_WIDTH / 2) - 100, 350, 200, 35, quit_game_active, quit_game_inactive, quit_game)
        pygame.display.update()


def button(x, y, w, h, inactive, active, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        screen.blit(active, (x, y))
        if click[0] == 1 and action is not None:
            action()
    else:
        screen.blit(inactive, (x, y))


def new_game():
    increment_games()
    run_game()


def quit_game():
    quit()


# Grafika!
atomic_explosion_path = 'resources/images/atomic_bomb_explosion.png'
fireworks_path = 'resources/images/Firework.png'

# Definice spritu
# atomic explosion
sprites = [
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 0, 320, 232), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 233, 320, 232), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 465, 320, 232), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 697, 320, 232), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 929, 320, 232), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(atomic_explosion_path, (0, 1161, 320, 232), 5, 1, False, FRAMES),
    sprite.SpriteStripAnim(fireworks_path, (0, 0, 256, 256), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(fireworks_path, (0, 257, 256, 256), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(fireworks_path, (0, 513, 256, 256), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(fireworks_path, (0, 769, 256, 256), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(fireworks_path, (0, 1025, 256, 256), 5, 1, False, FRAMES) +
    sprite.SpriteStripAnim(fireworks_path, (0, 1281, 256, 256), 5, 1, False, FRAMES)
]

# hodiny - FPS CLOCK / heart rate
clock = pygame.time.Clock()

# Kolecke spritů
my_sprites = pygame.sprite.Group()


def run_game():
    # start:
    minefield = init_minefield()
    screen.fill(BLACK)
    running = True

    # nastaveni animace
    sprites[0].iter()
    sprites[1].iter()
    is_exploded = False
    is_explode_sound_playing = False
    is_firework_sound_playing = False
    is_win = False

    # velikostPole = otazkaVelikostPole.velikostPole(WINDOW_WIDTH, WINDOW_HEIGHT)
    # cyklus udrzujici okno v chodu
    while running:
        # game_menu.game_intro(screen)
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
                if mouse_position[1] >= WINDOW_WIDTH or mouse_position[0] >= WINDOW_HEIGHT:
                    continue
                row = mouse_position[1] // (MINE_SIZE + MARGIN)
                column = mouse_position[0] // (MINE_SIZE + MARGIN)

                if row >= ROW_RANGE or column >= COLUMN_RANGE:
                    continue

                if event.button == 1:
                    if minefield[row][column] == MineFieldPositionStatus.MINE:
                        is_explode_sound_playing = True
                        is_exploded = True
                        increment_lost_games()
                    elif minefield[row][column] == MineFieldPositionStatus.HIDDEN:
                        check_surrounding([row, column], minefield)
                elif event.button == 3:
                    if minefield[row][column] == MineFieldPositionStatus.MINE:
                        minefield[row][column] = MineFieldPositionStatus.FLAGGED_AND_WAS_MINE
                        is_last_deactivated = True

                        for row in range(ROW_RANGE):
                            for column in range(COLUMN_RANGE):
                                if minefield[row][column] == MineFieldPositionStatus.MINE \
                                        or minefield[row][column] == MineFieldPositionStatus.FLAGGED_AND_WAS_NOT_MINE:
                                    is_last_deactivated = False

                        if is_last_deactivated:
                            is_win = True
                            is_firework_sound_playing = True
                            increment_win_games()
                    elif minefield[row][column] == MineFieldPositionStatus.HIDDEN:
                        minefield[row][column] = MineFieldPositionStatus.FLAGGED_AND_WAS_NOT_MINE
                    elif minefield[row][column] == MineFieldPositionStatus.FLAGGED_AND_WAS_NOT_MINE:
                        minefield[row][column] = MineFieldPositionStatus.HIDDEN
                    elif minefield[row][column] == MineFieldPositionStatus.FLAGGED_AND_WAS_MINE:
                        minefield[row][column] = MineFieldPositionStatus.MINE

        # Update
        my_sprites.update()

        # Render
        my_sprites.draw(screen)
        if is_win:
            render_result(minefield, is_exploded)
            try:
                if is_firework_sound_playing:
                    pygame.mixer.music.load('resources/sounds/Fireworks.mp3')
                    pygame.mixer.music.play(0)
                    is_firework_sound_playing = False
                image2 = sprites[1].next()
                screen.blit(image2, ((WINDOW_WIDTH / 2) - 160, (WINDOW_HEIGHT / 2) - 116))
            except StopIteration:
                print("Animation stopped.")
                pygame.time.delay(1000)
                break
        if is_exploded:
            try:
                render_result(minefield, is_exploded)

                if is_explode_sound_playing:
                    pygame.mixer.music.load('resources/sounds/Explosion3.wav')
                    pygame.mixer.music.play(0)
                    is_explode_sound_playing = False
                # TODO vyhodit velikost obrazku / animace???? Nekam do konstant
                image = sprites[0].next()
                screen.blit(image, ((WINDOW_WIDTH / 2) - 124, (WINDOW_HEIGHT / 2) - 124))
            except StopIteration:
                print("Animation stopped.")
                pygame.time.delay(1000)
                break
        if not (is_exploded or is_win):
            render_result(minefield, is_exploded)
        pygame.display.flip()
        pygame.display.update()


game_intro()
pygame.quit()
