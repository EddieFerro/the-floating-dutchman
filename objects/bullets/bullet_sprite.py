import pygame
from pygame import image, Rect, Surface, key, Vector2, transform
from objects.object_sprite import ObjectSprite
from objects.bullets.bullet_data import BulletData

class BulletSprite(ObjectSprite):
    def __init__(self, bullet_data: BulletData):
        super().__init__(bullet_data)
    
    def _set_original_image(self):
        sprite_sheet = image.load("Cannonball.png").convert()

        # exact dimension of player sprite
        temp_rect = Rect((0, 0, 18, 18))
        self._original_image = Surface(temp_rect.size).convert()

        # sets image to a portion of spritesheet (surface)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)

        # makes player appropriate size
        # self._original_image = transform.scale(self._original_image, (int(313/4), int(207/4)))
    
    def update(self):
        self._data.pos += (self._data.direction * self._data.vel)
        self.rect.center = self._data.pos