import pygame
from _1systems.inspector_debug.inspector_debugging_canvas import InspectorDebuggingCanvas
from _1systems.input.input_manager import InputManager
from _1systems.screen.scalable_game_screen import ScalableGameScreen
from _1systems.time.time import Time
from level import Level


class Game:

    def __init__(self):
        pygame.init()
        ScalableGameScreen.init_screens([1280, 720], [2000, 1000], [1600, 900])
        self.clock = pygame.time.Clock()
        self.level = Level(self)
        self.delta_time = 0
        self.ticks = 0  # it is not used for much, just holds the total amount of ticks elapsed
        self.max_amount_of_ticks = 1000000000

    def run_game_loop(self):
        while True:

            self.ticks += 1
            if self.ticks == self.max_amount_of_ticks:
                self.ticks = 0

            Time.DeltaTime = self.clock.tick() / 1000
            InputManager.tick()
            self.level.tick()
            self.level.render()
            self.render_status()
            ScalableGameScreen.render_final_scaled_result()


    def render_status(self):
        font = pygame.font.Font('_0resources/fonts/JetBrainsMono-Medium.ttf', 16)  # create a text surface object,
        msgs = "JNETO PRODUCTIONS GAME ENGINE: INSPECTOR DEBUGGING SYSTEM\n" + \
               f"\nFPS: {self.clock.get_fps():.1f}" + \
               f"\nTICKS: {self.ticks}" + \
               f"\nDELTA-TIME: {str(Time.DeltaTime)}\n" + \
               f"\nINPUT MANAGER\n{InputManager.get_status()}\n" + \
               f"\nPLAYER\n  {self.level.player.get_status()}"  # player is 0 in the list of objects as well

        # calls the method that displays text on screen
        InspectorDebuggingCanvas.blit_text(ScalableGameScreen.GameScreenDummySurface, msgs, (20, 20), font, color="cyan")


game = Game()
game.run_game_loop()
