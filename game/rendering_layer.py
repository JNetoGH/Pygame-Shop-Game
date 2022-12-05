from _1systems.scalable_game_screen_system import ScalableGameScreen
from _3gameobjs.game_obj import GameObject


class RenderingLayer:

    def __init__(self):
        self._game_objects_to_render: list[GameObject] = []

    def add_game_object(self, game_object: GameObject):
        self._game_objects_to_render.append(game_object)

    def remove_game_object(self, game_object: GameObject):
        self._game_objects_to_render.remove(game_object)

    def render_all_game_objects(self):
        for gm in self._game_objects_to_render:
            if gm.should__be_rendered:
                gm.game_object_render()
