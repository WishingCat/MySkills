"""Example: Nature-style optical-setup architecture diagram.

A 2D schematic of a fibre-coupled electro-optic measurement setup:

    [Laser] -- fibre --> [EOM] -- fibre --> lens -- free-space --> [PD]

Run:
    python examples/architecture_optical_setup.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_figure_helpers import (  # noqa: E402
    add_panel_label, callout, draw_arrow, draw_block, draw_chip_rainbow,
    draw_laser_source, draw_lens, draw_modulator, draw_optical_path,
    draw_photodetector, setup_nature_style, setup_schematic_axes,
)


def main() -> None:
    setup_nature_style()

    fig, ax = plt.subplots(figsize=(7.2, 2.6))
    setup_schematic_axes(ax, xlim=(0, 100), ylim=(0, 30))

    # 1. Laser
    draw_laser_source(ax, x=4, y=15, width=8, height=4.2,
                      label="1550 nm laser", fill="#3C5488")

    # 2. Optical fibre to modulator (red, solid)
    draw_optical_path(ax, [(13.2, 15), (28, 15)],
                      color="#E63946", linewidth=1.4)

    # 3. Modulator
    draw_modulator(ax, x=28, y=12.8, w=11, h=4.4,
                   label="EOM", fill="#F39B7F")

    # 4. Microwave drive (dashed control line from below)
    draw_optical_path(ax, [(33.5, 6), (33.5, 12.8)],
                      color="#3C5488", linewidth=1.0, linestyle="--")
    ax.text(33.5, 5.2, "RF drive", ha="center", va="top",
            fontsize=6.8, color="#3C5488")

    # 5. Optical fibre to chip
    draw_optical_path(ax, [(39, 15), (52, 15)],
                      color="#E63946", linewidth=1.4)

    # 6. Photonic chip with rainbow gradient
    draw_chip_rainbow(ax, x=52, y=11, w=14, h=8, palette="sunset")
    ax.text(59, 19.6, "Photonic chip", ha="center", va="bottom",
            fontsize=7, color="#222222")

    # 7. Free-space output -> lens -> PD
    draw_optical_path(ax, [(66, 15), (74, 15)],
                      color="#E63946", linewidth=1.4)
    draw_lens(ax, x=75, y=15, width=2, height=5.4)
    draw_optical_path(ax, [(76, 15), (88, 15)],
                      color="#E63946", linewidth=1.4, arrow=True)
    draw_photodetector(ax, x=92, y=15, radius=2.6, label="PD")

    # 8. Read-out electronics block (below PD)
    draw_block(ax, 84, 2, 12, 4, label="Oscilloscope",
               fill="#A8DADC", fontsize=6.8)
    draw_arrow(ax, 92, 12.4, 92, 6.2, color="#222222")

    # 9. Callouts
    callout(ax, target_xy=(75, 15.5), text_xy=(75, 23.5),
            text="Collimating lens")

    add_panel_label(ax, "a", x=0.005, y=0.98)

    out = Path(__file__).resolve().parent / "out_architecture.png"
    fig.savefig(out, dpi=300)
    fig.savefig(out.with_suffix(".pdf"))
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
