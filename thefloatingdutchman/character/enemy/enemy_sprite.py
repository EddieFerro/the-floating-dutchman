from abc import ABC, abstractmethod

from pygame.sprite import Group
from pygame import Vector2, Surface, transform, mask

from thefloatingdutchman.character.character_sprite import CharacterSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData


class EnemySprite(CharacterSprite, ABC):
    def __init__(self, enemy_data: EnemyData):
        super().__init__(enemy_data)
        self.radius = 80
        self._damage = 0.5
        self.mask = mask.from_surface(self.image)

    @abstractmethod
    def _set_original_image(self):
        pass

    @abstractmethod
    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        pass

    def _calc_rotation(self, player: PlayerSprite):
        self._angle = (player._data.pos -
                       self._data.pos).angle_to(Vector2(1, 0))
        self.image = transform.rotate(self._original_image, self._angle)
        self.rect = self.image.get_rect(center=self._data.pos)
        self.rect.center = self._data.pos
