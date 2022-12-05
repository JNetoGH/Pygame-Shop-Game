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

        ScalableGameScreen.init_screens(RES_FULL_HD, [2000,1300], RES_FULL_HD)

        # important stuff
        self.clock = pygame.time.Clock()
        self.scene_example = Scene(self)
        self.delta_time = 0

        # it is not used for much, just holds the total amount of update elapsed
        self.elapsed_updates = 0

        # should be the one of the last things to be instantiated
        self.inspector_debugging_canvas = InspectorDebuggingCanvas(self.scene_example, font_size=9)

        self.show_inspector_debugging_canvas = True

    def run_game_loop(self):
        while True:

            pygame.display.set_caption(f"JNETO PRODUCTION GAME ENGINE |  FPS {self.clock.get_fps():.1f}")
            self.elapsed_updates += 1
            GameTime.DeltaTime = self.clock.tick() / 1000
            InputManager.update()
            self.scene_example.scene_update()
            self.scene_example.scene_render()

            if InputManager.is_key_pressed(pygame.K_z):
                self.show_inspector_debugging_canvas = True
            elif InputManager.is_key_pressed(pygame.K_x):
                self.show_inspector_debugging_canvas = False
            if self.show_inspector_debugging_canvas:
                self.inspector_debugging_canvas.render_inspector_debugging_text()
                self.inspector_debugging_canvas.render_game_objects_gizmos()

            ScalableGameScreen.render_final_scaled_result()


game = Game()
game.run_game_loop()
