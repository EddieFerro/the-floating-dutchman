import random
from pygame.locals import *
import math
from pygame import Vector2, sprite, Surface, event, display
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.character.character_sprite import CharacterSprite
#Import all necessary sprite/data file for each new drop
from .hearts.heart_data import HeartData
from .hearts.heart_sprite import HeartSprite
import thefloatingdutchman.ui as ui


class TreasureManager(Manager):
    def __init__(self):
        super().__init__()
        self._hearts = sprite.Group()
        self._treasure = ui.TreasureSurface()
        self._proximity = False
    # Initialize all new drop sprite groups
    def spawn(self, level: int):
        self._hearts = sprite.Group()
        self.drop_items()

    #Call all update functions for dropped item (collision detection, etc)
    def update(self, player: PlayerSprite, screen: Surface):
        self._heart_update(player, screen)

    # Add drop functions for new items to the drop method
    def drop_items(self):
        self._drop_hearts()

    #Add drop groups to be counted in total drop count
    def dropped_count(self):
        return len(self._hearts.sprites())

    # ***** HEARTS *****
    def _drop_hearts(self):
        self._hearts = sprite.Group()

        rand_pos_x: int = random.randint(40, WINDOW_WIDTH / 2 - 200) if bool(random.randint(0, 1)) else random.randint(WINDOW_WIDTH / 2 + 200, WINDOW_WIDTH - 40)
        rand_pos_y: int = random.randint(40, WINDOW_HEIGHT / 2 - 100) if bool(random.randint(0, 1)) else random.randint(WINDOW_HEIGHT / 2 + 100, WINDOW_HEIGHT - 40)
        self._hearts.add(
            HeartSprite(
                HeartData(
                    1500,
                    Vector2(rand_pos_x, rand_pos_y),
                    0,
                )
            )
        )



    def _heart_update(self, player: PlayerSprite, screen: Surface):
        self._hearts.update()
        for heart in self._hearts:
            distance = math.hypot(
                (player.rect.x - heart.rect.x), (player.rect.y - heart.rect.y))
            # print(distance)
            if (distance < 300):
                self._proximity = True
            else:
                self._proximity=False




    def _get_heart_count(self) -> int:

        return len(self._hearts.sprites())

    def _get_proximity(self) -> bool:
        return self._proximity

    def draw(self, screen: Surface):
        self._hearts.draw(screen)
        if(self._proximity):
            self._treasure.update_treasure_screen(screen)

    # ***** END HEARTS *****
