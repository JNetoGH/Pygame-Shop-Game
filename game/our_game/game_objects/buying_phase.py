import pygame

from JNetoProductions_pygame_game_engine.components.key_tracker.key_tracker import KeyTracker
from JNetoProductions_pygame_game_engine.components.text_render.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from our_game.game_objects.player import Player, ResInventory, Resource


class MiddleBlock(GameObject):
    pass


class BuyingPhase(GameObject):

    def __init__(self, name: str, player, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.image = pygame.Surface((0, 0))
        self.text_render = TextRenderComponent("BUYING PHASE", 60, pygame.Color(255, 255, 255), 0, 0, self)

        self.fixed_position_on_screen = pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth,
                                                       ScalableGameScreen.HalfDummyScreenHeight)
        self.fix_game_object_on_screen(self.fixed_position_on_screen)

        self.key_tracker_arrow_left = KeyTracker(pygame.K_LEFT, self)
        self.key_tracker_arrow_right = KeyTracker(pygame.K_RIGHT, self)
        self.key_tracker_arrow_up = KeyTracker(pygame.K_UP, self)
        self.key_tracker_arrow_down = KeyTracker(pygame.K_DOWN, self)
        self.key_tracker_enter = KeyTracker(pygame.K_RETURN, self)
        self.key_tracker_k = KeyTracker(pygame.K_k, self)

        self.current_item_index = 0
        self.purchase_amount = 1

        self.max_allowed_amount_for_purchase = 100

        self.player = player
        self.is_running = False

    def run_phase(self):
        self.is_running = True
        self.current_item_index = 0
        self.purchase_amount = 1

    def stop_phase(self):
        self.is_running = False

    def game_object_update(self) -> None:
        if self.is_running:

            current_item: Resource = self.player.res_inventory.resources[self.current_item_index]
            purchase_value: float = current_item.price * self.purchase_amount
            has_enough_money = self.player.money >= purchase_value

            print(f"available money: {self.player.money}")
            print(f"has enough money: {has_enough_money}")
            print(f"{current_item.name}")
            print(f"amount: {self.purchase_amount}")
            print(f"price: {purchase_value}\n")

            # switch between resources
            if self.key_tracker_arrow_right.has_key_been_fired_at_this_frame:
                if not self.current_item_index == len(self.player.res_inventory.resources)-1:
                    self.current_item_index += 1
                    self.purchase_amount = 1
            elif self.key_tracker_arrow_left.has_key_been_fired_at_this_frame:
                if not self.current_item_index <= 0:
                    self.current_item_index -= 1
                    self.purchase_amount = 1

            # increase the amount for purchase
            elif self.key_tracker_arrow_up.has_key_been_fired_at_this_frame:
                if not self.purchase_amount >= self.max_allowed_amount_for_purchase:
                    self.purchase_amount += 1
            elif self.key_tracker_arrow_down.has_key_been_fired_at_this_frame:
                if not self.purchase_amount <= 1:
                    self.purchase_amount -= 1

            # try to make the purchase
            elif self.key_tracker_enter.has_key_been_fired_at_this_frame:
                if has_enough_money:
                    self.player.money -= purchase_value
                    current_item.amount += self.purchase_amount

            # quit the phase
            elif self.key_tracker_k.has_key_been_fired_at_this_frame:
                self.stop_phase()
