import pygame
from _1systems.input.input_manager import InputManager
from _1systems.screen.scalable_game_screen import ScalableGameScreen
from _1systems.time.game_time import GameTime
from scene import Scene


class InspectorDebuggingCanvas:

    def __init__(self, scene: Scene, font_size):
        self.current_game_object_index = 0
        self.current_scene = scene
        self.font_size = font_size

    def render_inspector_debugging_text(self):
        font = pygame.font.Font('_0resources/fonts/JetBrainsMono-Medium.ttf', self.font_size)  # create a text surface object,
        msgs = "JNETO PRODUCTIONS GAME ENGINE: INSPECTOR DEBUGGING SYSTEM\n" \
               "\nENGINE INNER DETAILS" + \
               f"\nfps: {self.current_scene.game.clock.get_fps():.1f}" + \
               f"\nelapsed updates: {self.current_scene.game.elapsed_updates}" + \
               f"\ndelta-time: {str(GameTime.DeltaTime)}\n" \
               f"\n{ScalableGameScreen.get_inspector_debugging_status()}" + \
               f"\n{InputManager.get_inspector_debugging_status()}" + \
               f"\n{self.current_scene.all_game_obj[0].get_inspector_debugging_status()}"  # player is 0 in the list of objects as well
        # calls the method that displays text on the dummy screen
        InspectorDebuggingCanvas._blit_text(ScalableGameScreen.GameScreenDummySurface, msgs, (20, 20), font, color="cyan")

    @staticmethod
    # print text on screen with \n
    def _blit_text(surface, text, pos, font, color=pygame.Color('blue')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
