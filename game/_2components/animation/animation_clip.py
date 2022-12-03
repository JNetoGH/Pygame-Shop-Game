from os import walk   # allow us to walk through folders
import pygame


# it's basically a list of images
class AnimationClip:

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

