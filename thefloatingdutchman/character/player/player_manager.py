from pygame import Vector2, sprite, display

from thefloatingdutchman.character.player.player_data import PlayerData
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.game_settings import WINDOW_HEIGHT, WINDOW_WIDTH
from thefloatingdutchman.manager import Manager


class PlayerManager(Manager):
    def __init__(self):
        super().__init__()
        self._player = None

    def spawn(self):
        player_data = PlayerData(100, 750, Vector2(
            display.Info().current_w/2, display.Info().current_h/2), 10)
        self._player = PlayerSprite(player_data)

    def draw(self, screen):
        screen.blit(self._player.image, self._player.rect)
        self._player.bullets.draw(screen)

    def update(self, screen, enemies: sprite.Group(), placeholder):
        self._player.update(screen, placeholder)
        for enemy in enemies:
            hits = sprite.spritecollide(self._player, enemy.bullets, True, sprite.collide_mask)
            for bullet in hits:
                self._player.take_damage(enemy._damage)

    @property
    def player(self):
        return self._player
