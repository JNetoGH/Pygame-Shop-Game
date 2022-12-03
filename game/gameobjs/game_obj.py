import pygame


class GameObject(pygame.sprite.Sprite):

    def __init__(self, pos: pygame.math.Vector2, group, level):
        super().__init__(group)
        self.level = level
        self.position: pygame.math.Vector2 = pos
        # adds itself to the level game object list
        level.all_game_obj.append(self)
        # calls its start() method
        self.start()

    def get_index_in_level_list(self) -> int:
        for i in range(0, len(self.level.all_game_obj)):
            if self.level.all_game_obj[i] == self:
                return i

    def start(self) -> None:
        pass

    def tick(self) -> None:
        pass

    def render(self) -> None:
        pass

