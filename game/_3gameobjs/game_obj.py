import pygame
from _1systems.scalable_game_screen_system import ScalableGameScreen
from _1systems.text_rendering_system import TextRender
from _2components.transform.transform import Transform
from abc import abstractmethod





class GameObject(pygame.sprite.Sprite):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__()
        self.name = name
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
        # - The center pos of the rect is the same of the gm obj pos by default, but needs to be set back to the
        #   object pos at every movement, it's automatically made by the transform bia the move_position method
        self.rect = self.image.get_rect(center=self.transform.position)
        # adds itself to the scene game object list
        scene.all_game_obj.append(self)
        # calls its start() method
        self.game_object_start()

    def get_index_in_scene_all_game_objects_list(self) -> int:
        for i in range(0, len(self.scene.all_game_obj)):
            if self.scene.all_game_obj[i] == self:
                return i

    @abstractmethod
    def game_object_start(self) -> None:
        pass

    # pygame is stupid and has already an update method for sprites(a.k.a game obj super class)
    # so I had to call it this way
    @abstractmethod
    def game_object_update(self) -> None:
        pass

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
               f"index in scene game objects list: {self.get_index_in_scene_all_game_objects_list()}\n" \
               f"components: [{components_names}]\n\n" \
               f"{components_inspector_debugging_status}"

    # DO NOT TOUCH AND DO NOT OVERRIDE! IT'S USED BY THE RENDERING_LAYER IN ORDER TO RENDER THE GAME OBJECT
    def game_object_render(self) -> None:

        # re-centers the image sprite rect to the new possible position
        self.rect = self.image.get_rect(center=self.transform.position)

        # - draws the game object image on the dummy screen
        # - the subtractions are need in order to displaye the image correctly because, by default it's shown at
        #   the corner like:
        """
            |-------|
            |       | = rect
            |-------|
                     IMAGE
        """
        image_x = self.transform.position.x - self.rect.width // 2
        image_y = self.transform.position.y - self.rect.height // 2
        ScalableGameScreen.GameScreenDummySurface.blit(self.image, (image_x, image_y))

    # DO NOT TOUCH AND DO NOT OVERRIDE! IT'S USED BY THE RENDERING_LAYER IN ORDER TO RENDER THE GAME OBJECT'S GIZMOS
    def game_object_debug_late_render_gizmos(self) -> None:

        font_size = 15
        font = pygame.font.Font('_0resources/fonts/JetBrainsMono-Medium.ttf', font_size)  # create a text surface object,
        description_spacing_x = 20
        description_spacing_y = 10

        # IMAGE RECT GIZMOS
        pygame.draw.rect(ScalableGameScreen.GameScreenDummySurface, "red", self.rect, 1)
        # descriprion
        text_img_rect = "self.image.rect"
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface,
                             ScalableGameScreen.GameScreenDummySurface.get_width(),  ScalableGameScreen.GameScreenDummySurface.get_height(),
                             text_img_rect , (self.transform.position.x + self.rect.width//2 + description_spacing_x, self.transform.position.y+self.rect.height//2-font_size),
                             font, color=pygame.Color("red"))

        # TRANSFORM GIZMOS
        pygame.draw.circle(ScalableGameScreen.GameScreenDummySurface, "black", self.transform.position, 5)
        # description
        text_transform = f"Transform.position (x:{self.transform.position.x} | y:{self.transform.position.y})"
        TextRender.blit_text(ScalableGameScreen.GameScreenDummySurface,
                             ScalableGameScreen.GameScreenDummySurface.get_width(),  ScalableGameScreen.GameScreenDummySurface.get_height(),
                             text_transform, (self.transform.position.x + description_spacing_x, self.transform.position.y - font_size//2),
                             font, color=pygame.Color("black"))