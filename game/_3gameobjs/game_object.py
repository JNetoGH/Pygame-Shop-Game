import pygame
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _1systems.text_rendering_system import TextRender
from _2components.transform.transform import Transform
from abc import abstractmethod


class GameObject(pygame.sprite.Sprite):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__()
        self.name = name
        self.should__be_rendered: bool = True
        # when a component is instantiated, it is automatically stored here
        self.components_list = []
        self.scene = scene
        # sets the transform
        self.transform = Transform(self)
        # sets the rendering layer
        self.rendering_layer = rendering_layer
        self.rendering_layer.add_game_object(self)
        # makes a default img to the object
        self.image = pygame.Surface((64, 32))
        self.image.fill((255, 255, 255))
        # - The rectangle that holds the game object's image
        # - The center pos of the image_rect is the same of the gm obj pos by default, but needs to be set back to the
        #   object pos at every movement, it's automatically made by the transform bia the move_position method
        self.image_rect = self.image.get_rect(center=self.transform.position)
        # adds itself to the scene game object list
        scene.all_game_obj.append(self)

    def get_index_in_scene_all_game_objects_list(self) -> int:
        for i in range(0, len(self.scene.all_game_obj)):
            if self.scene.all_game_obj[i] == self:
                return i
        return -1

    def get_this_game_object_rendering_layer_index_in_scene(self) -> int:
        for i in range(0, len(self.scene.rendering_layers)):
            if self.scene.rendering_layers[i] == self.rendering_layer:
                return i
        return -1

    # pygame is stupid and has already an update method for sprites(a.k.a game obj super class)
    # so I had to call it this way
    @abstractmethod
    def game_object_update(self) -> None:
        pass

    # it's meant to be overridden with a super().get_inspector_debugging_status() call in it
    def get_inspector_debugging_status(self) -> str:
        components_names = ""
        for component in self.components_list:
            components_names += type(component).__name__ + ", "
        components_names = components_names[:-1]
        components_names = components_names[:-1]
        components_inspector_debugging_status = ""
        for component in self.components_list:
            components_inspector_debugging_status += component.get_inspector_debugging_status() + "\n"
        return f"GAME OBJECT INSPECTOR \n" \
               f"game object name: {self.name}\n" \
               f"class name: {type(self)} \n" \
               f"should be rendered: {self.should__be_rendered}\n" \
               f"index in scene game objects list: {self.get_index_in_scene_all_game_objects_list()}\n" \
               f"rendering layer index: {self.get_this_game_object_rendering_layer_index_in_scene()}\n" \
               f"components: [{components_names}]\n\n" \
               f"{components_inspector_debugging_status}"

    # DO NOT TOUCH AND DO NOT OVERRIDE! IT'S USED BY THE InspectorDebuggingCanvas IN ORDER TO RENDER THE GAME OBJECT'S GIZMOS
    def game_object_debug_late_render_gizmos(self) -> None:

        font_size = 15
        font = pygame.font.Font('_0resources/fonts/JetBrainsMono-Medium.ttf', font_size)  # create a text surface object,
        description_spacing_x = 20
        description_spacing_y = 10

        # IMAGE RECT GIZMOS
        pygame.draw.rect(ScalableGameScreen.GameScreenDummySurface, "red", self.image_rect, 1)
        # description
        text_img_rect = "self.image.image_rect"
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth, text_img_rect,
                             (self.transform.position.x + self.image_rect.width // 2 + description_spacing_x, self.transform.position.y + self.image_rect.height // 2 - font_size),
                             font, color=pygame.Color("red"))

        # TRANSFORM GIZMOS
        pygame.draw.circle(ScalableGameScreen.GameScreenDummySurface, "cyan", self.transform.position, 5)
        # description
        text_transform = f"({self.name})Transform.position (x:{self.transform.position.x} | y:{self.transform.position.y})"
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth, text_transform,
                             (self.transform.position.x + description_spacing_x, self.transform.position.y - font_size//2),
                             font, color=pygame.Color("cyan"))

        # THE DEBUGGING STATS IS ALSO GOING TO APPEAR AS GIZMOS
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
        game_object_stats_text =\
               f"GAME OBJECT INSPECTOR \n" \
               f"\ngame object name: {self.name}\n" \
               f"class name: {type(self)} \n" \
               f"should be rendered: {self.should__be_rendered}\n" \
               f"index in scene game objects list: {self.get_index_in_scene_all_game_objects_list()}\n" \
               f"rendering layer index: {self.get_this_game_object_rendering_layer_index_in_scene()}\n" \
               f"\ncomponents:\n[{components_names}]\n\n"
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.DummyScreenWidth, game_object_stats_text,
                             (self.transform.position.x - self.image_rect.width // 2, self.transform.position.y + self.image_rect.height // 2 + description_spacing_y),
                             font, color=pygame.Color("black"))
