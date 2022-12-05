import pygame
import numpy
from _1systems.game_time_system import GameTime
from _1systems.input_manager_system import InputManager
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _2components.key_tracker.key_tracker import KeyTracker
from _2components.timer.timer import Timer
from _2components.animation.animation_clip import AnimationClip
from _2components.animation.animation_controller import AnimationController
from _2components.single_sprite.single_sprite import SingleSprite
from _3gameobjs.game_obj import GameObject


class Tool(GameObject):

    def __init__(self, name: str, img_path, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.img_path = img_path
        self.single_sprite = SingleSprite(f"{self.img_path}", self)
        position_x = ScalableGameScreen.DummyScreenWidth // 2
        position_y = ScalableGameScreen.DummyScreenHeight - self.rect.height
        self.transform.move_position(pygame.Vector2(position_x, position_y))


class Player(GameObject):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        # movement related
        self.move_speed = 200
        self.normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)
        self.non_normalized_direction: pygame.Vector2 = pygame.Vector2(0, 0)

        # used everywhere
        self.is_moving = False

        # game object default sprite
        self.single_sprite = SingleSprite("_0resources/graphics/character/down_idle/0.png", self)

        # used in animations holds the last direction the player faced while walking e.g. left, up...
        self.last_direction_before_stop = "down"

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

        # TOOLS
        self.axe = Tool("axe", "_0resources/graphics/tools/axe.png", self.scene, self.scene.rendering_layer_tools)
        self.water = Tool("water", "_0resources/graphics/tools/water.png", self.scene, self.scene.rendering_layer_tools)
        self.hoe = Tool("hoe", "_0resources/graphics/tools/hoe.png", self.scene, self.scene.rendering_layer_tools)


        # TOOLS USAGE CONTROLLING SYSTEM
        # tooling player timer system
        self.is_using_tool = False
        # each tool takes a certain amount of time to its usage be computed
        self.tool_usage_timer = Timer(duration_in_ms=600, game_object_owner=self, func=self.finish_current_selected_tool_usage)
        # used just for debugging, every time a tool_usage_timer ends adds 1
        self.total_current_tool_usages = 0
        # gonna use p key to switch tools when fired
        self.tool_changer_key_tracker_p = KeyTracker(pygame.K_p, self)
        self.available_tools = [self.axe, self.water, self.hoe]
        self.current_tool_index: int = 0
        self.current_selected_tool = self.available_tools[self.current_tool_index] if len(self.available_tools) > 0 else "empty list"

        # SEEDS
        self.change_seed_key_tracker_o = KeyTracker(pygame.K_o, self)
        self.use_seed_key_tracker_ctrl = KeyTracker(pygame.K_LCTRL, self)
        self.available_seeds = ["corn", "tomato"]
        self.current_seed_index: int = 0
        self.current_selected_seed = self.available_seeds[self.current_seed_index] if len(self.available_seeds) > 0 else "empty list"
        # used just for debugging
        self.last_used_seed = "Null"

    def update_tool_menu_rendered_at_screen(self, required_tool):
        for t in self.available_tools:
            if t != required_tool:
                t.should__be_rendered = False
            else:
                t.should__be_rendered = True

    # called when the tool's timer is over, the computation of the tool effect
    def finish_current_selected_tool_usage(self):
        # what happens when the tool_exit_time
        print(f"{self.current_selected_tool} used")
        self.total_current_tool_usages += 1
        # deactivates the tool
        if self.is_using_tool:
            self.animation_controller.current_frame_index = 0
            self.is_using_tool = False

    def game_object_update(self) -> None:

        # KEYS
        # SPACE = USE TOOL (usage compute when the timer is over) | P = CHANGE TOOL
        #  L_CONTROL = PLANT SEED (when used is removed from the seeds list) | O = CHANGE SEED

        # TOOLS
        # tool timer activation Press Space to use a tool, can only use or switch between tools if the tools list is not empty
        if len(self.available_tools) > 0:
            # starts using the current selected tool if the player is not using it and activates the tool_usage_timer
            if InputManager.is_key_pressed(pygame.K_SPACE) and not self.is_using_tool:
                self.animation_controller.current_frame_index = 0
                self.is_using_tool = True
                # runs the tool_usage_timer when it ends it will execute the finish_using_current_selected_tool_round()
                # which will deactivate the timer and sel is_using_tool to False, making the timer able to run again
                self.tool_usage_timer.activate()
            # switches tool: can only switch a tool if is not using a tool at the moment
            if not self.is_using_tool and self.tool_changer_key_tracker_p.has_key_been_fired_at_this_frame:
                self.current_tool_index += 1
                if self.current_tool_index == len(self.available_tools):
                    self.current_tool_index = 0
                self.current_selected_tool = self.available_tools[self.current_tool_index]
                # resets the total_current_tool_usages of the tool when switched
                self.total_current_tool_usages = 0
            self.update_tool_menu_rendered_at_screen(self.current_selected_tool)

        # SEEDS
        # can only use or switch between seed if the seed list is not empty, switches between seed
        if len(self.available_seeds) > 0:
            # switches the current selected seed
            if self.change_seed_key_tracker_o.has_key_been_fired_at_this_frame:
                self.current_seed_index += 1
                if self.current_seed_index == len(self.available_seeds):
                    self.current_seed_index = 0
                self.current_selected_seed = self.available_seeds[self.current_seed_index]
            # uses the current selected tool and passes the current one to be the next one or "empty list" string
            if self.use_seed_key_tracker_ctrl.has_key_been_fired_at_this_frame:
                if len(self.available_seeds) > 0:
                    # REQUIRED TO SWITCH THE CURRENT SEED
                    was_at_the_first_on_the_list = False
                    if self.current_seed_index == 0:
                        was_at_the_first_on_the_list = True
                    # USED JUST FOR DEBUGGING
                    print(f"{self.current_selected_seed} used")
                    self.last_used_seed = self.current_selected_seed
                    # REMOVES THE CURRENT SEED FROM THE LIST
                    self.available_seeds.remove(self.current_selected_seed)
                    # SWITCHES THE CURRENT SEED
                    # pass the current selected one to the one before or to the 0 index
                    self.current_seed_index = self.current_seed_index - 1 if not was_at_the_first_on_the_list else 0
                    # sets the current seed or empty list is there is no more seeds
                    self.current_selected_seed = self.available_seeds[self.current_seed_index] if len(self.available_seeds) > 0 else "empty list"
                else:
                    self.current_selected_seed = "empty list"

        # MOVE
        # updates the is_moving field for the animations and its other dependencies
        self.is_moving = not (InputManager.Vertical_Axis == 0 and InputManager.Horizontal_Axis == 0) and not self.is_using_tool
        # allows moving only if there is no tool being used
        if not self.is_using_tool and self.is_moving:
            self.move_player()
        else:
            self.kill_player_directions()

        # ANIMATES THE PLAYER
        self.animate_player()

    def animate_player(self):
        # can oly make the movement stuff then there is no tool being used
        if self.is_using_tool:
            # using tool: simply concatenates the tool name, it will be the same as the clip folders names
            if self.last_direction_before_stop == "down":
                self.animation_controller.set_current_animation(self.available_tools[self.current_tool_index].name + "_down")
            elif self.last_direction_before_stop == "up":
                self.animation_controller.set_current_animation(self.available_tools[self.current_tool_index].name + "_up")
            elif self.last_direction_before_stop == "left":
                self.animation_controller.set_current_animation(self.available_tools[self.current_tool_index].name + "_left")
            elif self.last_direction_before_stop == "right":
                self.animation_controller.set_current_animation(self.available_tools[self.current_tool_index].name + "_right")
        else:
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
        if numpy.linalg.norm(self.non_normalized_direction) != 0:
            self.normalized_direction = self.non_normalized_direction / numpy.linalg.norm(self.non_normalized_direction)
        else:
            self.normalized_direction = pygame.Vector2(0, 0)
        # creates a new position with the new direction
        new_position: pygame.Vector2 = self.transform.position
        new_position.x += self.normalized_direction.x * self.move_speed * GameTime.DeltaTime
        new_position.y += self.normalized_direction.y * self.move_speed * GameTime.DeltaTime
        self.transform.move_position(new_position)

    def kill_player_directions(self):
        self.normalized_direction = pygame.Vector2(0, 0)
        self.non_normalized_direction = pygame.Vector2(0, 0)

    def get_inspector_debugging_status(self) -> str:
        return super().get_inspector_debugging_status() + \
               f"PLAYER SELF IMPLEMENTED DEBUGGING STATS\n" \
               f"speed: {self.move_speed}\n" \
               f"normalized direction: {self.normalized_direction}\n" \
               f"normalized direction magnitude: {numpy.linalg.norm(self.normalized_direction)}\n" \
               f"non-normalized direction: {self.non_normalized_direction}\n" \
               f"non-normalized direction magnitude: {numpy.linalg.norm(self.non_normalized_direction)}\n" \
               f"\n" \
               f"available tools: {self.available_tools}\n" \
               f"current set tool: {self.current_selected_tool} index({self.current_tool_index})\n" \
               f"total usages computed: {self.total_current_tool_usages}\n" \
               f"is using tool: {self.is_using_tool}\n" \
               f"is tool use exit timer active: {self.tool_usage_timer.is_timer_active_read_only}\n" \
               f"\n" \
               f"available seeds: {self.available_seeds}\n" \
               f"current seed: {self.current_selected_seed} index({self.current_seed_index})\n" \
               f"last used seed: {self.last_used_seed}" \
