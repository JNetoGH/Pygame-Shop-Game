import pygame

from JNetoProductions_pygame_game_engine.components.single_sprite_component import SingleSpriteComponent
from JNetoProductions_pygame_game_engine.components.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject


class InventoryItem(GameObject):

    def __init__(self, name, price, initial_amount, img_path, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.name = name
        self.price = price
        self.amount = initial_amount
        self.single_sprite = SingleSpriteComponent(img_path, self)
        self.single_sprite.scale_itself(2)
        self.amount_text_render = TextRenderComponent(f"{self.amount}", 15, pygame.Color(0,0,0), 15, 13, self)

    def game_object_update(self) -> None:
        # updates their amount each frame
        self.amount_text_render.change_text(f"{self.amount}")

    def add_amount(self, quantity):
        if quantity <= 0:
            return
        self.amount += quantity

    def remove_amount(self, quantity):
        if quantity <= 0:
            return
        if self.amount - quantity < 0:
            return
        self.amount -= quantity

    def to_string(self) -> str:
        return f"name: {self.name}\n" \
               f"amount: {self.amount}\n" \
               f"price: {self.price}\n"
