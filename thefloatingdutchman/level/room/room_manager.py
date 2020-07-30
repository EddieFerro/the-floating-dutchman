from typing import List

from pygame import Surface

from thefloatingdutchman.manager import Manager
from thefloatingdutchman.character.player.player_sprite import PlayerSprite
from thefloatingdutchman.character.enemy.enemy_sprite import EnemySprite
from thefloatingdutchman.level.map.map_generator import MapGenerator
from thefloatingdutchman.user_interface.map_ui import MapUI
from thefloatingdutchman.utility.resource_container import ResourceContainer
from thefloatingdutchman.level.room.room import Room
from thefloatingdutchman.level.room.enemy_room import EnemyRoom
from thefloatingdutchman.character.enemy.enemy_manager import EnemyManager
from thefloatingdutchman.character.enemy.boss.boss_manager import BossManager
import random
from thefloatingdutchman.level.room.treasure_room  import TreasureRoom
from thefloatingdutchman.objects.treasure_manager import TreasureManager

class RoomManager(Manager):
    def __init__(self, res_container: ResourceContainer):
        super().__init__(res_container)
        self._map_generator = MapGenerator()
        self._map_ui = MapUI()

    def spawn(self, level: int):
        self._number_of_rooms = 26
        self._current_room_id = 0
        self._rooms_per_col = self._map_generator.generate_rooms_per_col(
            self._number_of_rooms, 5)

        self._room_graph = self._map_generator.generate_room_graph(
            self._rooms_per_col)

        self._rooms = self._generate_rooms()

        for i, room in enumerate(self._rooms):
            room.spawn(level, i)

        self._map_ui.spawn(self._rooms_per_col, self._room_graph.edges())

    def get_available_rooms(self) -> List[int]:

        # room must be cleared to move on
        if not self._rooms[self._current_room_id].cleared():
            return []

        # gets pairs of edges from current room to next available rooms
        edges = self._room_graph.edges(self._current_room_id)

        # gets list of rooms player can move to next
        return [v2 for v1, v2 in edges]

    def is_room_cleared(self) -> bool:

        return self._rooms[self._current_room_id].cleared()

    def is_level_cleared(self) -> bool:
        return self.is_room_cleared() and not self.get_available_rooms()

    def set_current_room(self, _id: int):
        if _id >= self._number_of_rooms < 0:
            raise ValueError("id provided was out of available room range")

        self._current_room_id = _id

    def update(self, player: PlayerSprite, screen: Surface):
        self._rooms[self._current_room_id].update(player, screen)

    def draw(self, screen):
        self._rooms[self._current_room_id].draw(screen)

    def get_current_enemies(self) -> List[EnemySprite]:
        return self._rooms[self._current_room_id].get_enemies()

    def render_map(self, screen, showMessage, dropCount, aMode) -> bool:
        return self._map_ui.render(screen, self._rooms,
                                   self.get_available_rooms(),
                                   self._current_room_id, self.set_current_room, showMessage, dropCount, aMode)

    def _generate_rooms(self) -> List[Room]:

        rooms = []
        treasure_count =0

        for i in range(0, self._number_of_rooms-1):
            roomChooser = random.choices([1, 2], weights=[0.6, 0.4], k=1)[0]
            if roomChooser == 1:
                rooms.append(EnemyRoom(self._res_container,
                                       EnemyManager(self._res_container)))
            elif treasure_count<2 and i != 0:
                rooms.append(TreasureRoom(self._res_container,
                                       TreasureManager(self._res_container)))
                treasure_count += 1
            else:
                rooms.append(EnemyRoom(self._res_container,
                                       EnemyManager(self._res_container)))


        rooms.append(EnemyRoom(self._res_container,
                               BossManager(self._res_container)))
        return rooms
    def get_proximity(self) -> bool:
        return self._rooms[self._current_room_id].get_proximity()
    def set_cleared(self):
        self._rooms[self._current_room_id].set_cleared()
    def  is_boss(self):
        return self._rooms[self._current_room_id].is_boss()
    def  get_id(self):
        return self._current_room_id
