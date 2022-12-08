import pygame
from JNetoProductions_pygame_game_engine.systems.game_time_system import GameTime
from JNetoProductions_pygame_game_engine.systems.input_manager_system import InputManager
from JNetoProductions_pygame_game_engine.components.collider.collider import Collider
from JNetoProductions_pygame_game_engine.components.animation.animation_clip import AnimationClip
from JNetoProductions_pygame_game_engine.components.animation.animation_controller import AnimationController
from JNetoProductions_pygame_game_engine.components.single_sprite.single_sprite import SingleSprite
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject


class Player(GameObject):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        # movement related
        self.move_speed = 200
        self.normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.non_normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)

        # used everywhere
        self.is_moving = False

        # game_loop object default sprite
        self.single_sprite = SingleSprite("our_game/game_res/graphics/character/down_idle/0.png", self)

        # collider
        self.collider = Collider(0, 30, 50, 20, self)

        # used in animations holds the last direction the player faced while walking e.g. left, up...
        self.last_direction_before_stop = "down"

        # animations and controller
        self.animation_walk_down = AnimationClip("walk_down", 4, "our_game/game_res/graphics/player/down")
        self.animation_walk_right = AnimationClip("walk_right", 4, "our_game/game_res/graphics/player/right")
        self.animation_walk_up = AnimationClip("walk_up", 4, "our_game/game_res/graphics/player/up")
        self.animation_walk_left = AnimationClip("walk_left", 4, "our_game/game_res/graphics/player/left")
        self.animation_idle_down = AnimationClip("idle_down", 4, "our_game/game_res/graphics/character/down_idle")
        self.animation_idle_right = AnimationClip("idle_right", 4, "our_game/game_res/graphics/character/right_idle")
        self.animation_idle_up = AnimationClip("idle_up", 4, "our_game/game_res/graphics/character/up_idle")
        self.animation_idle_left = AnimationClip("idle_left", 4, "our_game/game_res/graphics/character/left_idle")
        # tools animations

        # putting clips in a list
        animation_clips = [self.animation_walk_right, self.animation_walk_up, self.animation_walk_left,
                           self.animation_walk_down, self.animation_idle_right, self.animation_idle_up,
                           self.animation_idle_left, self.animation_idle_down]
        # animation controller
        self.animation_controller = AnimationController(animation_clips, self)

    def game_object_update(self) -> None:
        # MOVE
        # updates the is_moving field for the animations and its other dependencies
        self.is_moving = not (InputManager.Vertical_Axis == 0 and InputManager.Horizontal_Axis == 0)

        if self.is_moving:
            self.move_player()
        else:
            self.kill_player_directions()

        # ANIMATES THE PLAYER
        self.animate_player()

    def animate_player(self):
        # moving animation
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
        # idle animation
        else:
            if self.last_direction_before_stop == "down":
                self.animation_controller.set_current_animation("idle_down")
            elif self.last_direction_before_stop == "up":
                self.animation_controller.set_current_animation("idle_up")
            elif self.last_direction_before_stop == "left":
                self.animation_controller.set_current_animation("idle_left")
            elif self.last_direction_before_stop == "right":
                self.animation_controller.set_current_animation("idle_right")

    def move_player(self) -> None:
        # generates a direction based on players input
        self.non_normalized_direction = pygame.Vector2(InputManager.Horizontal_Axis, InputManager.Vertical_Axis)
        # normalizes the direction, but checks before if the Magnitude is not 0, otherwise it will launch an exception
        if self.non_normalized_direction.magnitude() != 0:
            # .norm = magnitude n quer dizer normalizado, python é estranho
            # vetor normalizado = vetor/magnitude
            self.normalized_direction = self.non_normalized_direction / self.non_normalized_direction.magnitude()
        else:
            self.normalized_direction = pygame.Vector2(0, 0)
        # creates a new world_position with the new direction
        new_position: pygame.Vector2 = self.transform.world_position.copy()
        new_position.x += self.normalized_direction.x * self.move_speed * GameTime.DeltaTime
        new_position.y += self.normalized_direction.y * self.move_speed * GameTime.DeltaTime
        self.transform.move_world_position_with_collisions_calculations(new_position)

    def kill_player_directions(self):
        self.normalized_direction = pygame.Vector2(0, 0)
        self.non_normalized_direction = pygame.Vector2(0, 0)

    def get_inspector_debugging_status(self) -> str:
        return super().get_inspector_debugging_status() + \
               f"PLAYER SELF IMPLEMENTED DEBUGGING STATS\n" \
               f"speed: {self.move_speed}\n" \
               f"normalized direction: {self.normalized_direction}\n" \
               f"normalized direction magnitude: {self.normalized_direction.magnitude()}\n" \
               f"non-normalized direction: {self.non_normalized_direction}\n" \
               f"non-normalized direction magnitude: {self.non_normalized_direction.magnitude()}\n" \
               f"\n" \
