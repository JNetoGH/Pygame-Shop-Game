import pygame

from systems.debugging_canvas import DebuggingCanvas
from systems.input_manager import InputManager
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
            InputManager.tick()
            self.delta_time = self.clock.tick() / 1000
            self.level.tick()
            self.level.render()
            self.print_status()
            pygame.display.update()

    def print_status(self):
        font = pygame.font.Font('freesansbold.ttf', 20)# create a text surface object,
        msgs = "JNETO PRODUCTIONS GAME ENGINE DEBUGGING STATUS" "\n" + \
               "\nINPUT MANAGER\n" + InputManager.get_status() + "\n" + \
               "\nPLAYER\n" + self.level.all_game_obj[0].get_status() #player is 0
        # calls the method that displays text on screen
        DebuggingCanvas.blit_text(self.screen, msgs, (20, 20), font, color="cyan")

game = Game()
game.run_game_loop()
