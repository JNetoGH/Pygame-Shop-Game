from _3gameobjs.map import Map
from _3gameobjs.player import Player
from rendering_layer import RenderingLayer
from _3gameobjs.test_obj import TestObj
from _1systems.scalable_game_screen_system import ScalableGameScreen


class Camara:

    def __init__(self, rendering_layers_to_render: list[RenderingLayer]):
        self._rendering_layers_to_render = rendering_layers_to_render
        self.followed_game_object = None

    def render_layers(self):
        for r_layer in self._rendering_layers_to_render:
            for game_obj in r_layer.game_objects_to_render_read_only:
                if game_obj.should__be_rendered:
                    # re-centers the image sprite rect to the new possible position
                    game_obj.rect = game_obj.image.get_rect(center=game_obj.transform.position)

                    # - draws the game object image on the dummy screen
                    # - the subtractions are need in order to displaye the image correctly because, by default it's shown at
                    #   the corner like:
                    """
                        |-------|
                        |       | => rect
                        |-------|
                                 IMAGE
                    """
                    image_x = game_obj.transform.position.x - game_obj.rect.width // 2
                    image_y = game_obj.transform.position.y - game_obj.rect.height // 2
                    ScalableGameScreen.GameScreenDummySurface.blit(game_obj.image, (image_x, image_y))

    def follow_game_object(self, game_object):
        self.followed_game_object = game_object

class Scene:
    def __init__(self, game):
        self.game = game

        """ 
        LIST USED FOR UPDATES:
            - It holds all game objects of the scene
            - When a game Obj is instantiated, it's automatically stored here using the scene passed as parameter in 
              its constructor
        """
        self.all_game_obj = []

        # - When a game Obj is instantiated, it's automatically stored here using the layer passed as parameter in its constructor
        self.rendering_layer_map = RenderingLayer()
        self.rendering_layer_0 = RenderingLayer()
        self.rendering_layer_1 = RenderingLayer()
        self.rendering_layer_tools = RenderingLayer()
        self.rendering_layers = [self.rendering_layer_map, self.rendering_layer_0, self.rendering_layer_1, self.rendering_layer_tools]

        self.map = Map("map", self, self.rendering_layer_map)
        self.player = Player("game_player", self, self.rendering_layers[0])
        self.test_obj = TestObj("test_obj_1", self, self.rendering_layers[1])

        self.scene_start()  # called once

        # main camera will render the rendering layers
        self.main_camera = Camara(self.rendering_layers)

    def scene_start(self):
        pass

    def scene_update(self):
        # first is called the components update of the object, and then the game object itself
        for gm in self.all_game_obj:
            for component in gm.components_list:
                component.component_update()
            gm.game_object_update()

    def scene_render(self):

        # clears the screen for rendering
        ScalableGameScreen.GameScreenDummySurface.fill("darkgreen")

        # renders all rendering layers
        self.main_camera.render_layers()


        """      
        OLD WAY WHEN SCENE WOULD RENDER EVERYTHING 
        WITH THIS FIELD AT THE CONSTRUCTOR: self.all_sprites = pygame.sprite.Group()  # sprite group, used to draw then all
        
        self.all_sprites.draw(ScalableGameScreen.GameScreenDummySurface)
        self.all_sprites.update()
        # used to see lines and squares mainly
        for gm in self.all_game_obj:
            gm.game_object_debug_late_render()
        """

    # CALLED BY THE InspectorDebuggingCanvas to show this text at the inpector
    def get_inspector_debugging_status(self) -> str:
        return f"SCENE DEBUGGING STATUS\n" \
               f"total rendering layers: {len(self.rendering_layers)}\n" \
               f"total game objects: {len(self.all_game_obj)}\n"

