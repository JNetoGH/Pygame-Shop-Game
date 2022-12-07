import pygame

from Test2 import Test2Obj
from _1systems.inspector_debugging_canvas_system import InspectorDebuggingCanvas
from _1systems.input_manager_system import InputManager
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _1systems.game_time_system import GameTime
from _3gameobjs.map import Map
from _3gameobjs.player import Player
from _3gameobjs.test_obj import TestObj
from camera import Camara
from rendering_layer import RenderingLayer
from scene import Scene


class Game:

    def __init__(self):

        pygame.init()

        # 21:9
        RES_WFHD= [2560, 1080]

        # 16:9
        RES_NHD = [640, 360]
        RES_FWVGA = [854, 480]
        RES_HD = [1280, 720]
        RES_HD_PLUS = [1600, 900]
        RES_FULL_HD = [1920, 1080]
        RES_2K_QHD = [2560, 1440]
        RES_4K = [3840, 2160]

        ScalableGameScreen.init_screens(RES_HD_PLUS ,RES_HD_PLUS ,RES_HD_PLUS )

        # important stuff
        self.clock = pygame.time.Clock()
        self.scene_example = Scene(self)
        self.delta_time = 0

        # it is not used for much, just holds the total amount of update elapsed
        self.elapsed_updates = 0

        # should be the one of the last things to be instantiated
        self.inspector_debugging_canvas = InspectorDebuggingCanvas(self.scene_example, font_size=15)

        # show both the inspector lateral info and the gizmos
        self.show_inspector_debugging_canvas = True
        self.show_debugging_gizmos = True

    def run_game_loop(self):

        # SCENE DEPENDENCIES

        # rendering layer
        self.rendering_layer_map = RenderingLayer()
        self.rendering_layer_test = RenderingLayer()
        self.rendering_layer_player = RenderingLayer()
        self.rendering_layer_tools = RenderingLayer()

        # loading the rendering layers to scene
        self.scene_example.rendering_layers = [self.rendering_layer_map, self.rendering_layer_test, self.rendering_layer_player, self.rendering_layer_tools]

        # game objects
        self.map = Map("map", self.scene_example, self.rendering_layer_map)
        self.player = Player("game_player", self.scene_example, self.rendering_layer_player)
        self.player.transform.position = pygame.Vector2(500, 500)
        self.test_obj = TestObj("test_obj_1", self.scene_example, self.rendering_layer_test)
        self.test_obj2 = Test2Obj("test2", self.scene_example, self.rendering_layer_test)

        # the main Camera
        # self.scene_example.rendering_layers == [self.rendering:layer..., self.rendering_layer...] same thing,
        # I am just doing it because I have already set the rendering layers of the scene
        self.scene_example.main_camera = Camara(self.scene_example.rendering_layers)
        # sets the camera to follow the payer
        self.scene_example.main_camera.follow_game_object(self.player)

        # Runs the game
        while True:

            pygame.display.set_caption(f"JNETO PRODUCTION GAME ENGINE |  FPS {self.clock.get_fps():.1f}")
            self.elapsed_updates += 1
            GameTime.DeltaTime = self.clock.tick() / 1000
            InputManager.update()
            self.scene_example.scene_update()
            self.scene_example.scene_render()

            # debugging inspector system and gizmos
            if InputManager.is_key_pressed(pygame.K_z):
                self.show_inspector_debugging_canvas = True
            elif InputManager.is_key_pressed(pygame.K_x):
                self.show_inspector_debugging_canvas = False
            if InputManager.is_key_pressed(pygame.K_c):
                self.show_debugging_gizmos = True
            elif InputManager.is_key_pressed(pygame.K_v):
                self.show_debugging_gizmos = False

            if self.show_debugging_gizmos:
                self.inspector_debugging_canvas.render_scene_game_objects_gizmos()

            # needs to be on top of gizmos
            if self.show_inspector_debugging_canvas:
                self.inspector_debugging_canvas.render_inspector_debugging_text()
                # the second text that shows the game object info on screen
                #self.inspector_debugging_canvas.render_game_object_inspector_debugging_status(1, "white")

            # for testing the camera
            if InputManager.is_key_pressed(pygame.K_q):
                self.scene_example.main_camera.follow_game_object(self.player)
            if InputManager.is_key_pressed(pygame.K_e):
                self.scene_example.main_camera.stop_following_current_set_game_object()
            if InputManager.is_key_pressed(pygame.K_r):
                self.scene_example.main_camera.focus_camera_at_world_position(pygame.Vector2(300, 300))

            # render the final produced frame
            ScalableGameScreen.render_final_scaled_result()


game = Game()
game.run_game_loop()
