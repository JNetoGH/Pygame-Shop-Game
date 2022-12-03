import pygame
import numpy

from systems.animation.animation_clip import AnimationClip
from systems.animation.animation_controller import AnimationController
from gameobjs.game_obj import GameObject
from systems.input.input_manager import InputManager


class Player(GameObject):
    def __init__(self, position: pygame.math.Vector2, group, level):
        super().__init__(position, group, level)

        # movement related
        self.non_normalized_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.normalized_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.move_speed = 200

        # animations and controller
        self.animation_walk_down = AnimationClip("walk_down", "0resources/graphics/character/down_walk")
        self.animation_walk_right = AnimationClip("walk_right", "0resources/graphics/character/right_walk")
        self.animation_walk_up = AnimationClip("walk_up", "0resources/graphics/character/up_walk")
        self.animation_walk_left = AnimationClip("walk_left", "0resources/graphics/character/left_walk")
        self.animation_controller = AnimationController(self.animation_walk_down)
        self.animation_controller.add_animation(self.animation_walk_right, self.animation_walk_up, self.animation_walk_left)

        # the image itself
        self.image = self.animation_walk_right.images[0]

        # the rectangle that represent the game object: the center pos of the rect is the same of the player pos
        self.rect = self.image.get_rect(center=self.position)

    def start(self) -> None:
        print("oi")

    def tick(self) -> None:
        self.move()

    def render(self) -> None:
        if InputManager.Horizontal_Axis == -1:
            self.animation_controller.set_current_animation("walk_left")
        if InputManager.Horizontal_Axis == 1:
            self.animation_controller.set_current_animation("walk_right")
        if InputManager.Vertical_Axis == -1:
            self.animation_controller.set_current_animation("walk_up")
        if InputManager.Vertical_Axis == 1:
            self.animation_controller.set_current_animation("walk_down")
        self.animation_controller.animate(self)

    def move(self) -> None:
        # generates a new move direction and normalizes it
        self.normalized_direction = pygame.math.Vector2(0, 0)
        self.non_normalized_direction = pygame.math.Vector2(InputManager.Horizontal_Axis, InputManager.Vertical_Axis)
        # avoids division by 0 exception: extracts the MAGNITUDE of the non-normalized direction
        if numpy.linalg.norm(self.non_normalized_direction) != 0:
            # normalizes the new direction
            self.normalized_direction = self.non_normalized_direction / numpy.linalg.norm(self.non_normalized_direction)
        # moves frame-rate independent
        self.position.x += self.normalized_direction.x * self.move_speed * self.level.game.delta_time
        self.position.y += self.normalized_direction.y * self.move_speed * self.level.game.delta_time
        self.rect.center = self.position  # updates the rect position

    def get_status(self) -> str:
        return f"Index in Level list = {self.get_index_in_level_list()}\n" \
               f"Speed: {self.move_speed}\n" \
               f"Position: {self.position}\n" \
               f"Normalized Direction: {self.normalized_direction}, magnitude={numpy.linalg.norm(self.normalized_direction)}\n" \
               f"Non-Normalized Direction: {self.non_normalized_direction}, magnitude={numpy.linalg.norm(self.non_normalized_direction)}"
