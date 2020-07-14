from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
import random
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
import math
import os
from pygame.sprite import Group
from pygame import Vector2, sprite, Surface, transform, Rect, image, mask

import pygame
from thefloatingdutchman.objects.bullets.bullet_data import BulletData
from thefloatingdutchman.objects.bullets.bullet_sprite import BulletSprite

from thefloatingdutchman.character.character_sprite import CharacterSprite
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_data import EnemyData
from thefloatingdutchman.game_settings import GREEN, RED


class EnemyType2(EnemySprite):

    def __init__(self, enemy_data: EnemyData):
        super().__init__(enemy_data)
        self._type2 = True

    def _set_original_image(self):
        sprite_sheet = image.load(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "Red Fighter.png")).convert_alpha()
        temp_rect = Rect((0, 0, 32, 32))
        self._original_image = pygame.Surface(temp_rect.size, pygame.SRCALPHA)
        self._original_image.blit(sprite_sheet, (0, 0), temp_rect)
        self._original_image = transform.scale(self._original_image, (int(32 * 2.5), int(32 * 2.5)))
        self._original_image = transform.rotate(self._original_image, -90)

    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        if (self._data.health <= 0):
            self.kill()
        # Check for nearby enemies, only move in certain case
        for enemy in enemies:
            if pygame.sprite.collide_circle(self, enemy) and enemy != self:
                distance = math.hypot((enemy.rect.x - self.rect.x), (enemy.rect.y - self.rect.y))
                # print(distance)
                if (distance < 400):
                    target_direction = Vector2(
                        (self.rect.x - enemy.rect.x), (self.rect.y - enemy.rect.y))
                    target_direction.scale_to_length(self._data.vel * 0.0001)
                    self.rect.x += target_direction.x
                    self.rect.y += target_direction.y

        # Type 2 enemy backs away from player
        distance = math.hypot((player.rect.x - self.rect.x), (player.rect.y - self.rect.y))
        if (distance > 300):
            self._data._stopMoving = False

        # Enemy moves toward player given that they are either type 1 or sufficiently far enough from player
        if self._data._stopMoving == False:
            target_direction = Vector2(
                - self.rect.x + player.rect.x + random.randrange(0, 30),
                - self.rect.y + player.rect.y + random.randrange(0, 30))
            target_direction.scale_to_length(self._data.vel * 0.9)

        try:
            # Update bullets
            self._bullets.update()

            # Delete enemy when it comes into contact with player
            if sprite.collide_mask(player, self) is not None:
                player.take_damage(30)
                enemies.remove(self)

            # Type 2 enemy specification
            # Auto fire towards player at a given rate
            t = pygame.time.get_ticks()
            if (t - self._prev_shot) > self._data.attack_speed:
                self._prev_shot = t
                temp_angle = math.atan2(player.rect.centery - self.rect.centery,
                                        player.rect.centerx - self.rect.centerx)
                temp_angle = math.degrees(temp_angle)
                temp_angle += random.uniform(-20, 20)
                direction = Vector2(1, 0).rotate(temp_angle)
                BulletSprite(BulletData(direction, 0, self._data.pos, 25)).add(self._bullets)

            # Stop moving towards player at a certain distance
            if pygame.sprite.collide_circle(self, player):
                self._data._stopMoving = True
                distance = math.hypot((player.rect.x - self.rect.x), (player.rect.y - self.rect.y))
                # Move back if in danger zone
                if (distance < 300):
                    target_direction = Vector2(
                        (self.rect.x - player.rect.x), (self.rect.y - player.rect.y))
                    target_direction.scale_to_length(self._data.vel * 1.01)
                    self.rect.x += target_direction.x
                    self.rect.y += target_direction.y

            # All other cases are given movement data here
            if self._data._stopMoving == False:
                self.rect.x += target_direction.x
                self.rect.y += target_direction.y

            screen_rect = screen.get_rect()

            self.rect.clamp_ip(screen_rect)

            self._data.pos = Vector2(self.rect.center)

            self._calc_rotation(player)

        except ValueError:
            return
