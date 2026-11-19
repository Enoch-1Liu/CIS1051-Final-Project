from manimlib import *
import numpy as np


class FourierWindingMachine(Scene):
    def construct(self):
        # Narration bar helper, smoothly handles caption transitions
        caption_bg = Rectangle(
            width=13.4,
            height=0.85,
            fill_color=BLACK,
            fill_opacity=0.85,
            stroke_color=GREY_B,
            stroke_width=1.5,
        ).to_edge(DOWN, buff=0.2)

        current_caption = None

        def set_caption(message, color=WHITE, wait_time=0.0):
            nonlocal current_caption
            new_caption = Text(message, font_size=22, color=color)
            if new_caption.get_width() > 12.8:
                new_caption.set_width(12.8)
            new_caption.move_to(caption_bg.get_center())

            if current_caption is None:
                self.play(FadeIn(caption_bg), FadeIn(new_caption), run_time=0.6)
            else:
                self.play(
                    FadeOut(current_caption, run_time=0.3),
                    FadeIn(new_caption, run_time=0.4),
                )
            current_caption = new_caption
            if wait_time > 0:
                self.wait(wait_time)

        # INTRO: Title Card
        title = Text("The Fourier Transform", font_size=52, color=BLUE_C)
        subtitle = Text("Visualizing the Winding Machine Intuition", font_size=28, color=GREY_A)
        subtitle.next_to(title, DOWN, buff=0.35)

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), run_time=0.8)

        # 1. Define the signal: 2 Hz + 3 Hz + DC offset
        t_max = 3.0
        n_samples = 600
        t_vals = np.linspace(0, t_max, n_samples)

        def signal(t):
            return 1.5 + 0.8 * np.cos(2 * np.pi * 2.0 * t) + 0.5 * np.cos(2 * np.pi * 3.0 * t)

        # ACT 1: Time-Domain Signal (Top-Left)
        time_axes = Axes(
            x_range=(0, t_max, 0.5),
            y_range=(0, 3.2, 1),
            width=5.2,
            height=1.9,
            axis_config={"include_tip": False},
        ).to_corner(UL, buff=0.55).shift(DOWN * 0.2)

        time_label = Text("g(t) = 1.5 + 0.8cos(4pi t) + 0.5cos(6pi t)", font_size=20, color=BLUE_C)
        time_label.next_to(time_axes, UP, buff=0.15)

        time_graph = time_axes.get_graph(signal, x_range=(0, t_max), color=BLUE_C)

        set_caption("Step 1: Start with a signal g(t) that mixes 2 Hz and 3 Hz waves.")
        self.play(
            ShowCreation(time_axes),
            Write(time_label),
            ShowCreation(time_graph),
            run_time=2.0,
        )
        self.wait(1.5)

        # ACT 2: Complex Plane & Winding (Bottom-Left)
        complex_plane = ComplexPlane(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            width=3.2,
            height=3.2,
        ).next_to(time_axes, DOWN, buff=0.75)

        freq_tracker = ValueTracker(0.5)

        freq_readout = always_redraw(lambda: Text(
            f"Winding f = {freq_tracker.get_value():.2f} Hz",
            font_size=22,
            color=YELLOW,
        ).next_to(complex_plane, UP, buff=0.15))

        def get_wound_curve():
            f = freq_tracker.get_value()
            z = signal(t_vals) * np.exp(-2j * np.pi * f * t_vals)
            points = [complex_plane.n2p(val) for val in z]
            curve = VMobject(color=YELLOW, stroke_width=2.5)
            curve.set_points_as_corners(points)
            return curve

        wound_curve = always_redraw(get_wound_curve)

        set_caption("Step 2: Wrap g(t) around the origin in the complex plane at a test frequency f.")
        self.play(ShowCreation(complex_plane), run_time=1.2)
        self.play(FadeIn(freq_readout), FadeIn(wound_curve), run_time=1.0)
        self.wait(1.8)

        # ACT 3: Center of Mass & Frequency Spectrum (Right)
        def get_com_complex(f):
            z = signal(t_vals) * np.exp(-2j * np.pi * f * t_vals)
            return np.mean(z)

        com_dot = always_redraw(lambda: Dot(
            complex_plane.n2p(get_com_complex(freq_tracker.get_value())),
            color=RED,
            radius=0.09,
        ))

        freq_axes = Axes(
            x_range=(0, 4.5, 1),
            y_range=(-0.2, 1.8, 0.5),
            width=5.4,
            height=4.0,
            axis_config={"include_tip": False},
        ).to_edge(RIGHT, buff=0.55).shift(UP * 0.25)

        freq_label = Text("Fourier Spectrum: Re(Center of Mass)", font_size=20, color=RED_C)
        freq_label.next_to(freq_axes, UP, buff=0.2)

        def get_spectrum_curve():
            f_curr = freq_tracker.get_value()
            freqs = np.linspace(0.5, max(0.51, f_curr), 250)
            points = [
                freq_axes.c2p(f, np.real(get_com_complex(f)))
                for f in freqs
            ]
            curve = VMobject(color=RED_C, stroke_width=3)
            curve.set_points_as_corners(points)
            return curve

        spectrum_curve = always_redraw(get_spectrum_curve)

        set_caption("Step 3: Track the red Center of Mass. For non-matching frequencies, it stays near 0.")
        self.play(
            FadeIn(com_dot, scale=2.0),
            ShowCreation(freq_axes),
            Write(freq_label),
            run_time=1.5,
        )
        self.add(spectrum_curve)
        self.wait(1.8)

        # ACT 4: Sweep to First Resonance (2.0 Hz)
        set_caption("Sweeping f upward... Watch the wrapped curve and red dot as we approach 2.0 Hz.")
        self.play(
            freq_tracker.animate.set_value(2.0),
            run_time=4.5,
            rate_func=linear,
        )

        # Pause and highlight the 2.0 Hz spike
        spike_2 = Dot(freq_axes.c2p(2.0, np.real(get_com_complex(2.0))), color=YELLOW, radius=0.09)
        label_2 = Text("2.0 Hz", font_size=18, color=YELLOW).next_to(spike_2, UP, buff=0.12)

        set_caption(
            "Match at 2.0 Hz! Peaks align on one side, pulling the Center of Mass outward.",
            color=YELLOW,
        )
        self.play(FadeIn(spike_2), Write(label_2), Indicate(com_dot, scale_factor=1.8))
        self.wait(2.5)

        # ACT 5: Sweep to Second Resonance (3.0 Hz)
        set_caption("Continuing the sweep... Between frequencies, the curve balances out again.")
        self.play(
            freq_tracker.animate.set_value(3.0),
            run_time=3.5,
            rate_func=linear,
        )

        # Pause and highlight the 3.0 Hz spike
        spike_3 = Dot(freq_axes.c2p(3.0, np.real(get_com_complex(3.0))), color=YELLOW, radius=0.09)
        label_3 = Text("3.0 Hz", font_size=18, color=YELLOW).next_to(spike_3, UP, buff=0.12)

        set_caption(
            "Match at 3.0 Hz! A second spike reveals the 3.0 Hz component hidden in g(t).",
            color=YELLOW,
        )
        self.play(FadeIn(spike_3), Write(label_3), Indicate(com_dot, scale_factor=1.8))
        self.wait(2.5)

        # ACT 6: Finish Sweep & Closing Summary
        set_caption("Finishing the sweep to 4.2 Hz... No other frequencies are present.")
        self.play(
            freq_tracker.animate.set_value(4.2),
            run_time=3.0,
            rate_func=linear,
        )

        set_caption(
            "Result: The Fourier Transform decomposes any time wave into its exact frequency spikes.",
            color=GREEN_C,
            wait_time=3.0,
        )