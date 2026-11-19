from pathlib import Path
import os
import subprocess
import time
import streamlit as st
import sympy as sp

st.title("Manim Math Visualizer")

mode = st.selectbox("Mode", ["2D Equation", "2x2 Matrix"])

scene_name = "EquationScene"
valid = True
env = os.environ.copy()

if mode == "2D Equation":
    scene_name = "EquationScene"
    expr_text = st.text_input("Enter f(x)", value="15*sin(x)")
    x = sp.Symbol("x")

    try:
        expr = sp.sympify(
            expr_text,
            locals={
                "sin": sp.sin,
                "cos": sp.cos,
                "tan": sp.tan,
                "exp": sp.exp,
                "sqrt": sp.sqrt,
                "log": sp.log,
                "ln": sp.log,
                "abs": sp.Abs,
                "pi": sp.pi,
                "e": sp.E,
            },
        )
        _ = sp.lambdify(x, expr, modules=["numpy"])
    except Exception as err:
        st.error(f"Invalid equation: {err}")
        valid = False

    col_x1, col_x2 = st.columns(2)
    with col_x1:
        x_min = st.number_input("X Min", value=-5.0, step=1.0)
    with col_x2:
        x_max = st.number_input("X Max", value=5.0, step=1.0)

    if x_min >= x_max:
        st.error("X Min must be smaller than X Max.")
        valid = False

    auto_y = st.checkbox("Auto-fit Y axis", value=True)
    y_max_input = st.number_input(
        "Custom ±Y range (used if Auto-fit is off)",
        min_value=1.0,
        max_value=500.0,
        value=20.0,
        step=1.0,
    )

    env["EQUATION_STR"] = expr_text
    env["X_MIN"] = str(x_min)
    env["X_MAX"] = str(x_max)
    if not auto_y:
        env["Y_MAX"] = str(y_max_input)
    else:
        env.pop("Y_MAX", None)

else:
    scene_name = "MatrixScene"
    st.caption("Matrix A = [[a, b], [c, d]] — column 1 is where i-hat lands; column 2 is where j-hat lands.")
    r1_c1, r1_c2 = st.columns(2)
    with r1_c1:
        mat_a = st.number_input("a (x of i-hat)", value=2.0, step=0.5)
    with r1_c2:
        mat_b = st.number_input("b (x of j-hat)", value=1.0, step=0.5)

    r2_c1, r2_c2 = st.columns(2)
    with r2_c1:
        mat_c = st.number_input("c (y of i-hat)", value=0.0, step=0.5)
    with r2_c2:
        mat_d = st.number_input("d (y of j-hat)", value=2.0, step=0.5)

    det = mat_a * mat_d - mat_b * mat_c
    st.info(f"Determinant $\\det(A) = {det:g}$ (area scale factor of the unit square)")

    env["MAT_A"] = str(mat_a)
    env["MAT_B"] = str(mat_b)
    env["MAT_C"] = str(mat_c)
    env["MAT_D"] = str(mat_d)


def find_latest_mp4(prefix: str, start_time: float) -> Path | None:
    project_root = Path(__file__).resolve().parent
    candidates = [
        p for p in project_root.rglob(f"{prefix}*.mp4")
        if p.stat().st_mtime >= start_time - 1.0
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


if st.button("Render Video") and valid:
    start_time = time.time()
    cmd = ["manimgl", str(Path(__file__).resolve().parent / "dynamic_plot.py"), scene_name, "-w"]

    with st.spinner(f"Rendering {scene_name} with manimgl..."):
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)

    if result.returncode != 0:
        st.error("Render failed:")
        if result.stderr:
            st.code(result.stderr, language="text")
        if result.stdout:
            st.code(result.stdout, language="text")
    else:
        video_path = find_latest_mp4(scene_name, start_time)
        if video_path and video_path.exists():
            st.video(str(video_path))
        else:
            st.warning(f"Command finished, but no {scene_name} .mp4 file was found under the project folder.")
            if result.stdout:
                st.code(result.stdout, language="text")