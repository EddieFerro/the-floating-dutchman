import math

from pygame.sprite import Group
from pygame import Vector2, sprite, Surface

import pygame
from objects.bullets.bullet_data import BulletData
from objects.bullets.bullet_sprite import BulletSprite

from character.character_sprite import CharacterSprite
from character.player.player_sprite import PlayerSprite
from character.enemy.enemy_data import EnemyData
from game_settings import GREEN


class EnemySprite(CharacterSprite):
    def __init__(self, enemy_data: EnemyData):
        super().__init__(enemy_data)
        self.radius = 50
        self._damage = 10

    def _set_original_image(self):
        self._original_image = Surface((20, 50))
        self._original_image.fill(GREEN)

    # Enemy AI might go in here
    def update(self, player: PlayerSprite, enemies: Group, screen: Surface):
        # Check for nearby enemies, only move in certain case
        if(self._data.health <= 0):
            self.kill()
        for enemy in enemies:
            if pygame.sprite.collide_circle(self, enemy) and enemy != self:
                distance = math.hypot((enemy.rect.x - self.rect.x), (enemy.rect.y - self.rect.y))
                # print(distance)
                if (distance < 400):
                    target_direction = Vector2(
                        (self.rect.x - enemy.rect.x), (self.rect.y - enemy.rect.y))
                    target_direction.scale_to_length(self._data.vel * 1.01)
                    self.rect.x += target_direction.x
                    self.rect.y += target_direction.y

        # Type 2 enemy backs away from player
        distance = math.hypot((player.rect.x - self.rect.x), (player.rect.y - self.rect.y))
        if (distance > 300 and self._data._type2):
            self._data._stopMoving = False

        # Enemy moves toward player given that they are either type 1 or sufficiently far enough from player
        if self._data._stopMoving == False:
            target_direction = Vector2(
                - self.rect.x + player.rect.x, - self.rect.y + player.rect.y)
            target_direction.scale_to_length(self._data.vel)

        try:
            # Update bullets
            self._bullets.update()

            # Delete enemy when it comes into contact with player
            if self.rect.colliderect(player.rect):
                enemies.remove(self)

            # Tyoe 2 enemy specification
            if self._data._type2:
                # Auto fire towards player at a given rate
                t = pygame.time.get_ticks()
                if (t - self._prev_shot) > 1000:
                    self._prev_shot = t
                    self._angle = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
                    self._angle = math.degrees(self._angle)
                    direction = Vector2(1, 0).rotate(self._angle)
                    BulletSprite(BulletData(direction, 0, Vector2(self.rect.x, self.rect.y), 25)).add(self._bullets)

            # Stop moving towards player at a certain distance
                if pygame.sprite.collide_circle(self, player):
                    self._data._stopMoving = True
                    distance = math.hypot((player.rect.x-self.rect.x),(player.rect.y - self.rect.y))
                    # Move back if in danger zone
                    if(distance < 300):
                        target_direction = Vector2(
                            (self.rect.x - player.rect.x), (self.rect.y -player.rect.y))
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

        except ValueError:
            return
        
