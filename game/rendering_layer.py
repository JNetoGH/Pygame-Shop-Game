from _1systems.scalable_game_screen_system import ScalableGameScreen
from _3gameobjs.game_object import GameObject


class RenderingLayer:

    def __init__(self, is_fixed_on_screen=False):
        self.is_fixed_on_screen = is_fixed_on_screen
        self._game_objects_to_render: list[GameObject] = []

    @property
    def game_objects_to_render_read_only(self):
        return self._game_objects_to_render

    def add_game_object(self, game_object: GameObject):
        self._game_objects_to_render.append(game_object)

    def remove_game_object(self, game_object: GameObject):
        self._game_objects_to_render.remove(game_object)
