import pygame

from _1systems.debug.debugging_canvas import DebuggingCanvas
from _1systems.input.input_manager import InputManager
from _1systems.time.time import Time
from level import Level
from settings import *


class Game:

    def __init__(self):
        pygame.init()
        self.screen: pygame.SurfaceType = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level(self)
        self.delta_time = 0

    def run_game_loop(self):
        while True:
            pygame.display.set_caption(f"Farmer | FPS = {self.clock.get_fps():.1f}")
            Time.DeltaTime = self.clock.tick() / 1000
            InputManager.tick()
            self.level.tick()
            self.level.render()
            self.print_status()
            pygame.display.update()

    def print_status(self):
        font = pygame.font.Font('freesansbold.ttf', 15)  # create a text surface object,
        msgs = "JNETO PRODUCTIONS GAME ENGINE DEBUGGING STATUS\n" + \
               "\nTIME\n" + "delta time: " + str(Time.DeltaTime) + "\n" + \
               "\nINPUT MANAGER\n" + InputManager.get_status() + "\n" + \
               "\nPLAYER\n" + self.level.player.get_status()  #  player is 0 in the list of objects as well
        # calls the method that displays text on screen
        DebuggingCanvas.blit_text(self.screen, msgs, (20, 20), font, color="cyan")

game = Game()
game.run_game_loop()
