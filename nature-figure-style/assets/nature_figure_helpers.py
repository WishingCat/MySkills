"""Nature-style figure helpers.

Reusable functions for the nature-figure-style skill. Empirical defaults are
calibrated against 22 Nature / Nature Photonics papers in the project's
`figures_extracted/` corpus — see references/empirical_observations.md.

Three groups:
  1. Style helpers: load mplstyle, fetch palettes, add panel labels.
  2. Architecture-diagram primitives: blocks, arrows, optical components,
     glowing volumetric beams, isometric chip stacks.
  3. Convention dictionaries: MATERIAL_COLORS, COMB_COLORS — recurring
     color choices across Nature Photonics papers.

Usage:
    from nature_figure_helpers import (
        setup_nature_style, nature_palette, add_panel_label,
        MATERIAL_COLORS, COMB_COLORS,
        draw_block, draw_arrow, draw_optical_path, draw_glow_beam,
        draw_laser_source, draw_lens, draw_modulator,
        draw_photodetector, draw_chip_rainbow, draw_isometric_layer_stack,
        callout, setup_schematic_axes,
    )
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from matplotlib.patches import (
    Circle,
    Ellipse,
    FancyArrowPatch,
    FancyBboxPatch,
    Polygon,
    Rectangle,
    Wedge,
)


# ===========================================================================
# Style helpers
# ===========================================================================

_STYLE_PATH = Path(__file__).resolve().parent / "nature.mplstyle"

PALETTES: dict[str, list[str]] = {
    # Empirical default: most-recurring 5-color set in Nature Photonics 2024-25.
    # Anchor papers: Yao 2025, Jin 2025, Kalinin 2025.
    "nature_photonics_modern": [
        "#E63946", "#F4A261", "#E9C46A", "#2A9D8F", "#264653",
        "#7E3FA8", "#F46197", "#888888",
    ],
    # Older Nature Photonics 2019-2023 categorical convention (red+blue+green+orange).
    "nature_photonics_classic": [
        "#D6322B", "#1F5FAE", "#2A8E3A", "#E08A2A",
        "#7E3FA8", "#B23A8C", "#222222", "#888888",
    ],
    # NPG (ggsci / npg_palette) — Cell / Nature Methods / biology default.
    "nature_journal": [
        "#E64B35", "#4DBBD5", "#00A087", "#3C5488",
        "#F39B7F", "#8491B4", "#91D1C2", "#DC0000",
    ],
    "morandi": ["#D7C7BC", "#C3AE94", "#B8A99A", "#A3A3A3",
                "#9DA9AC", "#8D9C8C", "#7E7F76", "#5C5C5C"],
    "monet": ["#A7C5D8", "#7FA5B9", "#B8C8A0", "#D8D4A5",
              "#E8B9A6", "#C98A8A", "#9B7B9B", "#5C6B8A"],
    "sunset": ["#FFE5B4", "#FFC988", "#FFA14A", "#FF6F3C",
               "#E63946", "#A4343A", "#6A0F49", "#2E1A47"],
    "ocean": ["#E0F7FA", "#A0DEE5", "#5BC0BE", "#3A9188",
              "#1C5D7A", "#0E3A5F", "#08244F", "#020F27"],
    "sakura": ["#FFF5F7", "#FFE0EC", "#FFB7CE", "#FF8FAB",
               "#F46197", "#C44B7F", "#8B3A62", "#4A1D3F"],
    "tiffany": ["#E8F6F3", "#A8DADC", "#81C9C4", "#4FB3A9",
                "#2E8B85", "#1F5F5B", "#F5E6CA", "#DDB892"],
}


# Recurring material-color recipe in 3D / isometric chip schematics
# (Hu 2021, He 2019, Feng 2024, Geravand 2025, Wang 2024, Yao 2025, Cheng 2025).
MATERIAL_COLORS: dict[str, str] = {
    # Substrates
    "silicon":       "#1F7C3A",   # Si — saturated forest green (He 2019, Geravand 2025)
    "silicon_alt":   "#5C8A6E",   # paler Si used by some isometric renders
    "ltoi":          "#5E60CE",   # LiTaO3 vivid purple-blue (Wang 2024)
    "lnoi":          "#D63E8C",   # thin-film LiNbO3 pink-magenta (He 2019, Feng 2024)
    "lnoi_light":    "#E58FB1",   # softer LN tone for lighter renders
    "sio2":          "#E8D8B0",   # buried oxide pale tan
    "sapphire":      "#9DC8E8",   # pale blue
    # Conductors / metal
    "gold":          "#E5B83A",   # electrodes / wire-bonds
    "gold_warm":     "#F2C83A",
    "copper":        "#C97B3D",
    "aluminum":      "#9DA9B5",
    # Optical / mode
    "active_mode":   "#2A9D8F",   # waveguide mode glow / teal
    "active_mode_b": "#26A69A",
    "passive":       "#BFBFBF",   # passive structures, generic gray
    # Electronics / detectors
    "pd_dark":       "#1E3A78",
    "rf_red":        "#D6322B",
}


# Dual-comb / pump-probe color convention (Giorgetta, Han, Jin, Cheng, Hu).
COMB_COLORS: dict[str, str] = {
    "comb1":   "#D6322B",   # red — comb 1 / signal
    "signal":  "#D6322B",
    "pump":    "#D6322B",
    "comb2":   "#1F5FAE",   # blue — comb 2 / LO / probe
    "lo":      "#1F5FAE",
    "probe":   "#1F5FAE",
    "beat":    "#7E3FA8",   # purple — beat / RF / heterodyne
    "rf":      "#7E3FA8",
    "shg":     "#2A8E3A",   # green — second harmonic / auxiliary
    "aux":     "#2A8E3A",
    "fiber":   "#F0C03A",   # yellow — EDFA / pump-fiber path
    "edfa":    "#F0C03A",
    "control": "#888888",   # gray — feedback / control (often dashed)
}


def setup_nature_style(palette: str = "nature_photonics_modern") -> None:
    """Apply the Nature-style mplstyle and pick a color cycle.

    Default is the empirically most-common Nature Photonics 2024-25 palette.
    Pass `nature_journal` for the older NPG biology cycle, or any other
    name in PALETTES.
    """
    plt.style.use(str(_STYLE_PATH))
    plt.rcParams["axes.prop_cycle"] = plt.cycler(color=nature_palette(palette))


def nature_palette(name: str = "nature_photonics_modern") -> list[str]:
    """Return a list of hex colors by palette name (see PALETTES)."""
    key = name.lower().replace("-", "_")
    if key not in PALETTES:
        raise KeyError(
            f"Unknown palette {name!r}. Available: {sorted(PALETTES)}"
        )
    return list(PALETTES[key])


def make_cmap(name: str = "sunset", n: int = 256) -> LinearSegmentedColormap:
    """Build a LinearSegmentedColormap from a named palette."""
    return LinearSegmentedColormap.from_list(name, nature_palette(name), N=n)


def add_panel_label(
    ax: plt.Axes,
    label: str,
    x: float = -0.15,
    y: float = 1.04,
    fontsize: float = 9,
) -> None:
    """Add a bold lowercase panel label at axis-coord (x, y).

    Empirical convention: bold lowercase a/b/c, sans-serif, ~9 pt, flush
    to the top-left of the panel — never (a), never A, never with period.
    Default position is just outside the axes top-left; for tight panels
    you may want (0.02, 0.98) for inside placement.
    """
    ax.text(
        x, y, label,
        transform=ax.transAxes,
        fontsize=fontsize, fontweight="bold",
        va="top", ha="left", color="#222222",
    )


def half_frame(ax: plt.Axes) -> None:
    """Hide top and right spines (the "open" L+B-only style).

    Pair with `ax.tick_params(top=False, right=False)` if your style
    enabled mirror ticks. Use this for clean line plots / bar plots
    that don't need a closed box; for spectra, log-log, polar, dense
    time series the default 4-spine box is more idiomatic.
    """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(top=False, right=False)


# ===========================================================================
# Architecture-diagram primitives
# ===========================================================================

_DEFAULT_EDGE = "#222222"
_DEFAULT_FILL = "#A8DADC"


def draw_block(
    ax: plt.Axes,
    x: float, y: float, w: float, h: float,
    label: str = "",
    fill: str = _DEFAULT_FILL,
    edge: str = _DEFAULT_EDGE,
    fontsize: float = 7.5,
    rounding: float | None = None,
    text_color: str = "#222222",
    linewidth: float = 0.6,
    zorder: float = 2,
) -> FancyBboxPatch:
    """Rounded rectangle with centered text. Use for system / flow diagrams."""
    if rounding is None:
        rounding = 0.12 * min(w, h)
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={rounding}",
        linewidth=linewidth, edgecolor=edge, facecolor=fill, zorder=zorder,
    )
    ax.add_patch(box)
    if label:
        ax.text(
            x + w / 2, y + h / 2, label,
            ha="center", va="center",
            fontsize=fontsize, color=text_color, zorder=zorder + 0.1,
        )
    return box


def draw_arrow(
    ax: plt.Axes,
    x1: float, y1: float, x2: float, y2: float,
    color: str = _DEFAULT_EDGE,
    linewidth: float = 0.8,
    style: str = "-|>",
    mutation_scale: float = 8,
    linestyle: str = "-",
    zorder: float = 3,
) -> FancyArrowPatch:
    """Solid arrow from (x1, y1) to (x2, y2).

    Empirical convention: thin (0.5-0.8 pt) black with small filled
    triangular head (-|>) at ~3 pt size. Curved arrows for feedback,
    straight for signal flow.
    """
    arr = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=mutation_scale,
        linewidth=linewidth, color=color, linestyle=linestyle, zorder=zorder,
    )
    ax.add_patch(arr)
    return arr


def draw_optical_path(
    ax: plt.Axes,
    points: Sequence[tuple[float, float]],
    color: str | None = None,
    role: str | None = None,
    linewidth: float = 1.4,
    arrow: bool = False,
    linestyle: str = "-",
    zorder: float = 2.5,
) -> None:
    """Piecewise-linear optical path through a list of points.

    Either pass an explicit `color` (hex) or a `role` from COMB_COLORS
    ("signal", "comb1", "comb2", "lo", "pump", "probe", "beat", "shg",
    "fiber", "control"). Solid line by default; pass linestyle='--' for
    feedback / virtual / proposed paths.
    """
    if color is None:
        color = COMB_COLORS.get(role or "signal", _DEFAULT_EDGE)
    pts = np.asarray(points, dtype=float)
    if linestyle == "-":
        ax.plot(
            pts[:, 0], pts[:, 1],
            color=color, linewidth=linewidth, solid_capstyle="round",
            zorder=zorder,
        )
    else:
        ax.plot(
            pts[:, 0], pts[:, 1],
            color=color, linewidth=linewidth, linestyle=linestyle,
            dashes=(3, 2), zorder=zorder,
        )
    if arrow and len(pts) >= 2:
        draw_arrow(
            ax, pts[-2, 0], pts[-2, 1], pts[-1, 0], pts[-1, 1],
            color=color, linewidth=linewidth * 0.8,
            mutation_scale=9, zorder=zorder + 0.2,
        )


def draw_glow_beam(
    ax: plt.Axes,
    p1: tuple[float, float],
    p2: tuple[float, float],
    color: str = "#E63946",
    core_width: float = 0.6,
    halo_width: float = 4.0,
    n_layers: int = 5,
    zorder: float = 2.4,
) -> None:
    """A "volumetric glowing beam": one bright core stroke with several
    progressively wider, more transparent halo strokes underneath.

    Reproduces the soft red beams used in 3D hero schematics
    (Kalinin 2025 AOC, Dinani 2025 fiber bundle, Jin 2025 chip module).
    Use for the headline beam of a 3D figure; vector schematics should
    use draw_optical_path() instead — the two looks should not mix in
    the same panel.
    """
    rgb = to_rgb(color)
    p1a = np.asarray(p1, dtype=float)
    p2a = np.asarray(p2, dtype=float)
    for i in range(n_layers, 0, -1):
        frac = i / n_layers
        w = core_width + (halo_width - core_width) * frac
        a = 0.55 * (1 - frac) ** 1.6 + 0.05
        ax.plot(
            [p1a[0], p2a[0]], [p1a[1], p2a[1]],
            color=(*rgb, a), linewidth=w,
            solid_capstyle="round", zorder=zorder - i * 0.01,
        )
    ax.plot(
        [p1a[0], p2a[0]], [p1a[1], p2a[1]],
        color=color, linewidth=core_width,
        solid_capstyle="round", zorder=zorder + 0.1,
    )


def draw_laser_source(
    ax: plt.Axes,
    x: float, y: float,
    width: float = 8,
    height: float = 4,
    label: str = "",
    fill: str = "#D6322B",
    edge: str = _DEFAULT_EDGE,
    label_below: bool = True,
) -> None:
    """A laser block: rectangle with a small triangular 'beam exit'.

    Default fill is the canonical "laser red" #D6322B. (x, y) is the
    LEFT edge midpoint; beam exits to the right.
    """
    body = Rectangle(
        (x, y - height / 2), width, height,
        facecolor=fill, edgecolor=edge, linewidth=0.6, zorder=2,
    )
    ax.add_patch(body)
    nose = Polygon(
        [(x + width, y - height / 4),
         (x + width + height / 2, y),
         (x + width, y + height / 4)],
        facecolor=fill, edgecolor=edge, linewidth=0.6, zorder=2,
    )
    ax.add_patch(nose)
    if label:
        if label_below:
            ax.text(x + width / 2, y - height / 2 - 0.8, label,
                    ha="center", va="top", fontsize=6.8, color="#222222")
        else:
            ax.text(x + width / 2, y + height / 2 + 0.8, label,
                    ha="center", va="bottom", fontsize=6.8, color="#222222")


def draw_lens(
    ax: plt.Axes,
    x: float, y: float,
    width: float = 1.8,
    height: float = 5,
    fill: str = "#A8DADC",
    edge: str = _DEFAULT_EDGE,
) -> None:
    """A simple biconvex lens (vertical ellipse) centered at (x, y)."""
    lens = Ellipse((x, y), width=width, height=height,
                   facecolor=fill, edgecolor=edge, linewidth=0.6,
                   alpha=0.85, zorder=2)
    ax.add_patch(lens)


def draw_mirror(
    ax: plt.Axes,
    x: float, y: float,
    length: float = 4,
    angle_deg: float = 45,
    color: str = "#5C5C5C",
    linewidth: float = 1.4,
) -> None:
    """A mirror as a short diagonal line centered at (x, y)."""
    a = np.deg2rad(angle_deg)
    dx, dy = np.cos(a) * length / 2, np.sin(a) * length / 2
    ax.plot([x - dx, x + dx], [y - dy, y + dy],
            color=color, linewidth=linewidth,
            solid_capstyle="butt", zorder=2)


def draw_modulator(
    ax: plt.Axes,
    x: float, y: float,
    w: float = 10, h: float = 4,
    label: str = "EOM",
    fill: str = "#F4A261",
    edge: str = _DEFAULT_EDGE,
) -> None:
    """A modulator block with a small electrode tab on top.

    (x, y) is the bottom-left of the body. Default fill is the
    Nature Photonics modern orange.
    """
    draw_block(ax, x, y, w, h, label=label, fill=fill, edge=edge,
               fontsize=7, rounding=0.4)
    tab_w, tab_h = 1.5, 1.2
    tab = Rectangle((x + w / 2 - tab_w / 2, y + h), tab_w, tab_h,
                    facecolor=fill, edgecolor=edge, linewidth=0.5, zorder=2)
    ax.add_patch(tab)


def draw_photodetector(
    ax: plt.Axes,
    x: float, y: float,
    radius: float = 2.5,
    label: str = "PD",
    fill: str = "#1E3A78",
    edge: str = _DEFAULT_EDGE,
    label_below: bool = True,
) -> None:
    """A photodetector: half-filled circle (incident light enters from left).

    (x, y) is the center. Default fill is the recurring PD dark-navy.
    """
    bg = Circle((x, y), radius, facecolor="white",
                edgecolor=edge, linewidth=0.6, zorder=2)
    ax.add_patch(bg)
    half = Wedge((x, y), radius, 90, 270,
                 facecolor=fill, edgecolor=edge, linewidth=0.6, zorder=2.1)
    ax.add_patch(half)
    if label:
        if label_below:
            ax.text(x, y - radius - 1.0, label,
                    ha="center", va="top", fontsize=6.8, color="#222222")
        else:
            ax.text(x, y + radius + 1.0, label,
                    ha="center", va="bottom", fontsize=6.8, color="#222222")


def draw_chip_rainbow(
    ax: plt.Axes,
    x: float, y: float,
    w: float, h: float,
    palette: str = "sunset",
    edge: str = _DEFAULT_EDGE,
    edge_linewidth: float = 0.6,
    shadow: bool = True,
    zorder: float = 2,
) -> None:
    """A photonic-chip-like rectangle with a horizontal rainbow gradient.

    (x, y) is the bottom-left corner. The gradient mimics light diffraction
    off an integrated photonic surface.
    """
    cmap = make_cmap(palette)
    grad = np.linspace(0, 1, 256).reshape(1, -1)
    if shadow:
        sh = Ellipse(
            (x + w / 2, y - 0.6),
            w * 0.95, max(0.7, h * 0.18),
            facecolor="#000000", edgecolor="none",
            alpha=0.13, zorder=zorder - 0.5,
        )
        ax.add_patch(sh)
    ax.imshow(
        grad, extent=[x, x + w, y, y + h],
        cmap=cmap, aspect="auto", zorder=zorder, interpolation="bilinear",
    )
    border = Rectangle(
        (x, y), w, h,
        facecolor="none", edgecolor=edge, linewidth=edge_linewidth,
        zorder=zorder + 0.1,
    )
    ax.add_patch(border)


def draw_isometric_layer_stack(
    ax: plt.Axes,
    x: float, y: float, w: float, h: float,
    layers: Sequence[tuple[str, float]],
    depth: float = 6.0,
    skew: float = 0.6,
    edge: str = _DEFAULT_EDGE,
    edge_linewidth: float = 0.5,
    label_layers: bool = True,
    label_fontsize: float = 6.5,
    zorder: float = 2,
) -> None:
    """Pseudo-isometric stacked-layer chip cross-section (TFLN, LTOI, OLED).

    (x, y) is the bottom-LEFT-FRONT corner of the bottom layer. Each
    layer is (color_or_material_key, thickness) — colors may be hex or
    keys of MATERIAL_COLORS. Skew is the dy/dx of the ~30° isometric tilt.

    Reproduces the look of He 2019 Fig. 1a, Wang 2024 Fig. 1, Geravand 2025
    Fig. 4a, Cheng 2025 Fig. 4.
    """
    dx_iso = depth * 0.6
    dy_iso = depth * skew * 0.5
    cur_y = y
    for color_key, thickness in layers:
        color = MATERIAL_COLORS.get(color_key, color_key)
        front = Rectangle(
            (x, cur_y), w, thickness,
            facecolor=color, edgecolor=edge, linewidth=edge_linewidth,
            zorder=zorder,
        )
        ax.add_patch(front)
        # darker side for depth shading
        rgb = np.array(to_rgb(color))
        side_rgb = np.clip(rgb * 0.78, 0, 1)
        side = Polygon(
            [(x + w, cur_y),
             (x + w + dx_iso, cur_y + dy_iso),
             (x + w + dx_iso, cur_y + thickness + dy_iso),
             (x + w, cur_y + thickness)],
            facecolor=side_rgb, edgecolor=edge, linewidth=edge_linewidth,
            zorder=zorder + 0.1,
        )
        ax.add_patch(side)
        # lighter top for depth shading
        top_rgb = np.clip(rgb + (1 - rgb) * 0.18, 0, 1)
        top = Polygon(
            [(x, cur_y + thickness),
             (x + w, cur_y + thickness),
             (x + w + dx_iso, cur_y + thickness + dy_iso),
             (x + dx_iso, cur_y + thickness + dy_iso)],
            facecolor=top_rgb, edgecolor=edge, linewidth=edge_linewidth,
            zorder=zorder + 0.1,
        )
        ax.add_patch(top)
        if label_layers:
            ax.text(x + w + dx_iso + 0.6, cur_y + thickness / 2,
                    color_key, ha="left", va="center",
                    fontsize=label_fontsize, color="#222222")
        cur_y += thickness


def callout(
    ax: plt.Axes,
    target_xy: tuple[float, float],
    text_xy: tuple[float, float],
    text: str,
    color: str = "#222222",
    fontsize: float = 7,
    arrowstyle: str = "-",
) -> None:
    """A thin annotation line from text_xy to target_xy.

    Empirical convention: thin (~0.4-0.5 pt) leader line, no arrowhead
    (use '-' not '-|>'), text in 6-7.5 pt sans-serif outside the panel.
    """
    ax.annotate(
        text,
        xy=target_xy, xytext=text_xy,
        fontsize=fontsize, color=color,
        ha="left", va="center",
        arrowprops=dict(
            arrowstyle=arrowstyle,
            color=color, linewidth=0.5,
            shrinkA=0, shrinkB=2,
        ),
    )


def setup_schematic_axes(
    ax: plt.Axes,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
) -> None:
    """Configure an axis for architecture-diagram drawing.

    Sets equal aspect, given limits, hides ticks/spines.
    """
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")


__all__ = [
    "setup_nature_style", "nature_palette", "make_cmap", "add_panel_label",
    "half_frame", "PALETTES", "MATERIAL_COLORS", "COMB_COLORS",
    "draw_block", "draw_arrow", "draw_optical_path", "draw_glow_beam",
    "draw_laser_source", "draw_lens", "draw_mirror", "draw_modulator",
    "draw_photodetector", "draw_chip_rainbow", "draw_isometric_layer_stack",
    "callout", "setup_schematic_axes",
]
