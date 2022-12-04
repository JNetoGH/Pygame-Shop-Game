from abc import abstractmethod

class Component:

    def __init__(self, game_object_owner):
        self.game_object_owner = game_object_owner
        self.game_object_owner.components_list.append(self)

    @abstractmethod
    def get_inspector_debugging_status(self) -> str:
        pass