# sets the current animation in a animation list and the current frame of the animation according to a speed
from systems.animation.animation_clip import AnimationClip
from gameobjs.game_obj import GameObject


class AnimationController:

    def __init__(self, default_animation_clip: AnimationClip):
        self.default_animation_clip = default_animation_clip
        self.animation_clips_list = [self.default_animation_clip]
        self.current_animation_clip_name = self.default_animation_clip.name
        self.current_animation_clip = self.default_animation_clip
        self.current_frame_index = 0  # the current img of the animation clip
        self.animation_speed = 4

    def add_animation(self, *animations: AnimationClip) -> None:
        for animation in animations:
            self.animation_clips_list.append(animation)

    def remove_animation(self, *animations: AnimationClip) -> None:
        for animation in animations:
            self.animation_clips_list.remove(animation)

    def set_current_animation(self, animation_clip_name) -> None:
        for animation_clip in self.animation_clips_list:
            if animation_clip.name == animation_clip_name:
                self.current_animation_clip = animation_clip
                self.current_animation_clip_name = animation_clip_name

    # ANIMATE
    def animate(self, game_object: GameObject) -> None:
        # jump from frame to frame
        self.current_frame_index += self.animation_speed * game_object.level.game.delta_time
        # sets back to the first frame if it's bigger than the size of the animation
        if self.current_frame_index >= len(self.current_animation_clip.images):
            self.current_frame_index = 0
        game_object.image = self.current_animation_clip.images[int(self.current_frame_index)]
