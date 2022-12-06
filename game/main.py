import pygame
from _1systems.inspector_debugging_canvas_system import InspectorDebuggingCanvas
from _1systems.input_manager_system import InputManager
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _1systems.game_time_system import GameTime
from scene import Scene


class Game:

    def __init__(self):

        """
            KEYS USED SO FAR:

                 - player:
                         SPACE = USE TOOL (usage compute when the timer is over)
                         P = CHANGE TOOL
                         L_CONTROL = PLANT SEED (when used is removed from the seeds list)
                         O = CHANGE SEED
                 - Game for (show_inspector_debugging_canvas)
                         Z show the debugging canvas
                         X hides the debugging canvas
                         C show gizmos
                         V hide gizmos
                 - Camara Testing
                        Q follows player
                        E stops following player
                        R focus camera at point 300 300

        """

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
        self.inspector_debugging_canvas = InspectorDebuggingCanvas(self.scene_example, font_size=8)

        # show both the inspector lateral info and the gizmos
        self.show_inspector_debugging_canvas = True
        self.show_debugging_gizmos = True

    def run_game_loop(self):
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
            if self.show_inspector_debugging_canvas:
                self.inspector_debugging_canvas.render_inspector_debugging_text()
            if self.show_debugging_gizmos:
                self.inspector_debugging_canvas.render_game_objects_gizmos()

            # for testing the camera
            if InputManager.is_key_pressed(pygame.K_q):
                self.scene_example.main_camera.follow_game_object(self.scene_example.player)
            if InputManager.is_key_pressed(pygame.K_e):
                self.scene_example.main_camera.stop_following_current_set_game_object()
            if InputManager.is_key_pressed(pygame.K_r):
                self.scene_example.main_camera.focus_camera_at_world_position(pygame.Vector2(300, 300))

            # render the final produced frame
            ScalableGameScreen.render_final_scaled_result()


game = Game()
game.run_game_loop()
