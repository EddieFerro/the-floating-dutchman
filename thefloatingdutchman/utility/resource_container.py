from os import path

from pygame import image


class ResourceContainer:

    def __init__(self):
        super().__init__()
        self._resources = {}
        self._load_resources()

    def _load_resources(self):
        self._resources['heart'] = self._load_sprite("heart.png")
        self._resources['treasure'] = self._load_sprite("treasure.png")

        self._resources['cannonball'] = self._load_sprite("cannonball.png")
        self._resources['laser_shot_1'] = self._load_sprite("laser_shot_1.png")
        self._resources['red_fighter'] = self._load_sprite("red_fighter.png")

        self._resources['green_fighter'] = self._load_sprite(
            "green_fighter.png")

        self._resources['pirate_ship'] = self._load_sprite("pirate_ship.png")

        self._resources['first_boss'] = self._load_sprite("first_boss.png")

        self.resources['first_boss_enraged'] = self._load_sprite("first_boss_enraged.png")

        self._resources['minion_boss'] = self._load_sprite("minion_boss.png")

        self._resources['alien_boss_sprite'] = self._load_sprite(
            "alien_boss_sprite.png")

        self._resources['level_1_background'] = self._load_path(
            "../utility/space_images/level_1_background.jpg")

        self._resources['level_2_background'] = self._load_path(
            "../utility/space_images/level_2_background.jpg")

        self._resources['level_3_background'] = self._load_path(
            "../utility/space_images/level_3_background.jpg")

    def _load_sprite(self, file: str):
        return image.load(path.join(path.dirname(
            path.realpath(__file__)), file)).convert_alpha()

    def _load_path(self, file: str):
        return path.join(path.dirname(
            path.realpath(__file__)), file)

    @property
    def resources(self) -> map:
        return self._resources
