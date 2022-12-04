import pygame
import numpy

from _1systems.input.input_manager import InputManager
from _1systems.time.game_time import GameTime
from _1systems.time.timer import Timer
from _2components.animation.animation_clip import AnimationClip
from _2components.animation.animation_controller import AnimationController
from _2components.single_sprite.single_sprite import SingleSprite
from _3gameobjs.game_obj import GameObject


class Player(GameObject):

    def __init__(self, scene):
        super().__init__(scene)
        # movement related
        self.move_speed = 200
        self.normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.non_normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)

        # game object default sprite
        self.single_sprite = SingleSprite("_0resources/graphics/character/down_idle/0.png", self)

        # used in animations holds the last direction the player faced while walking e.g. left, up...
        self.last_direction_before_stop = ""

        # animations and controller
        self.animation_walk_down =  AnimationClip("walk_down",  4, "_0resources/graphics/character/down_walk")
        self.animation_walk_right = AnimationClip("walk_right", 4, "_0resources/graphics/character/right_walk")
        self.animation_walk_up =    AnimationClip("walk_up",    4, "_0resources/graphics/character/up_walk")
        self.animation_walk_left =  AnimationClip("walk_left",  4, "_0resources/graphics/character/left_walk")
        self.animation_idle_down =  AnimationClip("idle_down",  4, "_0resources/graphics/character/down_idle")
        self.animation_idle_right = AnimationClip("idle_right", 4, "_0resources/graphics/character/right_idle")
        self.animation_idle_up =    AnimationClip("idle_up",    4, "_0resources/graphics/character/up_idle")
        self.animation_idle_left =  AnimationClip("idle_left",  4, "_0resources/graphics/character/left_idle")

        # animation controller
        animation_clips = [self.animation_walk_right, self.animation_walk_up, self.animation_walk_left,
                           self.animation_walk_down, self.animation_idle_right, self.animation_idle_up,
                           self.animation_idle_left, self.animation_idle_down]
        self.animation_controller = AnimationController(animation_clips, self)

        # tools animations
        self.animation_axe_down =  AnimationClip("axe_down",  4, "_0resources/graphics/character/down_axe")
        self.animation_axe_right = AnimationClip("axe_right", 4, "_0resources/graphics/character/right_axe")
        self.animation_axe_up =    AnimationClip("axe_up",    4, "_0resources/graphics/character/up_axe")
        self.animation_axe_left =  AnimationClip("axe_left",  4, "_0resources/graphics/character/left_axe")
        self.animation_controller.add_animation(self.animation_axe_up, self.animation_axe_down,
                                                self.animation_axe_left, self.animation_axe_right)

        # tooling player timer system
        self.selected_tool = "axe"
        self.tool_use_exit_timer = Timer(350)

    def update(self) -> None:

        # allows moving only if there is no tool being used
        if not self.tool_use_exit_timer.is_timer_active_read_only:
            self.move()

        # tool timer activation
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.tool_use_exit_timer.activate() # run a timer for the tool usage exit time
        self.tool_use_exit_timer.update()

    def render(self) -> None:
        super().render()
        self.animate()

    def animate(self):

        # can oly make the movement stuff then ther e is no tool being used
        if not self.tool_use_exit_timer.is_timer_active_read_only:
            isMoving = not (InputManager.Vertical_Axis == 0 and InputManager.Horizontal_Axis == 0)
            if isMoving:  # animacoes de cima e baixo tem pioridade sobre as laterais
                if InputManager.Horizontal_Axis == -1:
                    self.animation_controller.set_current_animation("walk_left")
                    self.last_direction_before_stop = "left"
                elif InputManager.Horizontal_Axis == 1:
                    self.animation_controller.set_current_animation("walk_right")
                    self.last_direction_before_stop = "right"
                if InputManager.Vertical_Axis == -1:
                    self.animation_controller.set_current_animation("walk_up")
                    self.last_direction_before_stop = "up"
                elif InputManager.Vertical_Axis == 1:
                    self.animation_controller.set_current_animation("walk_down")
                    self.last_direction_before_stop = "down"
            else:
                if self.last_direction_before_stop == "down":
                    self.animation_controller.set_current_animation("idle_down")
                elif self.last_direction_before_stop == "up":
                    self.animation_controller.set_current_animation("idle_up")
                elif self.last_direction_before_stop == "left":
                    self.animation_controller.set_current_animation("idle_left")
                elif self.last_direction_before_stop == "right":
                    self.animation_controller.set_current_animation("idle_right")
        # using tool
        else:
            if self.last_direction_before_stop == "down":
                self.animation_controller.set_current_animation("axe_down")
            elif self.last_direction_before_stop == "up":
                self.animation_controller.set_current_animation("axe_up")
            elif self.last_direction_before_stop == "left":
                self.animation_controller.set_current_animation("axe_left")
            elif self.last_direction_before_stop == "right":
                self.animation_controller.set_current_animation("axe_right")


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
               f"\nis a tool being used {self.tool_use_exit_timer.is_timer_active_read_only}\n" \
               f"tool timer start time {self.tool_use_exit_timer.start_time}\n"\
               f"tool timer current time {self.tool_use_exit_timer.current_time}\n" \
               f"tool timer elapsed time {self.tool_use_exit_timer.elapsed_time_read_only}\n"\
