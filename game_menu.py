# MENU pro hru
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(BLACK)

        myfont = pygame.font.SysFont("None", 50)

        nadpis = myfont.render("Triple Jan MineSweeper", True, WHITE)

        new_game_inactive = myfont.render("QUIT GAME", True, WHITE)
        new_game_active = myfont.render("QUIT GAME", True, RED)

        quit_game_inactive = myfont.render("QUIT GAME", True, WHITE)
        quit_game_active = myfont.render("QUIT GAME", True, RED)

        titleText = screen.blit(nadpis, (170, 200))  # title is an image

        titleText.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))

        # button(x, y, w, h, inactive, active, action=None)
        button(100, 350, 195, 80, new_game_active, new_game_inactive, new_game)
        button(300, 350, 195, 80, quit_game_active, quit_game_inactive, quit_game)
        pygame.display.update()
    # clock.tick(15)


def button(x, y, w, h, inactive, active, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        screen.blit(active, (x, y))
        if click[0] == 1 and action is not None:
            action()
    else:
        screen.blit(inactive, (x, y))


def quit_game():
    quit()