"""Example: Nature-style heatmap with proper colorbar.

Run:
    python examples/data_heatmap.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))
from nature_figure_helpers import (  # noqa: E402
    add_panel_label, make_cmap, setup_nature_style,
)


def main() -> None:
    setup_nature_style()
    cmap = make_cmap("sunset")

    rng = np.random.default_rng(0)
    x = np.linspace(-3, 3, 220)
    y = np.linspace(-2, 2, 160)
    X, Y = np.meshgrid(x, y)
    field = (
        np.exp(-((X - 0.4) ** 2 + (Y + 0.3) ** 2))
        + 0.6 * np.exp(-((X + 1.2) ** 2 + (Y - 0.5) ** 2))
        + 0.05 * rng.normal(size=X.shape)
    )

    fig, ax = plt.subplots(figsize=(3.8, 2.4))

    im = ax.imshow(
        field,
        extent=[x.min(), x.max(), y.min(), y.max()],
        origin="lower", aspect="auto",
        cmap=cmap, interpolation="nearest",
    )

    ax.set_xlabel("Wavenumber (cm$^{-1}$)")
    ax.set_ylabel(r"Detuning $\Delta\nu$ (GHz)")

    cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cbar.set_label("Intensity (a.u.)", labelpad=2)
    cbar.ax.tick_params(width=0.5, length=2)
    cbar.outline.set_linewidth(0.5)

    add_panel_label(ax, "b")

    out = Path(__file__).resolve().parent / "out_data_heatmap.png"
    fig.savefig(out, dpi=300)
    fig.savefig(out.with_suffix(".pdf"))
    print(f"saved: {out}")


if __name__ == "__main__":
    main()
