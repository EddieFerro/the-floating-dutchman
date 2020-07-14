from typing import List, Tuple
from math import sqrt, atan, degrees

from pygame import sprite, Surface, mouse, K_m, event, display, transform, KEYDOWN, MOUSEBUTTONDOWN, QUIT, transform
from pygame.math import Vector2

from thefloatingdutchman.level.room.room import Room
from thefloatingdutchman.game_settings import WHITE, GREEN, BLACK, GRAY, YELLOW, RED, WINDOW_HEIGHT, WINDOW_WIDTH


class RoomMarkerUI(sprite.Sprite):
    def __init__(self, x: int, y: int, width: int):
        sprite.Sprite.__init__(self)
        self.pos = Vector2(x, y)
        self.image = Surface((width, width))
        self.rect = self.image.get_rect(center=self.pos)
        self.image.fill(GRAY)


class RoomPathUI(sprite.Sprite):
    def __init__(self, topleft: Tuple[int, int], center: Tuple[int, int], length: float, deg_rotate: float):
        sprite.Sprite.__init__(self)
        self.image = Surface((int(length), 10))
        self.image.fill(GRAY)
        self.image.set_colorkey(BLACK)
        self.pos = topleft
        self.rect = self.image.get_rect(center=center)

        self.image = transform.rotate(self.image, deg_rotate)
        self.rect = self.image.get_rect()
        self.rect.center = center

    def draw(self, screen: Surface):
        screen.blit(self.image, self.rect)


class MapUI:
    def __init__(self):
        self._dots = sprite.Group()
        self._paths = sprite.Group()

    def _fill_shape(self,
                    sprite,
                    room: Room,
                    moveable_rooms: List[int],
                    current_room_id: int):

        if room.cleared():
            sprite.image.fill(YELLOW)
        elif room.id == current_room_id:
            sprite.image.fill(RED)
        elif room.id in moveable_rooms:
            if sprite.rect.collidepoint(mouse.get_pos()):
                sprite.image.fill(RED)
            else:
                sprite.image.fill(WHITE)
        else:
            sprite.image.fill(GREEN)

    def spawn(self, room_manager):
        self._dots.empty()
        self._dot_list = []
        self._paths.empty()

        num_rows = len(room_manager.rooms_per_row)

        for i, room_per_row in enumerate(room_manager.rooms_per_row):
            for j in range(room_per_row):
                temp_dot = RoomMarkerUI(
                    ((display.Info().current_w)*(i+1))/(num_rows+1),
                    (display.Info().current_h)*(j+1)/(room_per_row+1),
                    25
                )
                # double memory overhead, big oof
                self._dots.add(temp_dot)
                self._dot_list.append(temp_dot)

        for v1, v2 in room_manager._room_graph.edges:
            x1, y1 = self._dot_list[v1].pos
            x2, y2 = self._dot_list[v2].pos

            c1 = (x1 + x2)/2
            c2 = (y1+y2)/2

            x_len = x2 - x1
            y_len = y2 - y1

            hyp = sqrt(x_len**2 + y_len**2)
            rot = 180 - degrees(atan(y_len/(x_len)))
            self._paths.add(RoomPathUI((x1, y2), (c1, c2), hyp, rot))

    def render(self, screen,
               rooms: List[Room],
               moveable_rooms: List[int],
               current_room_id: int,
               set_current_room,
               placeholder
               ) -> bool:

        while True:
            for dot, room in zip(self._dots, rooms):
                self._fill_shape(dot, room, moveable_rooms, current_room_id)

            placeholder.fill(BLACK)
            self._paths.draw(placeholder)
            self._dots.draw(placeholder)

            display.flip()

            for e in event.get():
                if e.type == KEYDOWN and e.key == K_m and not rooms[current_room_id].cleared():
                    return False
                elif e.type == MOUSEBUTTONDOWN:
                    x, y = e.pos
                    for _id in moveable_rooms:

                        if self._dot_list[_id].rect.collidepoint(x, y):
                            set_current_room(_id)
                            return False
                elif e.type == QUIT:
                    return True
