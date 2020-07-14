import math
import random
import os
from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, Rect, image, mask
from abc import ABC, abstractmethod

import pygame
from thefloatingdutchman.objects.bullets.bullet_data import BulletData
from thefloatingdutchman.objects.bullets.bullet_sprite import BulletSprite

from thefloatingdutchman.character.character_sprite import CharacterSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.game_settings import GREEN, RED


class EnemySprite(CharacterSprite):
    def __init__(self, enemy_data: EnemyData):
        super().__init__(enemy_data)
        self.radius = 80
        self._damage = 10
        self.mask = mask.from_surface(self.image)

    @abstractmethod
    def _set_original_image(self):
        pass

    @abstractmethod
    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        pass

    def _calc_rotation(self, player: PlayerSprite):
        self._angle = (player._data.pos - self._data.pos).angle_to(Vector2(1, 0))
        self.image = transform.rotate(self._original_image, self._angle)
        self.rect = self.image.get_rect(center=self._data.pos)
        self.rect.center = self._data.pos
