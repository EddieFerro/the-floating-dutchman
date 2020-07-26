import random

from pygame import Vector2, sprite, Surface
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.manager import Manager
from thefloatingdutchman.character.character_sprite import CharacterSprite
#Import all necessary sprite/data file for each new drop
from .hearts.heart_data import HeartData
from .hearts.heart_sprite import HeartSprite


class DropManager(Manager):
    def __init__(self):
        super().__init__()
        self._hearts = sprite.Group()
    # Initialize all new drop sprite groups
    def spawn(self, level: int):
        self._hearts = sprite.Group()
        self._need_health = False

    #Call all update functions for dropped item (collision detection, etc)
    def update(self, player: PlayerSprite, screen: Surface):
        self._heart_update(player, screen)

    # Add drop functions for new items to the drop method
    def drop_items(self, level: int):
        if self._need_health:
            self._drop_hearts(level)

    #Add drop groups to be counted in total drop count
    def dropped_count(self):
        return len(self._hearts.sprites())

    # ***** HEARTS *****
    def _drop_hearts(self, level: int):
        self._hearts = sprite.Group()
        drop1Chance = 5
        drop2Chance = 1 + (level * 0.1)
        dropChooser = random.choices([1, 2], weights=[
            drop1Chance, drop2Chance], k=1)[0]
        if dropChooser == 1:
            rand_pos_x: int = random.randint(40, WINDOW_WIDTH / 2 - 200) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_WIDTH / 2 + 200, WINDOW_WIDTH - 40)
            rand_pos_y: int = random.randint(40, WINDOW_HEIGHT / 2 - 100) if bool(
                random.randint(0, 1)) else random.randint(WINDOW_HEIGHT / 2 + 100, WINDOW_HEIGHT - 40)
            self._hearts.add(
                HeartSprite(
                    HeartData(
                        1500,
                        Vector2(rand_pos_x, rand_pos_y),
                        0,
                    )
                )
            )
        elif dropChooser == 2:
            for i in range(2):
                rand_pos_x: int = random.randint(40, WINDOW_WIDTH / 2 - 200) if bool(
                    random.randint(0, 1)) else random.randint(WINDOW_WIDTH / 2 + 200, WINDOW_WIDTH - 60)
                rand_pos_y: int = random.randint(40, WINDOW_HEIGHT / 2 - 100) if bool(
                    random.randint(0, 1)) else random.randint(WINDOW_HEIGHT / 2 + 100, WINDOW_HEIGHT - 60)
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
        if player._data.health < player._data._max_health:
            self._need_health = True
            hits = sprite.spritecollide(player, self._hearts, True, sprite.collide_mask)
            for pickups in hits:
                player._data.gain_health(1)
        else:
            self._need_health = False

    def _get_heart_count(self) -> int:
        return len(self._hearts.sprites())

    def draw(self, screen: Surface):
        self._hearts.draw(screen)
    # ***** END HEARTS *****
