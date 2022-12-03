import pygame
import numpy
from gameobjs.game_obj import GameObject
from systems.input_manager import InputManager

#  allows us to walk through folders
from os import walk


# it's basically a list of images
class Animation:

    def __init__(self, name: str, folder_path: str):
        self.name = name
        self.images = []
        self.import_images_from_folder(folder_path)

    # imports every image inside a folder
    def import_images_from_folder(self, folder_path) -> None:
        surface_list = []
        print("importing ", end="")
        for folder_name, sub_folder, img_files_list in walk(folder_path):
            print(f"{folder_name} => {img_files_list}:")
            for img_name in img_files_list:
                img_path = folder_path + "/" + img_name
                print(f"{img_path}")
                img_surface = pygame.image.load(img_path).convert_alpha()
                surface_list.append(img_surface)
            print()
        for img in surface_list:
            self.images.append(img)

    def add_unitary_and_manually(self, image_path) -> None:
        image_surface = pygame.image.load(image_path).convert_alpha()
        self.images.append(image_surface)


class AnimationController:
    pass


class Player(GameObject):
    def __init__(self, position: pygame.math.Vector2, group, level):
        super().__init__(position, group, level)

        # movement related
        self.non_normalized_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.normalized_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.speed = 200

        # sprites
        # a dictionary that holds all sprites of this GameObject as a list for each position
        self.animations_dictionary = self.import_sprites_as_dictionary()
        self.animation_status = "down"  # the key to a animation list in the dictionary
        self.current_frame_index = 0  # the current img of the list of the dictionary
        self.animation_speed = 4

        # the image itself
        self.image = self.animations_dictionary[self.animation_status][self.current_frame_index]

        # the rectangle that represent the game object: the center pos of the rect is the same of the player pos
        self.rect = self.image.get_rect(center=self.position)




    def start(self) -> None:
        print("oi")

    def tick(self) -> None:
        self.move()

    def move(self):
        # generates a new move direction and normalizes it
        self.normalized_direction = pygame.math.Vector2(0, 0)
        self.non_normalized_direction = pygame.math.Vector2(InputManager.Horizontal_Axis, InputManager.Vertical_Axis)
        # avoids division by 0 exception: extracts the MAGNITUDE of the non-normalized direction
        if numpy.linalg.norm(self.non_normalized_direction) != 0:
            # normalizes the new direction
            self.normalized_direction = self.non_normalized_direction / numpy.linalg.norm(self.non_normalized_direction)

        # moves frame-rate independent
        self.position.x += self.normalized_direction.x * self.speed * self.level.game.delta_time
        self.position.y += self.normalized_direction.y * self.speed * self.level.game.delta_time
        self.rect.center = self.position  # updates the rect position

    def render(self) -> None:
        self.animate()

        
    # ANIMATE
    def animate(self):
        # jump from frame to frame
        self.current_frame_index += self.animation_speed * self.level.game.delta_time
        # sets back to the first frame if it's bigger than the size of the animation
        if self.current_frame_index >= len(self.animations_dictionary[self.animation_status]):
            self.current_frame_index = 0
        self.image = self.animations_dictionary[self.animation_status][int(self.current_frame_index)]


    # ANIMATION SPRITES DITIONARY
    def import_sprites_as_dictionary(self):
        animations_dictionary = {
                        "up": [],       "down": [],       "left": [],       "right": [],
                        "up_idle": [],  "down_idle": [],  "left_idle": [],  "right_idle": [],
                        "up_hoe": [],   "down_hoe": [],   "left_hoe": [],   "right_hoe": [],
                        "up_axe": [],   "down_axe": [],   "left_axe": [],   "right_axe": [],
                        "up_water": [], "down_water": [], "left_water": [], "right_water": []
                     }

        # adds the images to the dictionaries lists, searching for a folder with its key name
        for animation_folder_name in animations_dictionary.keys():
            path = "resources/graphics/character/" + animation_folder_name
            animations_dictionary[animation_folder_name] = self.import_imgs_from_folder(path)

        return animations_dictionary

    # imports every image inside a folder
    def import_imgs_from_folder(self, path):
        surface_list = []

        print("importing ", end="")
        for folder_name, sub_folder, img_files_list in walk(path):
            print(f"{folder_name} => {img_files_list}:")
            for img_name in img_files_list:
                img_path = path + "/" + img_name
                print(f"{img_path}")
                img_surface = pygame.image.load(img_path).convert_alpha()
                surface_list.append(img_surface)
            print()

        return surface_list


    def get_status(self) -> str:
        return f"Index in Level list = {self.get_index_in_level_list()}\n" \
               f"Speed: {self.speed}\n" \
               f"Position: {self.position}\n" \
               f"Normalized Direction: {self.normalized_direction}, magnitude={numpy.linalg.norm(self.normalized_direction)}\n" \
               f"Non-Normalized Direction: {self.non_normalized_direction}, magnitude={numpy.linalg.norm(self.non_normalized_direction)}"


