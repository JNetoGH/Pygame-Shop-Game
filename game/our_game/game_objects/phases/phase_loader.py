import pygame

from JNetoProductions_pygame_game_engine.components.key_tracker_component import KeyTrackerComponent
from JNetoProductions_pygame_game_engine.components.rect_trigger_component import RectTriggerComponent
from JNetoProductions_pygame_game_engine.components.text_render_component import TextRenderComponent
from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject
from JNetoProductions_pygame_game_engine.systems.scalable_game_screen_system import ScalableGameScreen
from our_game.game_objects.phases.phase_controller import PhaseController
from our_game.game_objects.player import Player


class RegisterBook(GameObject):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        # the book area
        self.transform.move_world_position(pygame.Vector2(100,200))
        self.book_rect_trigger = RectTriggerComponent(20,0,150,170,self)

        self.text_render1 = TextRenderComponent("register", 25, pygame.Color(253, 253, 150), 0, -50, self)
        self.text_render2 = TextRenderComponent("book", 25, pygame.Color(253, 253, 150), 0, -30, self)

        self.remove_default_rect_image()

class PhaseLoaderTrasnlucentSquare(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.stop_rendering_this_game_object()

        self.image = pygame.Surface((1200, 50))
        self.image.set_alpha(200)  # alpha level
        self.image.fill((0, 0, 0))  # this fills the entire surface

        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth, 60))


class PhaseLoaderTextHolder(GameObject):
    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.remove_default_rect_image()
        self.stop_rendering_this_game_object()

        self.fix_game_object_on_screen(pygame.Vector2(ScalableGameScreen.HalfDummyScreenWidth,
                                                      ScalableGameScreen.HalfDummyScreenHeight))

        text = "go to the balcony and press E on the register book to load the next phase"
        self.text_render = TextRenderComponent(text, 25, pygame.Color(255, 255, 255), 0, -300, self)


class PhaseLoader(GameObject):

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)

        self.stop_rendering_this_game_object()

        self.remove_default_rect_image()
        self.fix_game_object_on_screen(pygame.Vector2(
            ScalableGameScreen.HalfDummyScreenWidth, ScalableGameScreen.HalfDummyScreenHeight))

        self.key_tracker_e = KeyTrackerComponent(pygame.K_e, self)

        self.is_being_displayed = False
        self.change_code: PhaseController.PhaseCode = PhaseController.PhaseCode.NullPhase

        self.translucent_square = PhaseLoaderTrasnlucentSquare("phase_loader_translucent_square", self.scene, self.rendering_layer)
        self.text_holder = PhaseLoaderTextHolder("phase_loader_text_holder", self.scene, self.rendering_layer)

        self.player: Player = self.scene.get_game_object_by_name("player")
        self.register_book = RegisterBook("register_book", self.scene, self.rendering_layer)

    def _stop_loader(self):
        self.is_being_displayed = False
        self.stop_rendering_this_game_object()
        self.text_holder.stop_rendering_this_game_object()
        self.translucent_square.stop_rendering_this_game_object()

    def load_phase(self, phase_code: PhaseController.PhaseCode):
        print("\nEntered in PhaseLoader\n")
        self._change_phase(PhaseController.PhaseCode.NullPhase)
        self.change_code = phase_code
        self.is_being_displayed = True
        self.start_rendering_this_game_object()
        self.text_holder.start_rendering_this_game_object()
        self.translucent_square.start_rendering_this_game_object()

    def game_object_update(self) -> None:

        if self.player.win:
            self._change_phase(PhaseController.PhaseCode.End)
            self._stop_loader()

        if self.is_being_displayed and not self.player.win:

            is_player_at_book_area = self.register_book.book_rect_trigger.is_there_a_point_inside(self.player.collider.world_position_get_only)
            if is_player_at_book_area:
                # changes book color to green
                self.register_book.text_render1.change_color(pygame.Color(50, 205, 50))
                self.register_book.text_render2.change_color(pygame.Color(50, 205, 50))

                # changes to the netx phase
                if self.key_tracker_e.has_key_been_fired_at_this_frame:
                    self._stop_loader()
                    self._change_phase(self.change_code)
                    # changes book color to gray
                    self.register_book.text_render1.change_color(pygame.Color(200, 200, 200))
                    self.register_book.text_render2.change_color(pygame.Color(200, 200, 200))

            else:
                # change book color to yellow
                self.register_book.text_render1.change_color(pygame.Color(253, 253, 150))
                self.register_book.text_render2.change_color(pygame.Color(253, 253, 150))


    @staticmethod
    def _change_phase(phase_code: PhaseController.PhaseCode):
        PhaseController.CurrentPhase = phase_code
