from abc import abstractmethod


class Component:

    def __init__(self, game_object_owner):
        self._game_object_owner = game_object_owner
        self._game_object_owner.components_list.append(self)

    @property
    def game_object_owner_read_only(self):
        return self._game_object_owner

    def update(self):
        pass

    @abstractmethod
    def get_inspector_debugging_status(self) -> str:
        pass
