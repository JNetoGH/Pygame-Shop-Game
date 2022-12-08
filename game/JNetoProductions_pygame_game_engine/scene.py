from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen

class Scene:

    def __init__(self, camera):

        # It holds all game_loop objects of the scene When a game_loop Obj is instantiated,
        # it's automatically stored here using the scene passed as parameter in  its constructor
        self.all_game_obj = []
        # main camera will render the rendering layers
        self.main_camera = camera

        # called once if i want to start stuff in here
        self.scene_start()

    def get_game_object_by_name(self, name: str):
        for game_obj in self.all_game_obj:
            if game_obj.name == name:
                return game_obj

    def scene_start(self):
        pass

    def scene_update(self):
        # first updates the components then the game_loop object itself
        for gm in self.all_game_obj:
            for component in gm.components_list:
                component.component_update()
            gm.game_object_update()

    def scene_render(self):
        # clears the screen for rendering
        ScalableGameScreen.GameScreenDummySurface.fill("green")
        # renders all rendering layers
        self.main_camera.render_layers()

    # CALLED BY THE InspectorDebuggingCanvas to show this text at the inspector
    def get_inspector_debugging_status(self) -> str:
        game_obj_names = []
        for gm_obj in self.all_game_obj:
            game_obj_names.append(gm_obj.name)
        return f"SCENE DEBUGGING STATUS\n" \
               f"total rendering layers: {len(self.main_camera.rendering_layers)}\n" \
               f"total game objects: {len(self.all_game_obj)}\n" \
               f"list: {game_obj_names}\n"
