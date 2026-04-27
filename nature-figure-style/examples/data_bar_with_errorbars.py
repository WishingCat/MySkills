"""Example: Nature-style bar chart with error bars (grouped).

Run:
    python examples/data_bar_with_errorbars.py
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

    groups = ["Si", "SiN", "LN", "LT"]
    cond_a = np.array([12.4, 9.7, 18.6, 21.3])
    cond_b = np.array([15.8, 11.0, 22.5, 24.1])
    err_a = np.array([1.0, 0.8, 1.4, 1.6])
    err_b = np.array([1.2, 0.9, 1.5, 1.8])

    x = np.arange(len(groups))
    width = 0.36

    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    ax.bar(
        x - width / 2, cond_a, width=width,
        color=colors[0], edgecolor="#3C5488", linewidth=0.5, label="Pulsed",
    )
    ax.bar(
        x + width / 2, cond_b, width=width,
        color=colors[1], edgecolor="#3C5488", linewidth=0.5, label="CW",
    )
    ax.errorbar(
        x - width / 2, cond_a, yerr=err_a,
        fmt="none", ecolor="#222222", elinewidth=0.6,
        capsize=2, capthick=0.6,
    )
    ax.errorbar(
        x + width / 2, cond_b, yerr=err_b,
        fmt="none", ecolor="#222222", elinewidth=0.6,
        capsize=2, capthick=0.6,
    )

    ax.set_xticks(x, groups)
    ax.set_ylabel(r"Q factor ($\times10^{6}$)")
    ax.set_xlabel("Platform")
    ax.set_ylim(0, 30)
    ax.legend(loc="upper left")

    add_panel_label(ax, "c")

    out = Path(__file__).resolve().parent / "out_data_bar.png"
    fig.savefig(out, dpi=300)
    fig.savefig(out.with_suffix(".pdf"))
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
