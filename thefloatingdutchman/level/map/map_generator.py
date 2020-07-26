from typing import List
from random import randint, choices
from ordered_set import OrderedSet

from networkx import DiGraph
import random

from thefloatingdutchman.level.room.room import Room
from thefloatingdutchman.level.room.enemy_room import EnemyRoom
from thefloatingdutchman.character.enemy.enemy_manager import EnemyManager


from thefloatingdutchman.level.room.treasure_room  import TreasureRoom
from thefloatingdutchman.objects.treasure_manager import TreasureManager
from thefloatingdutchman.character.enemy.boss.boss_manager import BossManager


class MapGenerator:

    def generate_rooms_per_col(self, num_rooms: int, max_per_col: int) -> List[int]:
        """Generate a list of ints that represent the number of rooms in each column"""
        rooms_per_col = []

        # first and last col should always have 1
        rooms_per_col.append(1)  # 0

        # account for first and last room seperately
        rooms_left = num_rooms - 2

        while rooms_left >= max_per_col+1:
            temp = randint(2, max_per_col)
            rooms_per_col.append(temp)
            rooms_left -= temp

        # this is to enforce max_per_col, may have one too many rooms
        if rooms_left == 1:
            rooms_left += 1
            num_rooms += 1
            for i, cnt in enumerate(rooms_per_col):
                if cnt > 2:
                    rooms_per_col[i] = cnt - 1
                    break

        rooms_per_col.append(rooms_left)
        rooms_per_col.append(1)  # num_rooms - 1

        return rooms_per_col

    def generate_rooms(self, num_rooms: int) -> List[Room]:

        rooms = []

        for i in range(0, num_rooms-1):
            roomChooser = random.choices([1, 2], weights=[0.5, 0.5], k=1)[0]

            if roomChooser == 1:
                rooms.append(EnemyRoom(EnemyManager()))
            else:
                rooms.append(TreasureRoom(TreasureManager()))


        rooms.append(EnemyRoom(BossManager()))
        return rooms

    def generate_room_graph(self, rooms_per_col: List[int]) -> DiGraph:

        room_graph = DiGraph()
        first_in_col = 0

        # for each column
        for i, room_count in enumerate(rooms_per_col):

            next_room_count = rooms_per_col[i+1]
            first_in_next_col = first_in_col+room_count
            last_in_col = first_in_next_col-1
            next_col_range = range(
                first_in_next_col, first_in_next_col + next_room_count)

            # once at second to last column, we can link all the rooms in the current col
            # to the final room in the last column and break out of the for loop
            if i == len(rooms_per_col) - 2:
                for _id in range(first_in_col, last_in_col+1):
                    room_graph.add_edge(_id, first_in_next_col)

                break

            if room_count > 1:

                # always make an edge on the outer path of the rooms
                room_graph.add_edge(
                    first_in_col, first_in_next_col)  # top edge
                room_graph.add_edge(
                    last_in_col, last_in_col+next_room_count)  # bottom edge

                chosen_ids = choices(next_col_range, k=room_count-2)
                chosen_ids.sort()

                # picks inside nodes from current col to join to next col
                for index, _id in enumerate(chosen_ids):
                    room_graph.add_edge(first_in_col+1+index, _id)

                chosen_ids.insert(0, first_in_next_col)
                chosen_ids.append(first_in_next_col + next_room_count - 1)

                inner_next_col_ids = set(next_col_range)

                # removes first and last from next column set
                inner_next_col_ids.remove(first_in_next_col)

                if next_room_count != 1:
                    inner_next_col_ids.remove(
                        first_in_next_col + next_room_count - 1)

                not_sel_list = list(inner_next_col_ids - set(chosen_ids))
                not_sel_list.sort(reverse=True)
                not_selected = OrderedSet(not_sel_list)

                # while we have nodes not selected
                # wish I could explain how this works...
                while not_selected:
                    _id = not_selected.pop()
                    j = _id - 1
                    k = _id

                    node_set = OrderedSet([_id])

                    j_index = [i for i, chosen_id in enumerate(
                        chosen_ids) if chosen_id == j][-1]

                    node_j_id = j_index + first_in_col

                    while k not in chosen_ids:
                        k += 1

                        if k not in chosen_ids:
                            node_set.add(k)
                            not_selected.pop()

                    k_index = chosen_ids.index(k)
                    node_k_id = k_index + first_in_col

                    choosy_listy = choices(
                        range(node_j_id, node_k_id+1), k=len(node_set))
                    choosy_listy.sort()

                    for nodey_boy, nodey_girl in zip(choosy_listy, node_set):
                        room_graph.add_edge(nodey_boy, nodey_girl)

            else:
                for _id in next_col_range:
                    room_graph.add_edge(first_in_col, _id)

            first_in_col += room_count

        return room_graph
