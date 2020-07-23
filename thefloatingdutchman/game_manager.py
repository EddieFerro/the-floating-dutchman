import os
import sys
from pygame import display, event, time, K_m, QUIT, KEYDOWN, K_TAB, image, transform

from thefloatingdutchman.character.player.player_manager import PlayerManager
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from thefloatingdutchman.level.room.room_manager import RoomManager
import thefloatingdutchman.ui as ui


class GameManager(Manager):
    def __init__(self):
        super().__init__()
        self._screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._main_menu = ui.MainMenu()
        self._game_over_screen = ui.GameOverScreen()  # game over screen
        self._pause_screen = ui.PauseScreen()
        self._done = False
        self._level = 0
        path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "space_images/level_1_background.jpg")
        self._background = ui.image_fill_background(path)
        self._tutorial = ui.Tutorial()
        self._post_level_screen = ui.PostLevelScreen()
        self._pre_level_screen = ui.PreLevelScreen()
        # can go ahead and construct managers
        # since their spawn function controls their state
        self._player_manager = PlayerManager()
        self._room_manager = RoomManager()

    def run(self, run_tutorial):
        # comment out this line to remove the tutorial
        if run_tutorial == 1:
            self._tutorial.begin_tutorial(self._screen)

        self.spawn()
        while not self._done:
            time.Clock().tick(FPS)  # setting fps not sure if it works tho
            for e in event.get():
                if e.type == QUIT:  # user closes application
                    #self._done = True  # game over
                    exit()
                elif e.type == KEYDOWN and e.key == K_TAB:
                    # will eventually be moved
                    self._access_pause_screen()
            self.update()
            self.draw(True)

    # resets game
    def spawn(self):
        self._level = 0
        self._done = False
        self._level_surface = ui.LevelSurface()
        self._health_ui = ui.HealthUI()
        self._player_manager.spawn()
        self._room_manager.spawn(self._level)
        self._post_level_screen.update_level(self._level)
        self._load_pre_level_screen()

    def update(self):
        self._room_manager.update(self._player_manager.player, self._screen)
        self._player_manager.update(self._screen, self._room_manager.get_current_enemies())
        self._health_ui.health_bar(self._screen, self._player_manager)

        if self._room_manager.is_level_cleared():
            self.draw(False)
            self._post_level_screen.appear(self._screen)
            self._level += 1
            self._level_surface.draw_new_level(self._level)
            self._room_manager.spawn(self._level)
            self._post_level_screen.update_level(self._level)
            self._load_pre_level_screen()

        if self._player_manager.player.dead:
            self._access_game_over_screen()

        if self._room_manager.is_room_cleared():  # enemies gone

            # must check if player died to last enemy exploding
            if self._player_manager.player.dead:
                self._access_game_over_screen()
            else:
                self._done = self._room_manager.render_map(self._screen)
                self._player_manager.player._data.pos.update(
                    WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
            time.wait(200)

    def draw(self, show_level):
        self._screen.blit(self._background, self._background.get_rect())
        self._player_manager.draw(self._screen)
        self._health_ui.health_bar(self._screen, self._player_manager)
        if show_level:
            self._level_surface.update_screen_level(self._screen)
        self._room_manager.draw(self._screen)
        display.flip()
        display.update()

    def _access_game_over_screen(self):
        result = self._game_over_screen.open(self._game_over_screen.draw(self._screen, 0, self._game_over_screen._y_locations, False, None))
        if result == 0: #play again
            self.spawn()
        if result == 1: #return to main menu
            self._done = True

    def _access_pause_screen(self):
        result = 0
        while True:
            result = self._pause_screen.open(self._pause_screen.draw(self._screen, result, self._pause_screen._y_locations, False, None), result)
            if result == 0: #resume game
                break
            elif result == 1: #show map
                self._done = self._room_manager.render_map(self._screen)
            elif result == 2: #show game controls
                self._tutorial.show_game_controls(self._screen)
            elif result == 3: #restart game
                self.spawn()
                self._load_pre_level_screen()
                break
            elif result == 4: #end game
                self._done = True
                break
            else: #exit application
                exit()
            self.draw(True)

    def _load_pre_level_screen(self):
        for i in range (1,4):
            self.draw(False)
            self._pre_level_screen.appear(self._screen, i)
