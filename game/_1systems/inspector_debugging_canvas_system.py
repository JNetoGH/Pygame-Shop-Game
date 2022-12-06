import pygame
from _1systems.input_manager_system import InputManager
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _1systems.game_time_system import GameTime
from _1systems.text_rendering_system import TextRender
from scene import Scene


class InspectorDebuggingCanvas:

    def __init__(self, scene: Scene, font_size=10):
        self.current_game_object_index = 0
        self.current_scene = scene
        self.font_size = font_size

    def render_inspector_debugging_text(self):
        font = pygame.font.Font('_0resources/fonts/JetBrainsMono-Medium.ttf',
                                self.font_size)  # create a text surface object,

        msgs = "JNETO PRODUCTIONS GAME ENGINE: INSPECTOR DEBUGGING SYSTEM\n\n" \
               f"ENGINE INNER DETAILS\n" \
               f"fps: {self.current_scene.game.clock.get_fps():.1f}\n" \
               f"elapsed updates: {self.current_scene.game.elapsed_updates}\n" \
               f"delta-time: {str(GameTime.DeltaTime)}\n\n" \
               f"{ScalableGameScreen.get_inspector_debugging_status()}\n" + \
               f"{InputManager.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.get_inspector_debugging_status()}\n" \
               f"{self.current_scene.all_game_obj[1].get_inspector_debugging_status()}\n"  # player is 0 in the list of objects as well

        # calls the method that displays text on the dummy screen
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth // 3,
                             msgs, (20, 20), font, color=pygame.Color("white"))

    def render_game_objects_gizmos(self):
        for gm_obj in self.current_scene.all_game_obj:
            gm_obj.game_object_debug_late_render_gizmos()
