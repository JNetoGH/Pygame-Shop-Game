import pygame


class ScalableGameScreen:

    # DUMMY SCREEN
    DummyScreenWidth = 1600
    DummyScreenHeight = 900
    HalfDummyScreenWidth = DummyScreenWidth // 2
    HalfDummyScreenHeight = DummyScreenHeight // 2

    # REAL CANVAS
    RealScreenWidth = 2300
    RealScreenScreenHeight = 1080
    HalfRealScreenWidth = RealScreenWidth // 2
    HalfRealScreenHeight = RealScreenScreenHeight // 2

    # CANVAS SURFACES
    TargetResolutionForUpScaling = [1600, 900]
    GameScreenDummySurface: pygame.Surface = None
    GameScreenRealSurface: pygame.Surface = None

    @staticmethod
    def init_screens(dummy_screen_resolution: list[int], real_screen_resolution: list[int], up_scaling_target_resolution):
        ScalableGameScreen.GameScreenDummySurface = pygame.Surface(dummy_screen_resolution)
        ScalableGameScreen.GameScreenRealSurface = pygame.display.set_mode(real_screen_resolution)
        ScalableGameScreen.TargetResolutionForUpScaling = up_scaling_target_resolution

    @staticmethod
    def upscale_dummy_screen_to_target_resolution():
        # the dummy frame after scaling
        scaled_frame = pygame.transform.scale(ScalableGameScreen.GameScreenDummySurface, ScalableGameScreen.TargetResolutionForUpScaling)
        return scaled_frame

    @staticmethod
    def generate_dummy_scaled_frame_centralized_inside_the_real_screen_surface():
        centralized_scaled_frame = ScalableGameScreen.upscale_dummy_screen_to_target_resolution()
        centralized_scaled_frame_rect = centralized_scaled_frame.get_rect()
        centralized_scaled_frame_rect.x = (ScalableGameScreen.GameScreenRealSurface.get_width() -
                               ScalableGameScreen.TargetResolutionForUpScaling[0]) // 2
        centralized_scaled_frame_rect.y = (ScalableGameScreen.GameScreenRealSurface.get_height() -
                               ScalableGameScreen.TargetResolutionForUpScaling[1]) // 2
        return centralized_scaled_frame, centralized_scaled_frame_rect

    @staticmethod
    def render_final_scaled_result():
        centralized_scaled_frame, centralized_scaled_frame_rect = ScalableGameScreen.generate_dummy_scaled_frame_centralized_inside_the_real_screen_surface()
        ScalableGameScreen.GameScreenRealSurface.blit(centralized_scaled_frame, centralized_scaled_frame_rect)
        pygame.display.update()

    TILE_SIZE = 64


