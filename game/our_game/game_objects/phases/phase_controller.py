import enum

from JNetoProductions_pygame_game_engine.game_object_base_class import GameObject


class PhaseController(GameObject):
    class PhaseCode(enum.Enum):
        End = -2
        NullPhase = -1
        BuyingPhase = 0
        CraftingPhase = 1
        SellingPhase = 2

    CurrentPhase: PhaseCode = PhaseCode.NullPhase

    def __init__(self, name: str, scene, rendering_layer):
        super().__init__(name, scene, rendering_layer)
        self.remove_default_rect_image()

        self.buying_phase = self.scene.get_game_object_by_name("buying_phase")
        self.crafting_phase = self.scene.get_game_object_by_name("crafting_phase")
        self.selling_phase = self.scene.get_game_object_by_name("selling_phase")
        self.player = self.scene.get_game_object_by_name("player")
        self.phase_loader = self.scene.get_game_object_by_name("phase_loader")
        self.phase_loader.load_phase(PhaseController.PhaseCode.BuyingPhase)

    def game_object_update(self) -> None:

        if PhaseController.CurrentPhase == PhaseController.PhaseCode.End:
            self.buying_phase.stop_phase()
            self.crafting_phase.stop_phase()
            self.selling_phase.stop_phase()
            self.phase_loader._stop_loader()

        if PhaseController.CurrentPhase == PhaseController.PhaseCode.BuyingPhase and not self.buying_phase.is_running and not self.player.win:
            self.buying_phase.run_phase()
        elif PhaseController.CurrentPhase == PhaseController.PhaseCode.CraftingPhase and not self.crafting_phase.is_running and not self.player.win:
            self.crafting_phase.run_phase()
        elif PhaseController.CurrentPhase == PhaseController.PhaseCode.SellingPhase and not self.selling_phase.is_running and not self.player.win:
            self.selling_phase.run_phase()
        elif self.player.win:
            PhaseController.CurrentPhase = PhaseController.PhaseCode.NullPhase
