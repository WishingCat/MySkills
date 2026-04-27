"""Example: Nature-style line plot with multiple traces and shaded errorbar.

Run from the skill directory:
    cd /path/to/.claude/skills/nature-figure-style
    python examples/data_line_plot.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_figure_helpers import (  # noqa: E402
    add_panel_label, nature_palette, setup_nature_style,
)


def main() -> None:
    setup_nature_style("nature_journal")
    colors = nature_palette("nature_journal")

    rng = np.random.default_rng(2026)
    x = np.linspace(0, 10, 200)
    truths = [
        np.sin(x) * np.exp(-x / 8),
        np.sin(x + 0.6) * np.exp(-x / 6),
        np.sin(x + 1.2) * np.exp(-x / 4),
    ]
    labels = ["Sample A", "Sample B", "Sample C"]

    fig, ax = plt.subplots(figsize=(3.5, 2.6))

    for y, label, c in zip(truths, labels, colors):
        noise = rng.normal(scale=0.04, size=y.shape)
        y_obs = y + noise
        ax.plot(x, y_obs, color=c, linewidth=1.2, label=label)
        ax.fill_between(
            x, y_obs - 0.06, y_obs + 0.06,
            color=c, alpha=0.18, edgecolor="none",
        )

    ax.set_xlabel("Time (ns)")
    ax.set_ylabel("Amplitude (a.u.)")
    ax.set_xlim(0, 10)
    ax.legend(loc="upper right")

    add_panel_label(ax, "a")

    out = Path(__file__).resolve().parent / "out_data_line_plot.png"
    fig.savefig(out, dpi=300)
    fig.savefig(out.with_suffix(".pdf"))
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
