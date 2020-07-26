from pygame import Surface

from thefloatingdutchman.level.room.room import Room
from thefloatingdutchman.objects.treasure_manager import TreasureManager
from thefloatingdutchman.character.player.player_sprite import PlayerSprite


class TreasureRoom(Room):
    def __init__(self, treasure_manager: TreasureManager):
        super().__init__()
        self._treasure_manager = treasure_manager

    def spawn(self, level: int, _id: int):
        super().spawn(level, _id)
        self._cleared = False
        self._dropped = True
        self._treasure_manager.spawn(level)

    def update(self, player: PlayerSprite, screen: Surface):
        if self._treasure_manager._get_heart_count():
            self._treasure_manager.update(player, screen)

    def get_enemies(self):
        return None

    def cleared(self) -> bool:

        return self._cleared

    def draw(self, screen: Surface):
        self._treasure_manager.draw(screen)

    def get_proximity(self):
        return self._treasure_manager._get_proximity()

    def set_cleared(self):
        self._cleared=True
