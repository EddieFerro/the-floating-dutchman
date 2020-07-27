import math
import random

from pygame import Rect, Vector2, time

from thefloatingdutchman.utility.resource_container import ResourceContainer
from thefloatingdutchman.objects.weapons.weapon import Weapon
from thefloatingdutchman.objects.weapons.bullets.bullet_sprite import BulletSprite
from thefloatingdutchman.objects.weapons.bullets.bullet_data import BulletData
from thefloatingdutchman.character.player.player_sprite import PlayerSprite


class MultiShotWeapon(Weapon):
    def __init__(self, res_container: ResourceContainer, bullet_type=BulletSprite):
        super().__init__(res_container, bullet_type)

    def fire(self, player: PlayerSprite, attack_speed: int, spread: int, rect: Rect, life_time=0) -> bool:
        """Returns true if weapon fired"""

        # Auto fire towards player at a given rate
        t = time.get_ticks()
        if (t - self._prev_shot) > attack_speed:
            self._prev_shot = t
            temp_angle = math.atan2(
                player.rect.centery - rect.centery, player.rect.centerx - rect.centerx)
            orig_temp_angle = math.degrees(temp_angle)
            temp_angle = orig_temp_angle + random.uniform(-15, 15)
            direction = Vector2(1, 0).rotate(temp_angle)
            self._bullets.add(self._bullet_type(
                self._res_container, BulletData(direction, 0, Vector2(rect.center), 25)))
            temp_angle = orig_temp_angle + random.uniform(-15, 15)
            direction = Vector2(1, 0).rotate(temp_angle)
            self._bullets.add(self._bullet_type(
                self._res_container, BulletData(direction, 0, Vector2(rect.center), 25)))

            # if(BossState.TELEPORT):
            #     temp_angle = orig_temp_angle + random.uniform(-15, 15)
            #     direction = Vector2(1, 0).rotate(temp_angle)
            #     self._bullets.add(self._bullet_type(
            #         BulletData(direction, 0, Vector2(rect.center), 25)))
            #     temp_angle = orig_temp_angle + random.uniform(-15, 15)
            #     direction = Vector2(1, 0).rotate(temp_angle)
            #     self._bullets.add(self._bullet_type(
            #         BulletData(direction, 0, Vector2(rect.center), 25)))