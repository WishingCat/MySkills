---
name: "nature-plot-style"
description: "Use when the user wants a Matplotlib scientific figure that matches the dominant style distilled from `/Users/wishingcat/Research/Nature 绘图`: Helvetica 6 pt text, thin axes, inward ticks, compact wide layouts, pastel wavelength-like colors, and SVG-first export from CSV, arrays, or table data."
---

# Nature Plot Style

## When to use
- Generate a new scientific figure that should resemble the dominant plotting style in `/Users/wishingcat/Research/Nature 绘图`.
- Restyle an existing Matplotlib script so it looks like the lab's publication figures.
- Turn CSV/TSV/Excel/inline arrays into compact publication-style line plots, comparison plots, scatter plots, heatmaps, or lightweight 3D figures.

This skill reflects the dominant pattern in the codebase, not every outlier. Prefer the common publication style unless the user explicitly asks to mimic a specific script.

## Default workflow
1. Read the user data and infer the plot family from column meanings before asking questions.
2. Default to Matplotlib plus `pandas`/`numpy`.
3. Use English labels and explicit units unless the user requests Chinese labels.
4. Build the figure with a compact canvas first; only enlarge when labels, legends, or dense data require it.
5. Export SVG by default. Add a high-DPI PNG only if the user asks or if raster output is clearly useful.

## Core style rules
- Font: `Helvetica`
- Base font size: `6`
- Axes label size: `6`
- Legend font size: `6` by default, sometimes `4` for dense multi-curve figures
- Axes linewidth: `0.25`
- Tick direction: inward on both axes
- Major tick size: `2`
- Major tick width: `0.25`
- Grid: off by default
- Title: usually omitted
- Legend frame: off
- Save with `bbox_inches="tight"`
- Prefer `plt.tight_layout()` unless a custom layout makes it worse

Use these rcParams unless the figure type needs a tiny adjustment:

```python
plt.rcParams.update({
    "font.family": "Helvetica",
    "font.size": 6,
    "lines.linewidth": 0.5,
    "lines.markersize": 0,
    "lines.markeredgewidth": 0.7,
    "axes.labelsize": 6,
    "axes.linewidth": 0.25,
    "axes.grid": False,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 2,
    "ytick.major.size": 2,
    "xtick.major.width": 0.25,
    "ytick.major.width": 0.25,
    "xtick.labelsize": 6,
    "ytick.labelsize": 6,
    "legend.fontsize": 6,
    "legend.frameon": False,
})
```

## Palette
Use a soft wavelength-ordered palette instead of harsh default colors. Reuse adjacent hues for ordered multi-curve data.

```python
WAVELENGTH_SORTED_COLORS = [
    (149/255, 117/255, 205/255),
    (121/255, 134/255, 203/255),
    (100/255, 181/255, 246/255),
    (79/255, 195/255, 247/255),
    (77/255, 208/255, 225/255),
    (77/255, 182/255, 172/255),
    (129/255, 199/255, 132/255),
    (174/255, 213/255, 129/255),
    (220/255, 231/255, 117/255),
    (255/255, 241/255, 118/255),
    (255/255, 213/255, 79/255),
    (255/255, 183/255, 77/255),
    (255/255, 138/255, 101/255),
    (229/255, 115/255, 115/255),
    (240/255, 98/255, 146/255),
]
```

Practical defaults:
- Main single curve: cyan-blue region such as `WAVELENGTH_SORTED_COLORS[3]` or `[4]`
- Ground truth vs reconstruction: blue or cyan versus coral/red
- Reference or baseline series: muted gray like `#99A3A8`, `#CFCFCF`, or `lightgray`
- Heatmaps: build a custom colormap from 4-7 adjacent palette colors, often with slightly reduced saturation

## Figure family rules

### 1. Single or multi-curve spectrum plots
- This is the dominant style in the codebase.
- Prefer `figsize` around `(3.0, 2.0)`, `(3.6, 2.0)`, `(4.3, 2.0)`, `(4.8, 1.85)`, or `(6.3, 1.2)` depending on density.
- Use line widths in the `0.3` to `0.7` range.
- Usually no markers for dense spectra.
- Set explicit x/y limits and ticks instead of relying on auto-scaling.
- Use legends only when the series identity is not obvious.

### 2. Comparison curves with two y-axes
- Use `twinx()` when units differ but the x-axis is shared.
- Keep both axes thin and minimalist.
- Hide the secondary tick labels entirely if the second axis is only structural.
- Merge legends across axes when the figure is small.

### 3. Scatter or benchmark comparison plots
- Use small hollow markers first: `o`, `s`, `D`, `^`, `h`, `*`.
- Keep marker sizes restrained.
- Use text annotations sparingly and place them with small manual offsets.
- Log scales are acceptable when the data spans orders of magnitude.

### 4. Heatmaps and contour overlays
- Stay with Helvetica 6 pt unless the source plot is clearly an outlier.
- Prefer `imshow` plus optional contour lines and a slim colorbar.
- Keep the colorbar label short and unit-bearing.
- Use accent markers or short text labels in palette-matched colors.

### 5. 3D plots
- Only use 3D when the user data is inherently spatial or matrix-like and 2D would lose meaning.
- This family exists in the codebase but is not the dominant publication style.
- Keep backgrounds clean and colors soft; avoid flashy shading.

## Layout conventions
- Most figures are wider than they are tall.
- Labels are concise and usually unit-bearing, for example `Wavelength (nm)` or `Normalized intensity (dB)`.
- Many figures intentionally omit a title.
- Legends commonly sit at `upper right`, `upper center`, or just above the plot with `ncol=2` or `ncol=3`.
- Use manual ticks for scientific readability.
- Keep all spines visible unless a specific figure benefits from hiding one.

## Annotation conventions
- Use annotations only for real emphasis: directional arrows, highlighted peaks, special points, or panel guidance.
- Match annotation color to the target curve where possible.
- Keep arrow styles simple: `->` or `-|>`.

## What not to do by default
- Do not use seaborn defaults.
- Do not use heavy grids.
- Do not use thick spines or large fonts.
- Do not use oversized legends or decorative shadows.
- Do not default to dark backgrounds.
- Do not switch to Chinese labels unless the user asks.

## Output expectations
When the user gives data and asks for a figure in this style:
- produce runnable Python code unless they ask only for the image,
- generate the figure file,
- default the output to `.svg`,
- mention any assumptions about column mapping or units,
- keep the code easy to edit for future datasets.
