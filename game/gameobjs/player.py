import pygame
import numpy
from gameobjs.game_obj import GameObject
from systems.input_manager import InputManager


class Player(GameObject):
    def __init__(self, position: pygame.math.Vector2, group, level):
        super().__init__(position, group, level)

        # the image itself
        self.image = pygame.Surface((64, 32))
        self.image.fill((255, 255, 255))

        # the rectangle that represent the game object: the center pos of the rect is the same of the player pos
        self.rect = self.image.get_rect(center=self.position)

        # movement related
        self.non_normalized_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.normalized_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.speed = 200

    def start(self) -> None:
        print("oi")

    def tick(self) -> None:
        self.move()

    def move(self):
        # generates a new move direction and normalizes it
        self.normalized_direction = pygame.math.Vector2(0, 0)
        self.non_normalized_direction = pygame.math.Vector2(InputManager.Horizontal_Axis, InputManager.Vertical_Axis)
        # avoids division by 0 exception: extracts the MAGNITUDE of the non-normalized direction
        if self.non_normalized_direction.magnitude() > 0:
            self.normalized_direction = self.non_normalized_direction.normalize()  # normalizes the new direction

        # moves frame-rate independent
        self.position += self.normalized_direction * self.speed * self.level.game.delta_time
        self.rect.center = self.position  # updates the rect position

    def render(self) -> None:
        pass

    def get_status(self) -> str:
        return f"Index in Level list = {self.get_index_in_level_list()}\n" \
               f"Speed: {self.speed}\n" \
               f"Position: {self.position}\n" \
               f"Normalized Direction: {self.normalized_direction}, magnitude={numpy.linalg.norm(self.normalized_direction)}\n" \
               f"Non-Normalized Direction: {self.non_normalized_direction}, magnitude={numpy.linalg.norm(self.non_normalized_direction)}"


