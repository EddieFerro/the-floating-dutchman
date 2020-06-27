from pygame import display, event, time, K_n, QUIT, KEYDOWN, K_TAB

from character.player.player_manager import PlayerManager
from manager import Manager
from game_settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from level.room.room_manager import RoomManager
from user_interface.map_ui import MapUI
import ui


class GameManager(Manager):
    def __init__(self):
        super().__init__()
        self._screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._game_over_screen = ui.initialize_game_over_screen()  # game over screen
        self._pause_screen = ui.initialize_pause_screen()
        self._map = MapUI()
        self._done = False
        self._level = 0
        self._background = ui.image_fill_background("space_images/space8.jpg")

        # can go ahead and construct managers
        # since their spawn function controls their state
        self._player_manager = PlayerManager()
        self._room_manager = RoomManager()

    def run(self):
        self.spawn()
        # comment out this line to remove the tutorial
        ui.tutorial(self._screen)

        while not self._done:
            time.Clock().tick(FPS)  # setting fps not sure if it works tho
            for e in event.get():
                if e.type == QUIT:  # user closes application
                    # will eventually be moved
                    self._done = True  # game over

                elif e.type == KEYDOWN and e.key == K_TAB:
                    # will eventually be moved
                    self._done = ui.screen_options(ui.draw_pause_screen(
                        self._screen, self._pause_screen), "RESUME")  # pause
                elif e.type == KEYDOWN and e.key == K_n:
                    self._map.render(self._screen,
                                     self._room_manager.rooms,
                                     self._room_manager.get_available_rooms(),
                                     self._room_manager.current_room_id,
                                     self._room_manager.set_current_room)

            self.update()
            self.draw()

            # if len(self._room._enemy_manager._enemies) == 0:  # enemies gone
            #     self._done = ui.screen_options(ui.draw_game_over_screen(
            #         self._screen, self._game_over_screen), "PLAY AGAIN")  # game over
            #     if self._done is False:
            #         self.spawn()

    # resets game

    def spawn(self):
        self._level = 0
        self._player_manager.spawn()
        self._room_manager.spawn(self._level)
        self._map.spawn(self._room_manager)

    def update(self):
        self._player_manager.update(self._screen)
        self._room_manager.update(self._player_manager.player)

    def draw(self):
        # self._screen.fill(BLACK)
        self._screen.blit(self._background, self._background.get_rect())
        self._player_manager.draw(self._screen)
        self._room_manager.draw(self._screen)
        display.flip()
