import pygame
import numpy

from _1systems.input.input_manager import InputManager
from _1systems.screen.scalable_game_screen import ScalableGameScreen
from _1systems.time.game_time import GameTime
from _2components.animation.animation_clip import AnimationClip
from _2components.animation.animation_controller import AnimationController
from _3gameobjs.game_obj import GameObject


class Player(GameObject):

    def __init__(self, scene):
        super().__init__(scene)
        # movement related
        self.move_speed = 200
        self.normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.non_normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)

        # animations and controller
        self.animation_walk_down = AnimationClip("walk_down", "_0resources/graphics/character/down_walk")
        self.animation_walk_right = AnimationClip("walk_right", "_0resources/graphics/character/right_walk")
        self.animation_walk_up = AnimationClip("walk_up", "_0resources/graphics/character/up_walk")
        self.animation_walk_left = AnimationClip("walk_left", "_0resources/graphics/character/left_walk")
        self.animation_idle_down = AnimationClip("idle_down", "_0resources/graphics/character/down_idle")
        self.animation_idle_right = AnimationClip("idle_right", "_0resources/graphics/character/right_idle")
        self.animation_idle_up = AnimationClip("idle_up", "_0resources/graphics/character/up_idle")
        self.animation_idle_left = AnimationClip("idle_left", "_0resources/graphics/character/left_idle")
        # animation controller
        animation_clips = [self.animation_walk_right, self.animation_walk_up, self.animation_walk_left, self.animation_walk_down]
        self.animation_controller = AnimationController(animation_clips, self)
        self.animation_controller.add_animation(self.animation_idle_right, self.animation_idle_up, self.animation_idle_left, self.animation_idle_down)
        # the image itself
        self.image = self.animation_idle_down.images[0]

        # tooling player system
        self.selected_tool = "axe"

    def start(self) -> None:
        pass

    def update(self) -> None:
        self.move()

        #tool
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            pass
            # run a timer for the tool usage

    def render(self) -> None:
        super().render()
        self.animate()

    def animate(self):
        isMoving = not(InputManager.Vertical_Axis == 0 and InputManager.Horizontal_Axis == 0)
        if isMoving:  # animacoes de cima e baixo tem pioridade sobre as laterais
            if InputManager.Horizontal_Axis == -1:
                self.animation_controller.set_current_animation("walk_left")
            elif InputManager.Horizontal_Axis == 1:
                self.animation_controller.set_current_animation("walk_right")
            if InputManager.Vertical_Axis == -1:
                self.animation_controller.set_current_animation("walk_up")
            elif InputManager.Vertical_Axis == 1:
                self.animation_controller.set_current_animation("walk_down")
        else:
            if self.animation_controller.current_animation_clip == self.animation_walk_down:
                self.animation_controller.set_current_animation("idle_down")
            elif self.animation_controller.current_animation_clip == self.animation_walk_up:
                self.animation_controller.set_current_animation("idle_up")
            elif self.animation_controller.current_animation_clip == self.animation_walk_left:
                self.animation_controller.set_current_animation("idle_left")
            elif self.animation_controller.current_animation_clip == self.animation_walk_right:
                self.animation_controller.set_current_animation("idle_right")
        self.animation_controller.animate()

    def move(self) -> None:
        # generates a direction based on players input
        self.non_normalized_direction = pygame.Vector2(InputManager.Horizontal_Axis, InputManager.Vertical_Axis)
        # normalizes the direction, but checks before if the Magnitude is not 0, otherwise it will launch an exception
        if numpy.linalg.norm(self.non_normalized_direction) != 0:
            self.normalized_direction = self.non_normalized_direction / numpy.linalg.norm(self.non_normalized_direction)
        else:
            self.normalized_direction = pygame.Vector2(0, 0)
        # creates a new position with the new direction
        new_position: pygame.Vector2 = self.transform.position_read_only
        new_position.x += self.normalized_direction.x * self.move_speed * GameTime.DeltaTime
        new_position.y += self.normalized_direction.y * self.move_speed * GameTime.DeltaTime
        self.transform.move_position(new_position)

    def get_inspector_debugging_status(self) -> str:
        return super().get_inspector_debugging_status() + \
               f"Player Self Implemented Debugging Stats\n" \
               f"speed: {self.move_speed}\n" \
               f"normalized direction: {self.normalized_direction}\n" \
               f"normalized direction magnitude: {numpy.linalg.norm(self.normalized_direction)}\n" \
               f"non-normalized direction: {self.non_normalized_direction}\n" \
               f"non-normalized direction magnitude: {numpy.linalg.norm(self.non_normalized_direction)}\n" \

