from pygame import Surface

from thefloatingdutchman.level.room.room import Room
from thefloatingdutchman.character.enemy.enemy_manager import EnemyManager
from thefloatingdutchman.character.player.player_sprite import PlayerSprite


class EnemyRoom(Room):
    def __init__(self, enemy_manager: EnemyManager):
        super().__init__()
        self._enemy_manager = enemy_manager

    def spawn(self, level: int, _id: int):
        super().spawn(level, _id)
        self._cleared = False
        self._dropped = False
        self._enemy_manager.spawn(level)

    def update(self, player: PlayerSprite, screen: Surface):
        if self._enemy_manager.get_enemy_count():
            self._enemy_manager.update(player, screen)

    def get_enemies(self):
        return self._enemy_manager._enemies

    def get_proximity(self):
        return False

    def cleared(self) -> bool:
        return not self._enemy_manager.get_enemy_count()

    def draw(self, screen: Surface):
        self._enemy_manager.draw(screen)
