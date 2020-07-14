import math
import os
from pygame import image, Rect, Surface, key, Vector2, mouse, transform, sprite
import pygame

from thefloatingdutchman.game_settings import BLACK
from thefloatingdutchman.character.character_sprite import CharacterSprite
from thefloatingdutchman.character.player.player_data import PlayerData
from thefloatingdutchman.objects.bullets.bullet_data import BulletData
from thefloatingdutchman.objects.bullets.bullet_sprite import BulletSprite


class PlayerSprite(CharacterSprite):
    def __init__(self, player_data: PlayerData):
        super().__init__(player_data)
        self.radius = 200
        self._damage = 34
        self._dead = False
        self.mask = pygame.mask.from_surface(self.image)



    def _set_original_image(self):
        #sprite_sheet = image.load("pirate_ship_00000.png").convert()
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"pirate_ship_00000.png")
        sprite_sheet = image.load(path).convert_alpha()

        # exact dimension of player sprite
        temp_rect = Rect((0, 0, 549, 549))
        #self._original_image = Surface(temp_rect.size).convert()
        self._original_image = pygame.Surface(temp_rect.size, pygame.SRCALPHA)

        # sets image to a portion of spritesheet (surface)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)

        # makes player appropriate size
        self._original_image = transform.scale(
            self._original_image, (int(549/3), int(549/3)))
        self._original_image = transform.rotate(self._original_image, 90)

    # simple player movement

    def update(self, screen, placeholder):
        if(self._data.health <= 0):
            self._dead = True
            self.kill
        self._calc_movement(screen, placeholder)
        self._bullets.update()

    def _calc_movement(self, screen,placeholder):
        x = 0
        y = 0
        buttons = mouse.get_pressed()
        keys = key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x = -self._data.vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x = self._data.vel
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y = -self._data.vel
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y = self._data.vel
        if keys[pygame.K_SPACE] or buttons[0] == True:
            t = pygame.time.get_ticks()
            if (t - self._prev_shot) > self._data.attack_speed:
                self._prev_shot = t
                direction = Vector2(1,0).rotate(-self._angle)
                BulletSprite(BulletData(direction, 0, self._data.pos, 25)).add(self._bullets)


        if x != 0 and y != 0:
            x *= 0.7071
            y *= 0.7071

        self._data.pos = self._data.pos + Vector2(x, y)

        # must be called in this order, considering fixing later
        self._calc_rotation()
        self._check_walls(screen)

    def _check_walls(self, screen):
        screen_rect = screen.get_rect()

        # stops rect from moving outside screen
        self.rect.clamp_ip(screen_rect)

        # repositions player at center of rect
        self._data.pos = Vector2(self.rect.center)

    def _calc_rotation(self):
        mouse_x, mouse_y = mouse.get_pos()
        rel_x, rel_y = mouse_x - self._data.pos.x, mouse_y - self._data.pos.y
        self._angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = transform.rotate(self._original_image, int(self._angle))
        self.rect = self.image.get_rect(center=self._data.pos)
        self.rect.center = self._data.pos

    @property
    def dead(self) ->bool:
        return self._dead
