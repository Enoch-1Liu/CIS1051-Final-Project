import os
import re
from manimlib import *
import numpy as np
import sympy as sp

x, y = sp.symbols("x y")

ALLOWED_LOCALS = {
    "x": x,
    "y": y,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "exp": sp.exp,
    "sqrt": sp.sqrt,
    "log": sp.log,
    "ln": sp.log,
    "abs": sp.Abs,
    "pi": sp.pi,
    "e": sp.E,
}

from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

TRANSFORMS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)

def parse_math_expr(raw: str):
    s = raw.strip()
    if "=" in s:
        parts = s.split("=")
        if len(parts) == 2 and parts[0].strip().lower() == "y":
            s = parts[1].strip()
    return parse_expr(s, local_dict=ALLOWED_LOCALS, transformations=TRANSFORMS)


def compute_y_bounds(fn, x_min=-5.0, x_max=5.0, min_bound=5.0, max_bound=100.0):
    """Auto-scale symmetric y-bounds using the 95th percentile so asymptotes don't blow up the scale."""
    xs = np.linspace(x_min, x_max, 1000)
    with np.errstate(all="ignore"):
        ys = np.asarray(fn(xs), dtype=float)

    if ys.ndim == 0:
        ys = np.full_like(xs, float(ys))

    finite_abs = np.abs(ys[np.isfinite(ys)])
    if finite_abs.size == 0:
        return -min_bound, min_bound, max(1.0, min_bound / 5.0)

    peak = float(np.percentile(finite_abs, 95))
    bound = float(np.clip(peak * 1.15, min_bound, max_bound))
    step = max(1.0, round(bound / 5.0, 1))
    return -bound, bound, step


def build_segmented_curve(axes, fn, x_min=-5.0, x_max=5.0, y_limit=5.0, n=600):
    xs = np.linspace(x_min, x_max, n)
    with np.errstate(all="ignore"):
        ys = np.asarray(fn(xs), dtype=float)

    if ys.ndim == 0:
        ys = np.full_like(xs, float(ys))

    ys = np.where(np.isfinite(ys) & (np.abs(ys) <= y_limit * 1.5), ys, np.nan)

    group = VGroup()
    current_pts = []

    for i, (xv, yv) in enumerate(zip(xs, ys)):
        if np.isnan(yv) or abs(yv) > y_limit:
            if len(current_pts) >= 2:
                seg = VMobject(color=BLUE_C, stroke_width=3)
                seg.set_points_as_corners(current_pts)
                group.add(seg)
            current_pts = []
            continue

        if i > 0 and np.isfinite(ys[i - 1]) and abs(yv - ys[i - 1]) > y_limit:
            if len(current_pts) >= 2:
                seg = VMobject(color=BLUE_C, stroke_width=3)
                seg.set_points_as_corners(current_pts)
                group.add(seg)
            current_pts = []

        current_pts.append(axes.c2p(float(xv), float(yv)))

    if len(current_pts) >= 2:
        seg = VMobject(color=BLUE_C, stroke_width=3)
        seg.set_points_as_corners(current_pts)
        group.add(seg)

    return group


class EquationScene(Scene):
    def construct(self):
        raw_str = os.environ.get("EQUATION_STR", "15*sin(x)")
        expr = parse_math_expr(raw_str)

        if expr.has(y):
            sols = sp.solve(expr, y)
            if sols and not sols[0].has(y):
                fn = sp.lambdify(x, sols[0], modules=["numpy"])
            else:
                msg = Text("Enter an explicit expression in x (e.g., 15*sin(x))", font_size=24, color=RED)
                self.play(Write(msg))
                self.wait(2)
                return
        else:
            fn = sp.lambdify(x, expr, modules=["numpy"])

        x_min = float(os.environ.get("X_MIN", "-5.0"))
        x_max = float(os.environ.get("X_MAX", "5.0"))
        if x_min >= x_max:
            x_min, x_max = -5.0, 5.0

        x_span = x_max - x_min
        x_step = max(1.0, round(x_span / 10.0, 1))

        manual_y = os.environ.get("Y_MAX", "").strip()
        if manual_y:
            y_bound = max(0.5, float(manual_y))
            y_min, y_max = -y_bound, y_bound
            y_step = max(0.5, round(y_bound / 5.0, 1))
        else:
            y_min, y_max, y_step = compute_y_bounds(fn, x_min=x_min, x_max=x_max)

        axes = Axes(
            x_range=(x_min, x_max, x_step),
            y_range=(y_min, y_max, y_step),
            width=8,
            height=5,
            axis_config={"include_tip": False},
        )
        label = Text(
            f"y = {raw_str}   x in [{x_min:g}, {x_max:g}], y in [{-y_max:g}, {y_max:g}]",
            font_size=20,
            color=YELLOW,
        ).to_edge(UP)
        graph = build_segmented_curve(axes, fn, x_min=x_min, x_max=x_max, y_limit=y_max)

        self.play(ShowCreation(axes), Write(label))
        self.play(ShowCreation(graph), run_time=2.0)
        self.wait(1.0)

class MatrixScene(Scene):
    def construct(self):
        a = float(os.environ.get("MAT_A", "2.0"))
        b = float(os.environ.get("MAT_B", "1.0"))
        c = float(os.environ.get("MAT_C", "0.0"))
        d = float(os.environ.get("MAT_D", "2.0"))

        det = a * d - b * c

        plane = NumberPlane(
            x_range=(-6, 6, 1),
            y_range=(-6, 6, 1),
            width=9,
            height=6,
        ).shift(DOWN * 0.25)

        # Standard basis vectors: i_hat = (1, 0), j_hat = (0, 1)
        i_hat = Arrow(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            buff=0,
            color=GREEN_C,
            stroke_width=5,
        )
        j_hat = Arrow(
            plane.c2p(0, 0),
            plane.c2p(0, 1),
            buff=0,
            color=RED_C,
            stroke_width=5,
        )

        # Unit square showing area scaling via |det(A)|
        unit_square = Polygon(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            plane.c2p(1, 1),
            plane.c2p(0, 1),
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.2,
            stroke_width=2.5,
        )

        header = Text(
            f"A = [[{a:g}, {b:g}], [{c:g}, {d:g}]]   |   det(A) = {det:g}",
            font_size=24,
            color=YELLOW,
        ).to_edge(UP)

        legend = Text(
            "i-hat (green) -> col 1   |   j-hat (red) -> col 2",
            font_size=20,
            color=GREY_A,
        ).next_to(header, DOWN, buff=0.12)

        self.play(
            ShowCreation(plane),
            Write(header),
            FadeIn(legend),
        )
        self.play(
            GrowArrow(i_hat),
            GrowArrow(j_hat),
            ShowCreation(unit_square),
            run_time=1.2,
        )
        self.wait(0.8)

        # Compute transformed endpoints in plane coordinates
        new_i_end = plane.c2p(a, c)
        new_j_end = plane.c2p(b, d)
        origin_pt = plane.c2p(0, 0)

        target_i = Arrow(origin_pt, new_i_end, buff=0, color=GREEN_C, stroke_width=5)
        target_j = Arrow(origin_pt, new_j_end, buff=0, color=RED_C, stroke_width=5)
        target_square = Polygon(
            origin_pt,
            new_i_end,
            plane.c2p(a + b, c + d),
            new_j_end,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.2,
            stroke_width=2.5,
        )

        # Deform grid lines smoothly by applying the linear map (x, y) -> (ax + by, cx + dy)
        target_plane = plane.copy()
        for mob in target_plane.get_family():
            if isinstance(mob, VMobject) and mob is not target_plane:
                pts = mob.get_points()
                if len(pts) > 0:
                    transformed_pts = []
                    for pt in pts:
                        x_val, y_val = plane.p2c(pt)[:2]
                        nx = a * x_val + b * y_val
                        ny = c * x_val + d * y_val
                        transformed_pts.append(plane.c2p(nx, ny))
                    mob.set_points(np.array(transformed_pts))

        self.play(
            Transform(plane, target_plane),
            Transform(i_hat, target_i),
            Transform(j_hat, target_j),
            Transform(unit_square, target_square),
            run_time=2.5,
        )
        self.wait(1.5)