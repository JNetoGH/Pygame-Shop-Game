import pygame
import numpy

from _1systems.game_time_system import GameTime
from _1systems.input_manager_system import InputManager
from _2components.key_tracker.key_tracker import KeyTracker
from _2components.timer.timer import Timer
from _2components.animation.animation_clip import AnimationClip
from _2components.animation.animation_controller import AnimationController
from _2components.single_sprite.single_sprite import SingleSprite
from _3gameobjs.game_obj import GameObject


class Player(GameObject):

    def __init__(self, name: str, scene):
        super().__init__(name, scene)

        # movement related
        self.move_speed = 200
        self.normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.non_normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)

        # used everywhere
        self.is_moving = False

        # game object default sprite
        self.single_sprite = SingleSprite("_0resources/graphics/character/down_idle/0.png", self)

        # used in animations holds the last direction the player faced while walking e.g. left, up...
        self.last_direction_before_stop = ""

        # animations and controller
        self.animation_walk_down = AnimationClip("walk_down", 4, "_0resources/graphics/character/down_walk")
        self.animation_walk_right = AnimationClip("walk_right", 4, "_0resources/graphics/character/right_walk")
        self.animation_walk_up = AnimationClip("walk_up", 4, "_0resources/graphics/character/up_walk")
        self.animation_walk_left = AnimationClip("walk_left", 4, "_0resources/graphics/character/left_walk")
        self.animation_idle_down = AnimationClip("idle_down", 4, "_0resources/graphics/character/down_idle")
        self.animation_idle_right = AnimationClip("idle_right", 4, "_0resources/graphics/character/right_idle")
        self.animation_idle_up = AnimationClip("idle_up", 4, "_0resources/graphics/character/up_idle")
        self.animation_idle_left = AnimationClip("idle_left", 4, "_0resources/graphics/character/left_idle")
        # tools animations
        self.animation_axe_down = AnimationClip("axe_down", 3, "_0resources/graphics/character/down_axe")
        self.animation_axe_right = AnimationClip("axe_right", 3, "_0resources/graphics/character/right_axe")
        self.animation_axe_up = AnimationClip("axe_up", 3, "_0resources/graphics/character/up_axe")
        self.animation_axe_left = AnimationClip("axe_left", 3, "_0resources/graphics/character/left_axe")
        self.animation_hoe_down = AnimationClip("hoe_down", 3, "_0resources/graphics/character/down_hoe")
        self.animation_hoe_right = AnimationClip("hoe_right", 3, "_0resources/graphics/character/right_hoe")
        self.animation_hoe_up = AnimationClip("hoe_up", 3, "_0resources/graphics/character/up_hoe")
        self.animation_hoe_left = AnimationClip("hoe_left", 3, "_0resources/graphics/character/left_hoe")
        self.animation_water_down = AnimationClip("water_down", 3, "_0resources/graphics/character/down_water")
        self.animation_water_right = AnimationClip("water_right", 3, "_0resources/graphics/character/right_water")
        self.animation_water_up = AnimationClip("water_up", 3, "_0resources/graphics/character/up_water")
        self.animation_water_left = AnimationClip("water_left", 3, "_0resources/graphics/character/left_water")
        # putting clips in a list
        animation_clips = [self.animation_walk_right, self.animation_walk_up, self.animation_walk_left,
                           self.animation_walk_down, self.animation_idle_right, self.animation_idle_up,
                           self.animation_idle_left, self.animation_idle_down, self.animation_axe_up,
                           self.animation_axe_down, self.animation_axe_left, self.animation_axe_right,
                           self.animation_hoe_up, self.animation_hoe_down, self.animation_hoe_left,
                           self.animation_hoe_right, self.animation_water_up, self.animation_water_down,
                           self.animation_water_left, self.animation_water_right]
        # animation controller
        self.animation_controller = AnimationController(animation_clips, self)

        # tooling player timer system
        self.is_using_tool = False
        self.tool_use_exit_timer = Timer(600, self)
        # gonna use p key to switch tools when fired
        self.key_tracker_p = KeyTracker(pygame.K_p, self)
        self.available_tools = ["axe", "water", "hoe"]
        self.current_tool_index = 0
        self.selected_tool = self.available_tools[self.current_tool_index]

        # seeds
        self.available_seeds = ["corn", "tomato"]
        self.current_seed_index = 0
        self.selected_seed = self.available_seeds[self.current_seed_index]

    def update(self) -> None:

        # UPDATES IS MOVING FIELD
        self.is_moving = not (InputManager.Vertical_Axis == 0 and InputManager.Horizontal_Axis == 0) and not self.is_using_tool

        # TOOLS
        # tool timer activation Press Space to use a tool
        if InputManager.is_key_pressed(pygame.K_SPACE):
            if not self.is_using_tool:
                self.animation_controller.current_frame_index = 0
                self.is_using_tool = True
                # run a timer for the tool usage exit time_system
                self.tool_use_exit_timer.activate()
        # deactivates the tool
        if not self.tool_use_exit_timer.is_timer_active_read_only:
            if self.is_using_tool:
                self.animation_controller.current_frame_index = 0
                self.is_using_tool = False
        # switches tool: can only switch a tool if is not using a tool at the moment
        if not self.is_using_tool:
            if self.key_tracker_p.has_key_been_fired_at_this_frame:
                self.current_tool_index += 1
                if self.current_tool_index == len(self.available_tools):
                    self.current_tool_index = 0

        # MOVE
        # allows moving only if there is no tool being used
        if not self.is_using_tool and self.is_moving:
            self.move_player()

    def render(self) -> None:
        super().render()
        self.animate_player()

    def animate_player(self):
        # can oly make the movement stuff then ther e is no tool being used
        if not self.is_using_tool:
            if self.is_moving:
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
        # using tool: simply concatenates the tool name, it will be the same as the clip folders names
        else:
            if self.last_direction_before_stop == "down":
                self.animation_controller.set_current_animation(self.available_tools[self.current_tool_index] + "_down")
            elif self.last_direction_before_stop == "up":
                self.animation_controller.set_current_animation(self.available_tools[self.current_tool_index] + "_up")
            elif self.last_direction_before_stop == "left":
                self.animation_controller.set_current_animation(self.available_tools[self.current_tool_index] + "_left")
            elif self.last_direction_before_stop == "right":
                self.animation_controller.set_current_animation(self.available_tools[self.current_tool_index] + "_right")

    def move_player(self) -> None:
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
               f"PLAYER SELF IMPLEMENTED DEBUGGING STATS\n" \
               f"speed: {self.move_speed}\n" \
               f"normalized direction: {self.normalized_direction}\n" \
               f"normalized direction magnitude: {numpy.linalg.norm(self.normalized_direction)}\n" \
               f"non-normalized direction: {self.non_normalized_direction}\n" \
               f"non-normalized direction magnitude: {numpy.linalg.norm(self.non_normalized_direction)}\n" \
               f"current set tool: {self.available_tools[self.current_tool_index]}\n" \
               f"is using tool: {self.is_using_tool}\n" \
               f"is tool use exit timer active: {self.tool_use_exit_timer.is_timer_active_read_only}\n" \

