"""End-to-end smoke test for the v2.0 nature-figure-style skill.
Generates four sample figures exercising different style paths:
  1. line_plot       — closed-box, modern palette, shaded error band
  2. bar_with_errors — half-frame, dual-color, T-cap errorbars
  3. heatmap         — viridis, side colorbar
  4. hybrid_arch     — 3D isometric chip stack on top + 2D vector schematic below
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec

ASSETS = Path("/Users/wishingcat/Research/Nature 绘图/.claude/skills/nature-figure-style/assets")
OUT    = Path("/Users/wishingcat/Research/Nature 绘图/.claude/skills/nature-figure-style/examples")
sys.path.insert(0, str(ASSETS))

from nature_figure_helpers import (  # noqa: E402
    setup_nature_style, half_frame, add_panel_label,
    setup_schematic_axes, draw_isometric_layer_stack, draw_glow_beam,
    draw_block, draw_optical_path, draw_laser_source, draw_photodetector,
    draw_modulator, callout, MATERIAL_COLORS, COMB_COLORS,
    nature_palette,
)

setup_nature_style()
COLORS = nature_palette("nature_photonics_modern")


# ---- 1. line_plot: closed box, shaded band, inward minor ticks ----
def test_line_plot():
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    x = np.linspace(0, 10, 200)
    rng = np.random.default_rng(42)
    for i, (label, mu) in enumerate([("100 K", 1.0), ("200 K", 0.7), ("300 K", 0.4)]):
        y = mu * np.exp(-x/4) * np.cos(2*x) + rng.normal(0, 0.02, x.size)
        sigma = 0.04 + 0.01 * np.sin(x)
        ax.plot(x, y, color=COLORS[i], linewidth=1.0, label=label)
        ax.fill_between(x, y - sigma, y + sigma,
                        color=COLORS[i], alpha=0.20, edgecolor='none')
    ax.set_xlabel('Time delay (ps)')
    ax.set_ylabel(r'$\Delta R/R$ (a.u.)')
    ax.set_xlim(0, 10)
    ax.legend(loc='upper right')
    add_panel_label(ax, 'a')
    fig.savefig(OUT / "v2_line_plot.png", dpi=300)
    fig.savefig(OUT / "v2_line_plot.pdf")
    plt.close(fig)


# ---- 2. bar with errors: half-frame ----
def test_bar():
    fig, ax = plt.subplots(figsize=(3.5, 2.4))
    cats = ["Si", "LNOI", "LTOI", "Hybrid"]
    vals = [3.2, 5.8, 6.4, 7.1]
    errs = [0.3, 0.4, 0.5, 0.4]
    ax.bar(cats, vals, yerr=errs, color=COLORS[:4],
           edgecolor="#222222", linewidth=0.5,
           error_kw=dict(elinewidth=0.6, capsize=2, capthick=0.6, ecolor="#222222"))
    ax.set_ylabel('Q factor ($\\times 10^6$)')
    ax.set_ylim(0, 8)
    half_frame(ax)
    add_panel_label(ax, 'b')
    fig.savefig(OUT / "v2_bar.png", dpi=300)
    plt.close(fig)


# ---- 3. heatmap: viridis with side colorbar ----
def test_heatmap():
    fig, ax = plt.subplots(figsize=(3.8, 2.8))
    rng = np.random.default_rng(0)
    X, Y = np.meshgrid(np.linspace(-3, 3, 200), np.linspace(-2, 2, 150))
    Z = np.exp(-(X**2 + Y**2)/2) + 0.05 * rng.standard_normal(X.shape)
    im = ax.imshow(Z, cmap='viridis', extent=[-3, 3, -2, 2],
                   aspect='auto', origin='lower', interpolation='nearest')
    ax.set_xlabel('Frequency (GHz)')
    ax.set_ylabel('Detuning (MHz)')
    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cbar.set_label('Intensity (a.u.)')
    cbar.ax.tick_params(width=0.5, length=2)
    cbar.outline.set_linewidth(0.5)
    add_panel_label(ax, 'c')
    fig.savefig(OUT / "v2_heatmap.png", dpi=300)
    plt.close(fig)


# ---- 4. hybrid architecture: 3D isometric chip + 2D schematic ----
def test_hybrid():
    fig = plt.figure(figsize=(7.2, 4.4))
    gs = GridSpec(2, 1, height_ratios=[1.4, 1.0], hspace=0.05, figure=fig)

    # Top: 3D isometric LNOI stack with glow beam crossing it
    ax_top = fig.add_subplot(gs[0])
    setup_schematic_axes(ax_top, (0, 60), (0, 22))
    draw_isometric_layer_stack(
        ax_top, x=12, y=4, w=36, h=10,
        layers=[("silicon", 1.5), ("sio2", 0.6),
                ("lnoi", 0.5), ("gold", 0.3)],
        depth=8.0, label_layers=True, label_fontsize=6.5,
    )
    draw_glow_beam(ax_top, (3, 7), (54, 7),
                   color=COMB_COLORS["signal"],
                   core_width=0.9, halo_width=6.0, n_layers=5)
    callout(ax_top, target_xy=(30, 6.5), text_xy=(28, 18),
            text='Optical mode')
    add_panel_label(ax_top, 'a', x=0.005, y=0.99)

    # Bottom: 2D vector measurement schematic
    ax_bot = fig.add_subplot(gs[1])
    setup_schematic_axes(ax_bot, (0, 100), (0, 20))
    draw_laser_source(ax_bot, x=4, y=10, label='1550 nm CW',
                      fill=COMB_COLORS["signal"])
    draw_optical_path(ax_bot, [(14, 10), (38, 10)],
                      role="signal", linewidth=1.4)
    draw_modulator(ax_bot, x=38, y=8, w=14, h=4, label='LN MZM',
                   fill=MATERIAL_COLORS["lnoi_light"])
    draw_optical_path(ax_bot, [(52, 10), (78, 10)],
                      role="signal", linewidth=1.4, arrow=True)
    draw_photodetector(ax_bot, x=82, y=10, label='PD')
    # control / RF feedback (gray dashed)
    draw_optical_path(ax_bot, [(45, 4), (45, 1)],
                      role="control", linewidth=0.9, linestyle='--')
    ax_bot.text(45, 0.5, 'RF drive', ha='center', va='top',
                fontsize=6.5, color="#444444")
    add_panel_label(ax_bot, 'b', x=0.005, y=0.99)

    fig.savefig(OUT / "v2_hybrid_architecture.png", dpi=300)
    fig.savefig(OUT / "v2_hybrid_architecture.pdf")
    plt.close(fig)


if __name__ == "__main__":
    test_line_plot()
    test_bar()
    test_heatmap()
    test_hybrid()
    print("All four sample figures generated in", OUT)
