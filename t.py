from manim import *
import numpy as np

# Configure for YouTube 16:9 video (1080p)
config.frame_width = 16
config.frame_height = 9
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 30

class FrogJump(Scene):
    def construct(self):
        # --- Water Background ---
        water = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color="#a0d8ef",  # light blue water
            fill_opacity=0.8,
            stroke_width=0
        )
        self.add(water)

        # Waves: animated sinusoidal lines across full width
        waves = VGroup(*[
            FunctionGraph(
                lambda x, y=y: 0.1 * np.sin(2 * (x + self.time)) + y,
                x_range=[-config.frame_width/2, config.frame_width/2],
                color="#4ca3dd",  # blue waves
                stroke_width=1
            ).shift(DOWN * y)
            for y in np.arange(-2, 4, 0.5)
        ])
        waves.add_updater(lambda m: m.set_opacity(0.6))
        self.add(waves)

        # --- Stone ---
        stone = Ellipse(
            width=3, height=1.2,
            fill_color="#7f6a55",   # brownish grey
            fill_opacity=1,
            stroke_color="#5e4e3d", # darker outline
            stroke_width=4
        ).move_to(DOWN * 1)
        self.add(stone)

        # --- Frog Creation ---
        frog = self.create_frog()
        frog.move_to(stone.get_top() + DOWN * 0.1)
        self.add(frog)

        # --- Jump + Ripple Animation ---
        jump_anim = (
            frog.animate(rate_func=there_and_back, run_time=1)
            .shift(UP * 2)
            .scale(1.1, about_point=frog.get_bottom())
        )
        ripple = Circle(
            radius=0.5,
            stroke_color="#FFFFFF",  # white ripple
            stroke_width=2
        ).move_to(stone.get_center())

        self.play(jump_anim)
        self.play(
            Create(ripple),
            ripple.animate.scale(3).set_opacity(0),
            run_time=1
        )
        self.wait(2)

    def create_frog(self):
        # Body and belly
        body = Ellipse(
            width=1.2, height=0.7,
            fill_color="#32cd32",  # lime green
            fill_opacity=1
        )
        belly = Ellipse(
            width=0.7, height=0.35,
            fill_color="#9ae69a",  # light green
            fill_opacity=1
        ).shift(DOWN * 0.1)

        # Eyes
        eyes = VGroup()
        for offset in [-0.35, 0.35]:
            eye = Circle(
                radius=0.18,
                fill_color="#FFFFFF",  # white
                stroke_width=1
            )
            pupil = Circle(
                radius=0.08,
                fill_color="#000000"   # black
            ).shift(UP * 0.02)
            grp = VGroup(eye, pupil).move_to(
                body.get_center() + UP * 0.3 + RIGHT * offset
            )
            eyes.add(grp)

        # Legs
        legs = VGroup()
        for side in [-1, 1]:
            leg = VMobject()
            leg.set_points_as_corners([
                body.get_center() + DOWN * 0.4 + RIGHT * side * 0.3,
                body.get_center() + DOWN * 1   + RIGHT * side * 0.7
            ])
            leg.set_stroke("#32cd32", 10)  # same as body color
            legs.add(leg)

        return VGroup(body, belly, eyes, legs)
