---
name: nature-figure-style
version: 2.0.0
description: "Nature 期刊（Nature/Nature Photonics/Nature Communications 等）的两类绘图风格规则与可执行模板：数据图表（matplotlib）和架构图/示意图（Python/TikZ）。当用户要求画 Nature 风格的论文配图、数据图、折线图、柱状图、热力图、谱图、架构图、schematic、光路图、设备示意图、流程框图，或要求复刻 Nature/Science 论文风格、做投稿正图、制图、figure，又或者直接说『按 Nature 风格画』『论文配图风格』『paper figure』时务必使用本 skill。本 skill 包括：基于 22 篇 Nature/Nature Photonics 论文实证观察的尺寸/字号/线宽/坐标轴规范、recurring 配色策略与 material color recipe、可直接 plt.style.use 的 mplstyle、可调用的架构图组件函数（含 isometric chip、glow beam）、以及成品检查清单。"
---

# nature-figure-style

复刻 **Nature 系列期刊**论文配图风格的工作集。本 skill v2.0 的所有数值规则都基于 `/Users/wishingcat/Research/Nature 绘图/Nature 期刊绘图风格提取/figures_extracted/` 中 22 篇 Nature / Nature Photonics 论文的实证观察（2019–2026），见 `references/empirical_observations.md`。

## 触发后的工作流（按这个顺序走）

```
用户给图任务
    ↓
判断是『数据图表』还是『架构/示意图』
    ↓
┌─────────────────┴──────────────────┐
│                                    │
数据图表                          架构/示意图
(折线/柱状/热力/谱)                (光路/系统/方块流程/3D 芯片)
│                                    │
1. setup_nature_style()              1. 决定：A. 2D vector 块图
   （读 assets/nature.mplstyle）         B. 3D isometric chip
2. 读 references/data_plot.md            C. 混合 (3D 上 + 2D 下)
3. 选色：默认 nature_photonics_modern  2. 读 references/architecture_diagram.md
   （Yao 2025 / Jin 2025 复用率最高）  3. 用 assets/nature_figure_helpers.py
4. 出图后跑 references/checklist.md      中的组件函数 + MATERIAL_COLORS
                                       + COMB_COLORS
                                     4. 选色：见 references/color_palettes.md
                                     5. 出图后跑 references/checklist.md
```

**第一步永远是判断类型**，因为两类风格走完全不同的代码路径。混合型（一张大 figure 里既有架构又有数据子图）按子图分别处理。

## 核心不变量（无论哪类图都要满足）

实证观察：22 篇里 100% 的论文都遵守这五条；违反任何一条都会让人一眼看出"不像 Nature"：

1. **字体一律 sans-serif**（Helvetica / Arial / Liberation Sans）。绝对不要用 serif（Times New Roman 是 Word 的味道，不是论文图的味道）。
2. **panel 标号是粗体小写 a / b / c**（不是 A、不是 (a)、不是 1.2.3）。固定贴左上角，与子图对齐，9–10 pt 加粗。
3. **正图字号 6–9 pt**：刻度数字 6–7 pt，轴标签 7–8 pt，panel 字母 9–10 pt 加粗。这是按 Nature 实际印刷尺寸来的——单栏 89 mm 宽，双栏 183 mm 宽。
4. **Tick 方向是 inward**（`direction='in'`）。这是 22 篇里 100% 命中的最稳定特征。注意：本 skill 的旧版（v1.0）说 outward 是默认——那是错的，已修正。
5. **线宽要细**：坐标轴 0.6 pt，数据线 0.8–1.2 pt，参考虚线 0.5–0.7 pt。粗线条是 PPT 味，不是论文味。

## 关于 spine（轴线方框）的两个流派

实证观察的一个意外发现：现代 Nature Photonics 用 **四面闭合方框** 比 L+B 半框更常见。两个流派同时存在，按场景选：

| 场景 | 推荐 | 例子 |
|------|------|------|
| 谱图（光谱、PSD、频谱） | 闭合方框 | He 2019, Cheng 2025, Geravand 2025 |
| log-log 图（noise、Allan deviation） | 闭合方框 | Cheng 2025, Jin 2025 |
| 极坐标、密集时间序列 | 闭合方框 | Geravand 2025 |
| 简洁的折线图、柱状图 | L+B 半框 | Hu 2021, Feng 2024（部分），早期 Nature Photonics |
| 散点图（强调数据轮廓） | L+B 半框 | Paper 11, Paper 13 |

**本 skill 默认走闭合方框**（mplstyle 里 `axes.spines.top/right: True` + `xtick.top/ytick.right: True`）。要 L+B 半框时显式调用 `half_frame(ax)`。

## 配色

### 数据图：默认 `nature_photonics_modern`

实证观察：22 篇里 2024–2026 的 Nature Photonics 共有 7 篇用了非常接近的 5 色离散调色板：

```python
nature_photonics_modern = [
    "#E63946",  # 红 - 主信号 / 实验组
    "#F4A261",  # 橙 - 副信号 / 中间结果
    "#E9C46A",  # 金黄 - 参数 3
    "#2A9D8F",  # 青绿 - 参考 / 模拟
    "#264653",  # 深蓝 - baseline / dark trace
    "#7E3FA8",  # 紫 - 5 类以上扩展
    "#F46197",  # 粉 - 5 类以上扩展
    "#888888",  # 灰 - 5 类以上扩展
]
```

锚定论文：Yao 2025、Jin 2025、Kalinin 2025、Wang 2024、Geravand 2025（部分）。

**setup_nature_style()** 默认就用这套。要切换：
- `setup_nature_style("nature_photonics_classic")` — 早期 NPhoton 习惯（红+蓝+绿+橙）
- `setup_nature_style("nature_journal")` — NPG / ggsci 8 色，更偏 Cell / Nature Methods 生物风
- `setup_nature_style("morandi")` / `("monet")` — 严肃 / 柔和 子刊审美

### 连续 colormap

实证观察：
- **viridis** 用于 spectrogram、2D 测量矩阵、hyperspectral cube — 安全默认
- **inferno / magma** 用于强度图、streak camera、super-resolution（Paper 11、Paper 13、Dinani 2025）
- **eye diagram** 几乎总是黑底 + cyan-green density（He 2019、Geravand 2025、Wang 2024）
- **diverging RdBu_r** 用于带正负的物理量（band structure、相位、χ⁽²⁾）— Paper 10
- **viridis 的暖偏版** 也常见于 Jin 2025、Yao 2025 — 即不那么蓝紫的 cyan→yellow→red ramp
- **不用 jet**（除非物理量本身需要 hue 对应 wavelength，如 Geravand polar）

详见 `references/color_palettes.md`。

### 架构图：material color recipe

实证观察：3D / isometric 芯片图复用率极高的材料配色（见 `MATERIAL_COLORS` 字典）：

| 材料 | hex | 来源 |
|------|-----|------|
| Si 衬底 | `#1F7C3A` | He 2019, Geravand 2025 |
| LNOI / 薄膜铌酸锂 | `#D63E8C` (深) / `#E58FB1` (浅) | He 2019, Feng 2024 |
| LTOI / 钽酸锂 | `#5E60CE` | Wang 2024 |
| SiO₂ 埋氧 | `#E8D8B0` | He 2019, Cheng 2025 |
| 金电极 | `#E5B83A` / `#F2C83A` | Hu 2021, Feng 2024, Yao 2025 |
| Cu 走线 | `#C97B3D` | Geravand 2025 |
| 波导发光 / 模式 | `#2A9D8F` (teal) | Yao 2025, Hu 2021 |
| PD / 电子学 | `#1E3A78` | Geravand 2025 |
| Passive 灰 | `#BFBFBF` | 通用 |

直接 `from nature_figure_helpers import MATERIAL_COLORS; MATERIAL_COLORS["lnoi"]`。

### 双梳 / 双激光器配色公约

实证观察：dual-comb / pump-probe 论文有 stable color convention（见 `COMB_COLORS`）：

```
红  #D6322B = comb 1 / signal / pump
蓝  #1F5FAE = comb 2 / LO / probe
紫  #7E3FA8 = beat / RF / heterodyne
绿  #2A8E3A = SHG / 第二激光 / auxiliary
黄  #F0C03A = EDFA / pump-fiber path
灰  #888888 = feedback / control（虚线）
```

锚定论文：Giorgetta 2024、Han 2024、Jin 2025、Cheng 2025、Hu 2021。

## 数据图表（matplotlib）

**第 0 步——加载样式**：
```python
from nature_figure_helpers import setup_nature_style, add_panel_label
setup_nature_style()                # 默认 nature_photonics_modern
# 或者只加载样式不换 cycle：
# import matplotlib.pyplot as plt
# plt.style.use('<skill_dir>/assets/nature.mplstyle')
```

详细规则见 `references/data_plot.md`。它讲：
- 坐标轴样式（4-spine vs L+B 何时用）、tick 方向、minor ticks
- 双 y 轴（颜色配对）、log 轴、polar 的具体参数
- legend 位置和样式（无框、inline 替代）
- 误差棒 vs 误差填充带（推荐 band，alpha 0.15–0.25）
- 常见图型（折线、柱状、热力、散点、误差带、eye diagram、Allan deviation）的 matplotlib 模板

## 架构 / 示意图

详细规则见 `references/architecture_diagram.md`。它讲：
- **三种典型样式**：A. 2D 方块/光路图（vector）；B. 3D isometric chip 渲染；C. hybrid（3D 上 + 2D 下，或 photo + vector）— 这是 Nature Photonics 标志性混搭。
- 组件几何（圆角矩形、立体盒、光纤弯曲、激光器图标）
- 光束两种画法：vector 用 `draw_optical_path`（细色线），3D hero 用 `draw_glow_beam`（多层透明 halo）
- 标注引线（callout）的位置策略：thin (0.4–0.5 pt) leader line, 无箭头, 终点小圆点
- 何时用 matplotlib，何时建议外接 Inkscape / Blender

可调用工具：`assets/nature_figure_helpers.py` 里有：
- `draw_block(ax, ...)` — 圆角矩形功能块
- `draw_optical_path(ax, points, role="signal")` — 路径，按 COMB_COLORS 取色
- `draw_glow_beam(ax, p1, p2, ...)` — 3D hero 的发光体积光束（Kalinin 风格）
- `draw_laser_source(ax, ...)` / `draw_lens` / `draw_mirror` / `draw_modulator` / `draw_photodetector`
- `draw_chip_rainbow(ax, ...)` — 渐变芯片表面
- `draw_isometric_layer_stack(ax, ..., layers=[("silicon", 1.5), ("sio2", 0.6), ("lnoi", 0.4), ("gold", 0.3)])` — 多层 chip 截面（He 2019 / Wang 2024 风）
- `add_panel_label(ax, 'a')` — 加粗小写 panel 标号
- `callout(ax, target, text_xy, text)` — 细引线标注
- `MATERIAL_COLORS`、`COMB_COLORS` 字典

## 完成后的检查

每张图出完后，必须照 `references/checklist.md` 走一遍验证。不验证就报告完成 = 80% 概率会有破坏 Nature 感的小毛病（比如 tick 朝外了、panel label 是大写、legend 有多余边框）。

## 参考资料

- `references/empirical_observations.md` — **22 篇 Nature/NPhoton 论文的实证观察原始记录**（v2.0 新增；所有数值规则的依据）
- `references/data_plot.md` — 数据图表完整规则
- `references/architecture_diagram.md` — 架构图完整规则
- `references/color_palettes.md` — 配色场景化建议
- `references/checklist.md` — 出图后的检查清单
- `assets/nature.mplstyle` — matplotlib 样式文件
- `assets/nature_figure_helpers.py` — 架构图组件函数 + 配色字典
- `examples/` — 可直接跑的示例（折线、柱状、热力、架构图）

## 风格的"为什么"（写给将来调优的自己）

Nature 系列论文图的克制感来源于三条物理约束：
1. **印刷尺寸小**——单栏 89 mm，所以字号必须 6 pt+，线宽必须 0.5 pt+，不然印出来糊。
2. **黑白可读**——审稿/打印常是黑白，所以信息层级不能只靠颜色，要靠 marker 形状、线型、文字标注。
3. **同行评审审美**——审稿人看过几千张图，过度装饰（阴影、3D、渐变背景）会被认为不专业。但 *局部* 的 3D（chip 截面、hero schematic）反而是高分项，因为它能让读者快速理解物理结构。这就是为什么 Nature Photonics 喜欢 "3D 上 + 2D 下" 的混搭。

理解这三条约束就理解了所有规则的来源；遇到本 skill 没覆盖的边角情况，按这三条原则推导即可，并优先回去翻 `references/empirical_observations.md` 看是否有现成例子。
