import pygame
from pygame import QUIT
import time
import os
from thefloatingdutchman.character.character_data import CharacterData
from thefloatingdutchman.game_settings import (WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, BLUE, YELLOW, WHITE, RUFOUS, MANTIS, LIME, WIDTH_LEFT_BOUND, WIDTH_RIGHT_BOUND, GAME_OVER_BOUNDS, PAUSE_BOUNDS, MAIN_MENU_BOUNDS)


class Screen:
    #create surfaces from features
    def _gather_surfaces(self, surfaces, features, width, height, font_size) -> pygame.Surface:
        for txt, color, fill in features:
            surfaces.append(self._draw_surface(width,
                                                    height, font_size, txt, color, fill))
        return surfaces

    # create surface
    def _draw_surface(self, width, height, font_size, text,
                           text_color, fill) -> pygame.Surface:

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

    # draw pre-defined surfaces onto screen

    # screen, surfaces being attached to screen, y_value of surfaces being attached, index highlights surface to be highlighted
    def draw(self, screen, index, y_locations, tutorial, sleep_times) -> pygame.Surface:
        if not tutorial:
            if len(self._surfaces) == 7: # game over screen
                screen.fill(BLACK)
            elif len(self._surfaces) == 9: # main menu screen
                screen.blit(self._background, (0,0))
                screen.blit(self._logo, ((WINDOW_WIDTH - self._logo.get_width()) / 2, WINDOW_HEIGHT*.25))
            elif len(self._surfaces) == 13: # pause screen
                pygame.draw.rect(screen, WHITE, (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 5, WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / (10 / 7)), border_radius=int(min(WINDOW_WIDTH / 2, WINDOW_HEIGHT / (3 / 2)) / 4))

        i=0
        # attach surfaces onto screen
        for surface, height in zip(self._surfaces, y_locations):
            # swap surface with highlighted one
            if not tutorial and surface == self._surfaces[index+1]:
                screen.blit(self._surfaces[1 + int(len(self._surfaces) / 2) + index], ((WINDOW_WIDTH - surface.get_width()) / 2,
                                                                                       height))
            else:  # draw non-selected surface
                screen.blit(surface, ((WINDOW_WIDTH - surface.get_width()) / 2,
                                      height))
            if sleep_times and sleep_times[i] > 0:
                pygame.display.update()
                wait_for_user(sleep_times[i], False)
            i+=1

        pygame.display.update()  # update screen
        return screen


    def _access_menu(self, screen, result, num_options, bounds) -> int: # allows player to toggle between options in given menu 
        curr_index = result # indicates option currently chosen
        prev_index = result # previous option chosen

        while True:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()  # mouse position
                if event.type == QUIT:  # user closes application
                        exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:  # event has occurred
                    # player has chosen an option
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        if curr_index >= 0 and curr_index < num_options:  # return chosen option
                            return curr_index

                    # user presses up or down on keypad
                    if (event.type == pygame.KEYDOWN and (event.key == pygame.K_DOWN or event.key == pygame.K_UP)):
                        if event.key == pygame.K_UP and curr_index > 0:
                            curr_index -= 1
                            self.draw(screen, curr_index, self._y_locations, False, None)

                        elif event.key == pygame.K_DOWN and curr_index < num_options - 1:
                            curr_index += 1
                            self.draw(screen, curr_index, self._y_locations, False, None)

                    # button may be highlighted/selected, user hovers over proper width
                    elif (WIDTH_RIGHT_BOUND >= mouse[0] >= WIDTH_LEFT_BOUND):
                        i=0
                        for lower_bound, upper_bound in bounds:
                            if upper_bound >= mouse[1] >= lower_bound:
                                if prev_index != curr_index:
                                    screen = self.draw(screen, i, self._y_locations, False, None)
                                prev_index = curr_index
                                curr_index = i
                                # player clicked on Resume button
                                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                                    return curr_index
                            i+=1


class GameOverScreen(Screen):
    def __init__(self):
        self._initialize()

    # initialize surfaces that compose the game over screen

    def _initialize(self):
        # game over text
        self._surfaces = []
        self._surfaces.append(self._draw_surface(WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / 5, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "GAME OVER!", WHITE, None))

        features = [["PLAY AGAIN", WHITE, BLACK], ["RETURN TO MAIN MENU", WHITE, BLACK], ["EXIT GAME", WHITE, BLACK],
                    ["PLAY AGAIN", WHITE, MANTIS], ["RETURN TO MAIN MENU", WHITE, RUFOUS], ["EXIT GAME", WHITE, RUFOUS]]

        self._surfaces = self._gather_surfaces(self._surfaces, features, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 10, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 20))
        self._y_locations = [WINDOW_HEIGHT*.2, WINDOW_HEIGHT*.45, WINDOW_HEIGHT*.6, WINDOW_HEIGHT*.75]

    def open(self, screen) -> int:
        return self._access_menu(screen, 0, len(GAME_OVER_BOUNDS), GAME_OVER_BOUNDS)


class PauseScreen(Screen):
    def __init__(self):
        self._initialize()

    # initialize surfaces that compose the pause screen

    def _initialize(self):
        self._surfaces = []
        self._surfaces.append(self._draw_surface(WINDOW_WIDTH / 2,
                                                WINDOW_HEIGHT / 6, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "PAUSED", BLACK, None))  # pause

        features = [["RESUME", WHITE, BLACK], ["VIEW MAP", WHITE, BLACK], ["VIEW GAME CONTROLS", WHITE, BLACK], ["RESTART GAME", WHITE, BLACK], ["RETURN TO MAIN MENU", WHITE, BLACK], ["EXIT GAME", WHITE, BLACK],
                    ["RESUME", WHITE, MANTIS], ["VIEW MAP", WHITE, MANTIS], ["VIEW GAME CONTROLS", WHITE, MANTIS], ["RESTART GAME", WHITE, MANTIS], ["RETURN TO MAIN MENU", WHITE, RUFOUS], ["EXIT GAME", WHITE, RUFOUS]]

        self._surfaces = self._gather_surfaces(self._surfaces, features, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 14, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 25))
        self._y_locations = [WINDOW_HEIGHT*.2, WINDOW_HEIGHT*.35, WINDOW_HEIGHT*.44, WINDOW_HEIGHT*.53, WINDOW_HEIGHT*.62, WINDOW_HEIGHT*.71, WINDOW_HEIGHT*.8]

    def open(self, screen, result) -> int:
        return self._access_menu(screen, result, len(PAUSE_BOUNDS), PAUSE_BOUNDS)
        

class MainMenu(Screen):
    def __init__(self):
        self._initialize()

    def _initialize(self):
        self._background = image_fill_background(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "utility/space_images/main_menu_background.jpg"))
        self._logo = pygame.image.load(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "utility/logo.png"))
        self._logo = pygame.transform.scale(
            self._logo, (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 10)))

        self._surfaces = []
        self._surfaces.append(pygame.Surface(
            (0, 0), pygame.SRCALPHA))
        
        features = [["BEGIN GAME", WHITE, None], ["BEGIN GAME WITH TUTORIAL", WHITE, None], ["VIEW GAME CONTROLS", WHITE, None], ["EXIT GAME", WHITE, None],
                    ["BEGIN GAME", WHITE, MANTIS], ["BEGIN GAME WITH TUTORIAL", WHITE, MANTIS], ["VIEW GAME CONTROLS", WHITE, MANTIS], ["EXIT GAME", WHITE, RUFOUS]]

        self._surfaces = self._gather_surfaces(self._surfaces, features, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 12, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 25))
        self._y_locations = [WINDOW_HEIGHT*.9, WINDOW_HEIGHT*.4, WINDOW_HEIGHT*.5, WINDOW_HEIGHT*.6, WINDOW_HEIGHT*.7]

    def open(self, screen, result) -> int:
        return self._access_menu(screen, result, len(MAIN_MENU_BOUNDS), MAIN_MENU_BOUNDS)


class LevelSurface(Screen):
    # initialize surface with level being equal to 1
    def __init__(self):
        self.draw_new_level(0)

    # draw new surface containing new level when level is incremented
    def draw_new_level(self, level):
        self._level_surface = self._draw_surface(
            WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 20), "LEVEL " + str(level+1), WHITE, None)

    # drawing surface to screen
    def update_screen_level(self, screen):
        screen.blit(self._level_surface, ((WINDOW_WIDTH - self._level_surface.get_width()) / 2, -WINDOW_HEIGHT/3))

class MapSurface(Screen):
    # drawing surface to screen
    def update_map(self, screen):
        self._map_surface = self._draw_surface(
            WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 20), "Press M to close Map", YELLOW, None)
        screen.blit(self._map_surface, ((WINDOW_WIDTH - self._map_surface.get_width()) / 2, WINDOW_HEIGHT/2.5))


class MapSurface2(Screen):
    # drawing surface to screen
    def update_map(self, screen):
        self._map_surface = self._draw_surface(
            WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 20), "Press M to Open the Map and Advance", YELLOW, None)
        screen.blit(self._map_surface, ((WINDOW_WIDTH - self._map_surface.get_width()) / 2, WINDOW_HEIGHT/2.5))

class TreasureSurface(Screen):


    # drawing surface to screen
    def update_treasure_screen(self, screen, txt):
        self._treasure_surface = self._draw_surface(
            WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 20), txt, YELLOW,
            None)
        screen.blit(self._treasure_surface, ((WINDOW_WIDTH - self._treasure_surface.get_width()) / 2, -WINDOW_HEIGHT/4))


class Tutorial(Screen):
    # initialize surface elements and background image
    def __init__(self):
        self._generate_story_elements()
        self._generate_game_controls_elements()
        self._background = image_fill_background(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "utility/space_images/tutorial_background.jpg"))

    # initialize elements for story
    def _generate_story_elements(self):
        self._story_surfaces = []
        self._story_surfaces.append(self._draw_surface(WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "THE FLOATING DUTCHMAN", YELLOW, None))
        features = [["You Are the Captain of the Flying Dutchman", YELLOW, None], ["You have ended up in space and your crew", YELLOW, None],
        ["has been captured by the Ghost Bustas", YELLOW, None], ["It is up to you to rescue your crew", YELLOW, None],
        ["and defeat the Ghost Bustas", YELLOW, None], ["Press any Key to Continue", BLUE, None]]
        
        self._story_surfaces = self._gather_surfaces(self._story_surfaces, features, WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15))

    # initialize elements for game controls
    def _generate_game_controls_elements(self):
        self._game_controls_surfaces = []
        self._game_controls_surfaces.append(self._draw_surface(WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 14), "GAME CONTROLS", YELLOW, None))
        self._game_controls_surfaces.append(self._draw_surface(WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15), "Press any Key to Continue", BLUE, None))
        self.game_controls_image = pygame.image.load(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "utility/game_controls.png"))
        self.game_controls_image = pygame.transform.scale(
            self.game_controls_image, (int(WINDOW_WIDTH/2), int(WINDOW_HEIGHT/2)))

    # begin tutorial
    def begin_tutorial(self, screen):
        self.show_story(screen)
        self.show_game_controls(screen)

    # print story onto screen
    def show_story(self, screen):
        y_locations = [-WINDOW_HEIGHT/3,-WINDOW_HEIGHT/5,-WINDOW_HEIGHT/(35/2),3,WINDOW_HEIGHT/7,WINDOW_HEIGHT/5,WINDOW_HEIGHT/3]
        sleep_times = [2.5,3,0,3,0,1.5,0]
        screen.blit(self._background, self._background.get_rect())
        self._surfaces = self._story_surfaces
        self.draw(screen, 0, y_locations, True, sleep_times)
        wait_for_user(float('inf'), False)

    # print game controls onto screen
    def show_game_controls(self, screen):
        y_locations = [-WINDOW_HEIGHT/3,WINDOW_HEIGHT/3]
        screen.blit(self._background, self._background.get_rect())
        screen.blit(self.game_controls_image, ((WINDOW_WIDTH-self.game_controls_image.get_width()
                                                )/2, (WINDOW_HEIGHT-self.game_controls_image.get_height())/2))
        self._surfaces = self._game_controls_surfaces
        self.draw(screen, 0, y_locations, True, None)
        wait_for_user(float('inf'), False)


class PostLevelScreen(Screen):
    def __init__(self):
        self._surfaces = []
        features = [["LEVEL " + str(1), YELLOW, None], ["COMPLETE", YELLOW, None], ["Press any Key to Continue", YELLOW, None]]
        self._surfaces = self._gather_surfaces(self._surfaces, features, WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10))

    def update_level(self, level):
        self._surfaces[0] = self._draw_surface(WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10), "LEVEL " + str(level+1), YELLOW, None)

    def appear(self, screen):
        y_locations = [-WINDOW_HEIGHT/5, -WINDOW_HEIGHT/9, WINDOW_HEIGHT/3]
        sleep_times = [0,3,0]
        self.draw(screen, 0, y_locations, True, sleep_times)
        wait_for_user(float('inf'), False)


class PreLevelScreen(Screen):
    def __init__(self):
        self._all_surfaces = []
        features = [["LEVEL BEGINS IN", YELLOW, None], ["3", YELLOW, None], ["2", YELLOW, None], ["1", YELLOW, None]]
        self._all_surfaces = self._gather_surfaces(self._all_surfaces, features, WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10))


    def appear(self, screen, index):
        self._surfaces = [self._all_surfaces[0], self._all_surfaces[index]]
        y_locations = [-WINDOW_HEIGHT/5, -WINDOW_HEIGHT/9]
        self.draw(screen, 0, y_locations, True, None)
        wait_for_user(1, True)


class GameCompletedScreen(Screen):
    def __init__(self):
        self._initialize()

    def _initialize(self):
        self._background = image_fill_background(os.path.join(os.path.dirname(os.path.realpath(__file__)), "utility/space_images/main_menu_background.jpg"))
        self._logo = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "utility/logo.png"))
        self._surfaces = []
        features = [["CONGRATULATIONS!", LIME, None]]
        self._surfaces = self._gather_surfaces(self._surfaces, features, WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 10))
        features = [["You have rescued your crew", LIME, None], ["and defeated the Ghost Bustas", LIME, None], ["Press any Key to Continue", YELLOW, None]]
        self._surfaces = self._gather_surfaces(self._surfaces, features, WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15))

    def activate(self, screen):
        y_locations = [-WINDOW_HEIGHT/5, -WINDOW_HEIGHT/12, 0, WINDOW_HEIGHT/3]
        screen.blit(self._background, self._background.get_rect())
        screen.blit(self._logo, ((WINDOW_WIDTH - self._logo.get_width()) / 2, WINDOW_HEIGHT*.1))
        self.draw(screen, 0, y_locations, True, None)
        wait_for_user(float('inf'), False)


class CreditsScreen(Screen):
    def __init__(self):
        self._initialize()

    def _initialize(self):
        self._background = image_fill_background(os.path.join(os.path.dirname(os.path.realpath(__file__)), "utility/space_images/main_menu_background.jpg"))
        self._surfaces = []
        features = [["Thanks for Playing!", YELLOW, None], ["Developed By", YELLOW, None], ["Press any Key to Continue", YELLOW, None]]
        self._surfaces = self._gather_surfaces(self._surfaces, features, WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 15))
        features = [["Eddie Ferro", YELLOW, None], ["Kayton Fletcher", YELLOW, None], ["Santosh Tirumala", YELLOW, None], ["JJ Thurber", YELLOW, None], ["Ben Berlin", YELLOW, None]]
        self._surfaces = self._gather_surfaces(self._surfaces, features, WINDOW_WIDTH, WINDOW_HEIGHT, (int)(min(WINDOW_HEIGHT, WINDOW_WIDTH) / 18))

    def activate(self, screen):
        y_locations = [-WINDOW_HEIGHT/(5/2), -WINDOW_HEIGHT/4, WINDOW_HEIGHT/3, -WINDOW_HEIGHT/9, -WINDOW_HEIGHT/18, 0, WINDOW_HEIGHT/18, WINDOW_HEIGHT/9]
        screen.blit(self._background, self._background.get_rect())
        self.draw(screen, 0, y_locations, True, None)
        wait_for_user(float('inf'), False)


# health bar that shows player's health
class HealthUI():
    def __init__(self):
        self.full_heart = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "utility/full_heart.png")).convert_alpha()
        self.heart_outline = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "utility/heart_outline.png")).convert_alpha()
        self.half_heart = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "utility/half_heart.png")).convert_alpha()

    def health_bar(self, screen, playermanager):
        current_hp = playermanager.player._data.health
        max_hp = playermanager.player._data._max_health
        whole = int(current_hp / 1)
        # image = pygame.transform.scale(image, (1.5, 1.5))
        for x in range(max_hp):
            screen.blit(self.heart_outline, (30 + 75 * x, 30))
        for i in range(whole):
            screen.blit(self.full_heart, (30 + 75 * i, 30))
        if (current_hp - whole) > 0:
            screen.blit(self.half_heart, (30 + 75 * whole, 30))

# scales image to screen size


def image_fill_background(image_name):
    image = pygame.image.load(image_name)
    image = pygame.transform.scale(image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    return image


# pauses game until either key is pressed or the time spent in function is greater than sleep_time


def wait_for_user(sleep_time, auto):
    t0 = time.time()
    while True:
        if (time.time() - t0 > sleep_time):
            return
        for event in pygame.event.get():
            if event.type == QUIT:  # user closes application
                exit()
            if (not auto and event.type == pygame.KEYDOWN):
                return
