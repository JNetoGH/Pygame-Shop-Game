from _1systems.scalable_game_screen_system import ScalableGameScreen


class Scene:

    def __init__(self, game):

        # I don't know if it is going to stay here, some things use it to accesses de Game class, but whatever
        self.game = game

        # It holds all game objects of the scene When a game Obj is instantiated,
        # it's automatically stored here using the scene passed as parameter in  its constructor
        self.all_game_obj = []
        # - When a game Obj is instantiated, it's automatically stored here using the layer passed as parameter in its constructor
        self.rendering_layers = []
        # main camera will render the rendering layers
        self.main_camera = None

        # called once if i want to start stuff in here
        self.scene_start()

    def scene_start(self):
        pass

    def scene_update(self):
        # first updates the components then the game object itself
        for gm in self.all_game_obj:
            for component in gm.components_list:
                component.component_update()
            gm.game_object_update()

    def scene_render(self):
        # clears the screen for rendering
        ScalableGameScreen.GameScreenDummySurface.fill("darkgreen")
        # renders all rendering layers
        self.main_camera.render_layers()

    # CALLED BY THE InspectorDebuggingCanvas to show this text at the inspector
    def get_inspector_debugging_status(self) -> str:
        game_obj_names = []
        for gm_obj in self.all_game_obj:
            game_obj_names.append(gm_obj.name)
        return f"SCENE DEBUGGING STATUS\n" \
               f"total rendering layers: {len(self.rendering_layers)}\n" \
               f"total game objects: {len(self.all_game_obj)}\n" \
               f"list: {game_obj_names}\n"
