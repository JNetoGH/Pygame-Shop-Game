import pygame
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _1systems.text_rendering_system import TextRender
from _2components.transform.transform import Transform
from abc import abstractmethod


class GameObject(pygame.sprite.Sprite):

    def __init__(self, name: str, scene, rendering_layer, should_be_rendered: bool = True):
        super().__init__()

        # yes, because why not?
        self.name = name

        # in case False the Camera won't render this GameObject
        self.should__be_rendered: bool = True

        # when a component is instantiated, it is automatically stored here
        self.components_list = []

        # holds the scene that the game object is part of, and adds itself in it
        self.scene = scene
        scene.all_game_obj.append(self)

        # sets the transform
        # every game object in JNeto Production Game Engine must have a Transform
        self.transform = Transform(self)

        # sets the rendering layer, and adds itself to it
        self.rendering_layer = rendering_layer
        self.rendering_layer.add_game_object(self)

        # makes a default img to the object, it's just a rectangle filled with some color
        # sprites or animation override it
        self.image = pygame.Surface((64, 32))
        self.image.fill((255, 255, 255))

        # - The rectangle that holds the game object's image
        # - The center pos of the image_rect (a.k.a. screen position) is the same of the gm obj pos by default
        #   therefore, the at the start of the GameObject it's screen position is the same of its world position
        # - This rect is mostly used to hold the game object screen position (not world position)
        #   so it's quite essential
        self.image_rect = self.image.get_rect(center=self.transform.world_position)

    def get_index_in_scene_all_game_objects_list(self) -> int:
        for i in range(0, len(self.scene.all_game_obj)):
            if self.scene.all_game_obj[i] == self:
                return i
        return -1

    def get_this_game_object_rendering_layer_index_in_scene_rendering_layers_list(self) -> int:
        for i in range(0, len(self.scene.rendering_layers)):
            if self.scene.rendering_layers[i] == self.rendering_layer:
                return i
        return -1

    # pygame is stupid and has already an update method for sprites(a.k.a game obj super class)
    # so I had to call it this way
    @abstractmethod
    def game_object_update(self) -> None:
        pass

    def get_this_game_object_components_list_as_string(self):
        components_names = ""
        counter = 0
        max_comp_name_per_line = 3
        for component in self.components_list:
            counter += 1
            components_names += type(component).__name__ + ", "
            if counter == max_comp_name_per_line:
                components_names += "\n"
                counter = 0
        components_names = components_names[:-1]
        components_names = components_names[:-1]
        return components_names

    # it's meant to be overridden with a super().get_inspector_debugging_status() call in it
    def get_inspector_debugging_status(self) -> str:

        components_names = self.get_this_game_object_components_list_as_string()

        components_inspector_debugging_status = ""
        for component in self.components_list:
            components_inspector_debugging_status += component.get_inspector_debugging_status() + "\n"

        return f"GAME OBJECT INSPECTOR \n" \
               f"game object name: {self.name}\n" \
               f"class name: {type(self)} \n" \
               f"should be rendered: {self.should__be_rendered}\n" \
               f"index in scene game objects list: {self.get_index_in_scene_all_game_objects_list()}\n" \
               f"rendering layer index: {self.get_this_game_object_rendering_layer_index_in_scene_rendering_layers_list()}\n" \
               f"components: [{components_names}]\n\n" \
               f"{components_inspector_debugging_status}"

    # DO NOT TOUCH AND DO NOT OVERRIDE! IT'S USED BY THE InspectorDebuggingCanvas IN ORDER TO RENDER THE GAME OBJECT'S GIZMOS
    def game_object_debug_late_render_gizmos(self) -> None:

        font_size = 15
        font = pygame.font.Font('_0resources/fonts/JetBrainsMono-Medium.ttf', font_size)  # create a text surface object,
        description_spacing_x = 30
        description_spacing_y = 30

        object_screen_pos = self.transform.screen_position_read_only

        # IMAGE RECT GIZMOS
        pygame.draw.rect(ScalableGameScreen.GameScreenDummySurface, "red", self.image_rect, 1)
        # description
        text_img_rect = "self.image.image_rect"
        # render
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth, text_img_rect,
                             (object_screen_pos[0] - self.image_rect.width // 2, object_screen_pos[1] - self.image_rect.height // 2 - font_size - 5),
                             font, color=pygame.Color("red"))

        # TRANSFORM GIZMOS
        transform_color = "black"
        pygame.draw.circle(ScalableGameScreen.GameScreenDummySurface, transform_color, object_screen_pos, 5)
        # description
        text_transform = f"{self.name}'s Transform.world_position\n(x:{self.transform.world_position.x} | y:{self.transform.world_position.y})\n" \
                         f"{self.name}'s Transform.screen_position\n(x:{self.transform.screen_position_read_only.x} | y:{self.transform.screen_position_read_only.y})"
        # render
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth, text_transform,
                             (object_screen_pos[0] + description_spacing_x, object_screen_pos[1] - font_size // 2 - description_spacing_y),
                             font, color=pygame.Color(transform_color))

        # THE DEBUGGING STATS IS ALSO GOING TO APPEAR AS GIZMOS
        components_names = self.get_this_game_object_components_list_as_string()
        # description
        game_object_stats_text =\
               f"GAME OBJECT INSPECTOR \n" \
               f"\ngame object name: {self.name}\n" \
               f"class name: {type(self)} \n" \
               f"should be rendered: {self.should__be_rendered}\n" \
               f"index in scene game objects list: {self.get_index_in_scene_all_game_objects_list()}\n" \
               f"rendering layer index: {self.get_this_game_object_rendering_layer_index_in_scene_rendering_layers_list()}\n" \
               f"\ncomponents:\n[{components_names}]\n\n"
        # render
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth, game_object_stats_text,
                             (object_screen_pos[0] - self.image_rect.width // 2,
                              object_screen_pos[1] + self.image_rect.height // 2 + description_spacing_y),
                             font, color=pygame.Color("black"))