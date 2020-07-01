
import pygame
import time
from character.character_data import CharacterData
from game_settings import (WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, BLUE, YELLOW, WHITE, RED, GREEN, WIDTH_LEFT_BOUND, WIDTH_RIGHT_BOUND, CONTINUE_HEIGHT_LOWER_BOUND, CONTINUE_HEIGHT_UPPER_BOUND,
                           QUIT_HEIGHT_LOWER_BOUND, QUIT_HEIGHT_UPPER_BOUND)


# create surface


def new_screen_helper(width, height, font_size, text,
                      text_color, fill):

    # inserts surface onto screen
    surface = pygame.Surface(
        (width, height), pygame.SRCALPHA)  # create surface
    if fill:  # fill surface with color
        surface.fill(fill)

    font = pygame.font.SysFont('Comic Sans MS', font_size)  # font
    text = font.render(text, True, text_color)  # create text

    # center text onto surface
    surface.blit(text, ((surface.get_rect().width - text.get_width()) / 2,
                        (surface.get_rect().height - text.get_height()) / 2))

    return surface


# initialize surfaces that compose the game over screen


def initialize_game_over_screen():
    # game over text
    surfaces = []
    surfaces.append(new_screen_helper(WINDOW_WIDTH / 2,
                                      WINDOW_HEIGHT / 5, 100, "GAME OVER!", WHITE, None))

    # play again button
    surfaces.append(new_screen_helper(WINDOW_WIDTH / 4,
                                      WINDOW_HEIGHT / 10, 50, "PLAY AGAIN", WHITE, GREEN))

    # quit button
    surfaces.append(new_screen_helper(WINDOW_WIDTH / 4,
                                      WINDOW_HEIGHT / 10, 50, "QUIT", WHITE, BLACK))

    return surfaces


# initialize surfaces that compose the pause screen


def initialize_pause_screen():
    surfaces = []
    surfaces.append(new_screen_helper(WINDOW_WIDTH / 2,
                                      WINDOW_HEIGHT / 5, 100, "PAUSED", BLACK, None))  # pause
    surfaces.append(new_screen_helper(
        WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, 50, "RESUME", WHITE, GREEN))  # play again
    surfaces.append(new_screen_helper(WINDOW_WIDTH / 4,
                                      WINDOW_HEIGHT / 10, 50, "QUIT", WHITE, BLACK))  # quit

    return surfaces


# draw pre-defined surfaces onto screen


def draw_screens(screen, surfaces, three_elems):
    resize_heights = [4, 2, 3/2]
    if not three_elems:  # when only two surfaces are being attached
        resize_heights.pop(0)
    # attach surfaces onto screen
    for surface, height in zip(surfaces, resize_heights):
        screen.blit(surface, ((WINDOW_WIDTH - surface.get_width()) / 2,
                              (WINDOW_HEIGHT - surface.get_height()) / height))
    pygame.display.update()  # update screen
    return screen

# fill screen and return screen with surfaces drawn onto it


def draw_game_over_screen(screen, surfaces):
    screen.fill(BLACK)
    return draw_screens(screen, surfaces, True)


# fill screen and return screen with surfaces drawn onto it


def draw_pause_screen(screen, surfaces):
    pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 6, WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)),
                     border_radius=int(min(WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)) / 4))
    return draw_screens(screen, surfaces, True)

# fill screen and return screen with surfaces drawn onto it


def update_screen_options(screen, text, color1, color2):
    surfaces = []
    surfaces.append(new_screen_helper(WINDOW_WIDTH / 4,
                                      WINDOW_HEIGHT / 10, 50, text, WHITE, color1))  # play again
    surfaces.append(new_screen_helper(WINDOW_WIDTH / 4,
                                      WINDOW_HEIGHT / 10, 50, "QUIT", WHITE, color2))  # quit
    return draw_screens(screen, surfaces, False)


def screen_options(screen, text):
    # used to determine whether the user just changed options
    most_recent_is_continue = True

    while True:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()  # mouse position
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:  # event has occurred

                # player has chosen an option
                # (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if most_recent_is_continue:  # either end program or continue it
                        return False
                    else:
                        return True

                # button may be highlighted/selected, user hovers over proper width
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_UP)) or (WIDTH_RIGHT_BOUND >= mouse[0] >= WIDTH_LEFT_BOUND):

                    # user hovers over Play Again button
                    if CONTINUE_HEIGHT_UPPER_BOUND >= mouse[1] >= CONTINUE_HEIGHT_LOWER_BOUND or (event.type == pygame.KEYDOWN and event.key == pygame.K_UP):
                        if not most_recent_is_continue:  # user selects Play Again/Resume after selecting Quit
                            screen = update_screen_options(
                                screen, text, GREEN, BLACK)
                        most_recent_is_continue = True
                        # player clicked on Continue button
                        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                            return False

                    # user hovers over quit button
                    # user hovers over Quit Button
                    elif QUIT_HEIGHT_UPPER_BOUND >= mouse[1] >= QUIT_HEIGHT_LOWER_BOUND or (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN):
                        if most_recent_is_continue:  # user selects Quit after selecting Play Again/Resume
                            screen = update_screen_options(
                                screen, text, BLACK, RED)
                        most_recent_is_continue = False
                        # player clicked on Quit button
                        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                            return True


def image_fill_background(image_name):
    image = pygame.image.load(image_name)
    image = pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    return image


def wait_for_user(sleep_time):
    t0 = time.time()
    while True:
        if (time.time() - t0 > sleep_time):
            return
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE)):
                return

def health_bar(screen, playermanager):
    current_hp = playermanager.player._data.health
    temp1 = pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH/2 - 150, 97.5, 300, 50))
    temp2 = pygame.draw.rect(screen, GREEN, (WINDOW_WIDTH/2 - 140, 100, 280 * (current_hp/100), 45))

def level(screen, level):
    surface = new_screen_helper(
        WINDOW_WIDTH, WINDOW_HEIGHT, 100, "LEVEL "+str(level), WHITE, None)
    screen.blit(surface, ((WINDOW_WIDTH - surface.get_width()) / 2,
                          -WINDOW_HEIGHT/3))

def spawn_tutorial(screen, text):
    for txt, height, sleep_time, color, text_size in text:
        surface = new_screen_helper(
            WINDOW_WIDTH, WINDOW_HEIGHT, text_size, txt, color, None)
        screen.blit(surface, ((WINDOW_WIDTH - surface.get_width()) / 2,
                              height))
        if sleep_time > 0:
            pygame.display.update()
            wait_for_user(sleep_time)
    pygame.display.update()
    wait_for_user(float('inf'))


def tutorial(screen):
    image = image_fill_background("space_images/space14.png")
    screen.blit(image, image.get_rect())
    text1 = [("THE FLOATING DUTCHMAN", -WINDOW_HEIGHT/3, 2.5, YELLOW, 100),
             ("You Are the Captain of the Flying Dutchman", -
              WINDOW_HEIGHT/5, 3, YELLOW, 60),
             ("You have ended up in space and your crew", -
              WINDOW_HEIGHT/(35/2), 0, YELLOW, 60),
             ("has been captured by the Ghost Bustas", 3, 3, YELLOW, 60),
             ("It is up to you to rescue your crew",
              WINDOW_HEIGHT/7, 0, YELLOW, 60),
             ("and defeat the Ghost Bustas", WINDOW_HEIGHT/5, 1.5, YELLOW, 60),
             ("Press the Spacebar to Continue", WINDOW_HEIGHT/3, 0, BLUE, 60)]
    text2 = [("Read Carefully For the Sake of Your Crew", -WINDOW_HEIGHT/4, 2.5, YELLOW, 70),
             ("Use the Arrow Pad or WASD Keys to Move",
              -WINDOW_HEIGHT/12, 0, YELLOW, 60),
             ("Use the Spacebar or the Left Mouse Button to Fire", 0, 0, YELLOW, 60),
             ("Use the Mouse to Aim at Your Target",
              WINDOW_HEIGHT/12, 0, YELLOW, 60),
             ("Press M to Open the Map",
              WINDOW_HEIGHT/6, 0, YELLOW, 60),
             ("Press Tab to Pause",
              WINDOW_HEIGHT / 4, 0, YELLOW, 60),
             ("Press the Spacebar to Begin",
               WINDOW_HEIGHT/3, 0, BLUE, 60)]
    spawn_tutorial(screen, text1)
    screen.blit(image, image.get_rect())
    spawn_tutorial(screen, text2)
