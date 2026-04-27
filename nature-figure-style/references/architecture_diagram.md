# 架构 / 示意图完整规则（Nature 风格 / Python 代码生成）

适用于光路图、系统框图、设备示意、流程图、芯片示意等"非数据"的图。本文档基于 22 篇 Nature / Nature Photonics 论文实证（见 `empirical_observations.md`）。

## 0. 四种典型样式（先判断是哪一种）

读用户需求时先归类。四种样式的代码骨架完全不同。

| 样式 | 长什么样 | 何时用 | 用什么画 |
|------|----------|--------|----------|
| **A. 2D 方块/光路图（vector）** | 平面线条图 + 圆角块、激光器/光纤/PD 卡通图 | 算法流程、measurement setup、光路示意、网络拓扑 | matplotlib `Patch` + helpers |
| **B. 3D isometric chip 渲染** | ~30° 等距，多层堆叠，软渐变着色 | TFLN/LTOI/SOI 截面、芯片 hero 图、3D 模块 | `draw_isometric_layer_stack` + 自定义渐变 |
| **C. Hybrid（3D 上 + 2D 下）** | 上半 3D hero，下半 2D 链路 | Nature Photonics **最高频** 大图（Yao, Jin, Cheng, Chen） | A + B 在同一 figure 用 gridspec 拼接 |
| **D. Photo + vector overlay** | 真实显微/卫星/光路实物 + vector 标注 | 强调真实场景（Han 100 km、Paper 03 wrist sensor） | imshow photo + 上层 axes 叠 vector |

**经验**：复杂的 3D 芯片 hero 图 matplotlib 难做到极致。代码画到 80% 就够，剩下的让用户在 Inkscape / Blender 里收尾。

实证观察：Hybrid 模式（C）是 Nature Photonics 最具代表性的混搭——3D 上 + 2D 下让读者既看清物理结构又看清信号链。这种风格几乎是 Nature Photonics 的视觉签名。

## 1. 通用尺寸规则

架构图通常**比数据图大**：单栏 89 mm 仍可，但常用双栏 183 mm 或 1.5 栏 120 mm 以容纳标注。

```python
# 双栏架构图常用尺寸
fig, ax = plt.subplots(figsize=(7.2, 3.5), dpi=300)
ax.set_xlim(0, 100)   # 用任意单位坐标系（不是物理量）
ax.set_ylim(0, 50)
ax.set_aspect('equal')   # 关键：保证圆是圆，方是方
ax.axis('off')           # 架构图不显示坐标轴
```

`set_aspect('equal')` 和 `axis('off')` 是架构图的固定开场，或调用 `setup_schematic_axes(ax, xlim, ylim)`。

## 2. 配色（架构图配色逻辑）

**架构图配色逻辑和数据图不同**。数据图要色彩对比，架构图要 **柔和、有层次** + 材料语义。

### 2a. Material color recipe（实证最稳）

3D / isometric chip 的材料配色高度复用，直接 `from nature_figure_helpers import MATERIAL_COLORS`：

| 材料 | hex | 来源 |
|------|-----|------|
| Si 衬底 | `#1F7C3A` | He 2019, Geravand 2025 |
| LNOI 薄膜铌酸锂 | `#D63E8C` (深) / `#E58FB1` (浅) | He 2019, Feng 2024 |
| LTOI 钽酸锂 | `#5E60CE` | Wang 2024 |
| SiO₂ 埋氧 | `#E8D8B0` | He 2019, Cheng 2025 |
| 金电极 | `#E5B83A` / `#F2C83A` | Hu 2021, Feng 2024, Yao 2025 |
| Cu 走线 | `#C97B3D` | Geravand 2025 |
| 波导发光 / mode | `#2A9D8F` (teal) | Yao 2025, Hu 2021 |
| PD / 电子学 | `#1E3A78` | Geravand 2025 |
| Sapphire | `#9DC8E8` |  |
| Passive 灰 | `#BFBFBF` | 通用 |

### 2b. 双梳 / 双激光器配色公约（实证）

`from nature_figure_helpers import COMB_COLORS`：

| 角色 | hex | 来源 |
|------|-----|------|
| comb 1 / signal / pump | `#D6322B` 红 | Giorgetta, Han, Jin |
| comb 2 / LO / probe | `#1F5FAE` 蓝 | 同上 |
| beat / RF / heterodyne | `#7E3FA8` 紫 | Giorgetta |
| SHG / 第二激光 / aux | `#2A8E3A` 绿 | Cheng, Jin |
| EDFA / pump-fiber | `#F0C03A` 黄 | Han, Cheng |
| 控制 / feedback | `#888888` 灰（虚线） | 全员 |

`draw_optical_path(ax, points, role="signal")` 直接用 role 名取色。

### 2c. 一般用色

| 用途 | 推荐 |
|------|------|
| 主元素填充（功能块） | `Tiffany` / `Sakura` / `Morandi` 中段（柔和） |
| 强调元素（输入/输出） | `Sunset` 暖色 |
| 背景 | 纯白 |
| 边框、文字 | 深灰 `#222222`（不是纯黑） |

## 3. 样式 A：方块流程图

适合系统框图、算法流程、信号链。

### 模式

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Module  │ →  │  Module  │ →  │  Output  │
│    A     │    │    B     │    │          │
└──────────┘    └──────────┘    └──────────┘
```

### 代码骨架

```python
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(7.2, 2.4), dpi=300)
ax.set_xlim(0, 100); ax.set_ylim(0, 30); ax.set_aspect('equal'); ax.axis('off')

def add_block(ax, x, y, w, h, label, fill='#A8DADC', edge='#222222', fontsize=8):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle="round,pad=0,rounding_size=1.2",
                         linewidth=0.6, edgecolor=edge, facecolor=fill)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2, label,
            ha='center', va='center', fontsize=fontsize, color='#222222')

def add_arrow(ax, x1, y1, x2, y2, color='#222222'):
    arr = FancyArrowPatch((x1, y1), (x2, y2),
                          arrowstyle='-|>', mutation_scale=8,
                          linewidth=0.8, color=color)
    ax.add_patch(arr)

# 三个功能块
add_block(ax, 5, 12, 18, 8, 'Source\n(laser)', fill='#FFE5B4')
add_block(ax, 35, 12, 18, 8, 'Modulator', fill='#A8DADC')
add_block(ax, 65, 12, 18, 8, 'Detector', fill='#F46197')

# 连接箭头
add_arrow(ax, 23, 16, 35, 16)
add_arrow(ax, 53, 16, 65, 16)
```

### 风格要点

- **圆角**用 `boxstyle="round,pad=0,rounding_size=1.2"`，rounding_size 约为短边的 8–15%
- **边框 0.5–0.8 pt**，颜色用深灰 `#222222`，不要纯黑
- **填充淡饱和**色（饱和度 < 60%），不要填高饱和荧光色
- **箭头**用 `'-|>'` 实心三角，线宽 0.8 pt，比块边线略粗一点点
- **多层级关系**用同色族不同明度区分（输入端浅，处理端中，输出端深）

## 4. 样式 B：2D 光路图

适合光学实验示意。

### 元素图谱

| 元素 | 几何 | 注意 |
|------|------|------|
| 激光器 | 矩形带斜方块（"光腔"指向） | 标注波长 |
| 自由空间光路 | 直线 / 弯折线 | 实线 = 主光路，虚线 = 反馈/控制 |
| 透镜 | 椭圆或两个圆弧 | 标注焦距 |
| 反射镜 | 短斜线 | 反射角 45° 是默认 |
| 分束器 | 45° 短斜线（半反半透） | 路径分两路 |
| 调制器 / EOM | 矩形带电极符号 | 标注电压来源 |
| 光纤 | 双线（外护套 + 纤芯）或单条粗弯曲线 | 弯曲半径要平滑 |
| 检测器 / PD | 圆形带半月填充 | 标注 PD/APD/SNSPD |
| 振荡器 / 频谱仪 | 带波形小图标的矩形 | |

### 代码骨架

```python
from nature_figure_helpers import (
    draw_laser_source, draw_optical_path, draw_lens,
    draw_modulator, draw_photodetector, add_panel_label
)

fig, ax = plt.subplots(figsize=(7.2, 3.0), dpi=300)
ax.set_xlim(0, 100); ax.set_ylim(0, 40); ax.set_aspect('equal'); ax.axis('off')

# 激光器
draw_laser_source(ax, x=5, y=20, label='1550 nm laser')
# 光纤路径
draw_optical_path(ax, [(15, 20), (30, 20)], color='#E63946', linewidth=1.4)
# 调制器
draw_modulator(ax, x=30, y=18, w=10, h=4, label='EOM')
# 输出光路
draw_optical_path(ax, [(40, 20), (60, 20)], color='#E63946', linewidth=1.4)
# 透镜
draw_lens(ax, x=60, y=20)
# 探测器
draw_photodetector(ax, x=80, y=20, label='PD')
draw_optical_path(ax, [(64, 20), (80, 20)], color='#E63946', linewidth=1.4,
                  arrow=True)

add_panel_label(ax, 'a', x=0.02, y=0.98)
```

### 风格要点

- **光路用饱和色**（红 `#E63946` 是激光经典色，绿 `#5CAD5E` 是泵浦或第二激光，蓝 `#3C5488` 是参考路径）
- **路径方向用箭头**，但不是每段都加，主要在关键节点（输入端、输出端、分支处）
- **元件标注**优先写在元件正下方或正上方，标签和元件距离约 1–2 倍元件高度
- **辅助光路（控制信号、反馈）用虚线**：`linestyle='--', dashes=(3, 2)`
- **元件用统一的"线条美学"**：所有元件边框线宽相同（0.6–0.8 pt），所有路径线宽相同（1.2–1.4 pt）

## 5. 样式 C：Hybrid（3D 上 + 2D 下）— Nature Photonics 招牌混搭

实证：这是 Nature Photonics 大图的 **最高频** 模式。上半放 3D hero（让读者看清物理结构），下半放 2D measurement schematic 或链路（让读者看清信号流）。

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from nature_figure_helpers import (
    setup_nature_style, setup_schematic_axes,
    draw_isometric_layer_stack, draw_glow_beam,
    draw_block, draw_optical_path, draw_laser_source,
    draw_photodetector, add_panel_label,
    MATERIAL_COLORS, COMB_COLORS,
)
setup_nature_style()

fig = plt.figure(figsize=(7.2, 5.0), dpi=300)
gs = GridSpec(2, 1, height_ratios=[1.4, 1.0], hspace=0.05)

# 上半：3D isometric chip（hero）
ax_top = fig.add_subplot(gs[0])
setup_schematic_axes(ax_top, (0, 60), (0, 25))
draw_isometric_layer_stack(
    ax_top, x=10, y=4, w=40, h=10,
    layers=[("silicon", 1.5), ("sio2", 0.6),
            ("lnoi", 0.5), ("gold", 0.3)],
    depth=8.0, label_layers=True,
)
draw_glow_beam(ax_top, (5, 8), (52, 8),
               color=COMB_COLORS["signal"],
               core_width=0.8, halo_width=6.0)
add_panel_label(ax_top, 'a', x=0.01, y=0.98)

# 下半：2D vector measurement schematic
ax_bot = fig.add_subplot(gs[1])
setup_schematic_axes(ax_bot, (0, 100), (0, 20))
draw_laser_source(ax_bot, x=4, y=10, label='1550 nm CW',
                  fill=COMB_COLORS["signal"])
draw_optical_path(ax_bot, [(14, 10), (38, 10)],
                  role="signal", linewidth=1.4)
draw_block(ax_bot, 38, 6, 14, 8, label='LN MZM',
           fill=MATERIAL_COLORS["lnoi_light"])
draw_optical_path(ax_bot, [(52, 10), (78, 10)],
                  role="signal", linewidth=1.4, arrow=True)
draw_photodetector(ax_bot, x=82, y=10, label='PD')
add_panel_label(ax_bot, 'b', x=0.01, y=0.98)
```

### 关键技巧：3D isometric chip 的技术要点

1. **等距投影**：`set_aspect('equal')`，按 30° 等距画 face/side/top 三个多边形（`draw_isometric_layer_stack` 已封装）。
2. **层间深度阴影**：side face 用 `rgb*0.78`，top face 用 `rgb + (1-rgb)*0.18`。这是 helper 默认做的。
3. **彩虹渐变**（仿光子芯片表面光衍射效果）：用 `draw_chip_rainbow(ax, x, y, w, h, palette='sunset')`。
4. **光束 / 体积光**：用 `draw_glow_beam(ax, p1, p2)`。它会画 5 层从粗到细、从透明到不透明的同色 stroke + 中心 core line，模拟 Kalinin 2025 / Dinani 2025 / Jin 2025 hero 风格。
5. **阴影**：在元件正下方画一个半透明灰色椭圆（helper 里 `draw_chip_rainbow` 自带 `shadow=True` 选项）。
6. **金属/玻璃反光**：在元件顶部画一条短的浅色长条（高光带）。

### 何时认输

如果用户要的是"像 Nature 那种 hero 芯片图"——**不要硬撑**。matplotlib 能做到 80% 像，剩下的告诉用户：
- 把代码出图存为 SVG
- 用 Inkscape 打开
- 手工加渐变、玻璃质感、HDR 高光、reflection
- 或者用 Blender 真做 3D 渲染

代码里把基础形状摆对就行，不要为了做出"金属质感"写一百行 Bezier 曲线——那是反生产力的。

## 5b. 样式 D：Photo + vector overlay

实证：把真实显微 / 光路实物 / 卫星图叠加到 vector 标注上是 Nature Photonics 标志性做法（Han 2024 卫星航拍 + 光路、Paper 03 wrist sensor、Cheng 2025 实物 inset）。

```python
import matplotlib.image as mpimg
from nature_figure_helpers import callout, COMB_COLORS

fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=300)
img = mpimg.imread('chip_microscope.png')
ax.imshow(img, extent=[0, 100, 0, 60])
ax.set_xlim(0, 100); ax.set_ylim(0, 60)
ax.set_aspect('equal'); ax.axis('off')

# 在实拍上叠 vector 元素
ax.plot([20, 80], [30, 30], color=COMB_COLORS["signal"],
        linewidth=2.0, alpha=0.9)
callout(ax, target_xy=(50, 30), text_xy=(60, 50),
        text='LN waveguide')
```

技巧：
- 实拍图常 desaturate（`PIL.ImageEnhance.Color(img).enhance(0.5)`）以让 vector 标注醒目
- Vector 颜色和 schematic 部分用同一套 MATERIAL_COLORS 保持视觉一致
- 实拍区永远配 white scale bar（右下角）+ 黑色 0.5 pt 边框

## 6. 子图标号 / panel labels

和数据图同款规则：

```python
ax.text(0.02, 0.98, 'a', transform=ax.transAxes,
        fontsize=9, fontweight='bold', va='top', ha='left')
```

但架构图常常是单个大图占整张 figure，没有子图。这时 panel label 仍然贴左上角的画布坐标。

## 7. 标注（callout）

架构图标注比数据图重，常需要 callout 引线指向元件细节。

```python
def callout(ax, target_xy, text_xy, text, color='#222222'):
    ax.annotate(text, xy=target_xy, xytext=text_xy,
                fontsize=7, color=color,
                arrowprops=dict(arrowstyle='-', color=color,
                                linewidth=0.5, shrinkA=0, shrinkB=2))

callout(ax, target_xy=(45, 22), text_xy=(50, 32),
        text=r'$\lambda/4$ wave plate')
```

引线要细（0.5 pt），尽量短，不要交叉。

## 8. 排版构图原则

- **从左到右、从上到下**呈现信号流（西方阅读习惯）
- **主元件居中**，辅助元件靠边
- **留白要够**：元件之间至少 1 倍元件高度的间距
- **避免对角线**：除非必须，元件中心连线尽量水平/垂直/45°，不要任意角度
- **对齐网格**：心里画一个 5×5 或 10×10 的隐形网格，所有元件中心都落在网格点上

## 9. 完整示例

见 `examples/architecture_optical_setup.py`：一个完整的光纤光学实验装置示意图，可直接跑。

## 10. 反例速查

| 反例 | 改成 |
|------|------|
| 满图都是同一个色（一锅蓝） | 至少分 3 个色族（输入/处理/输出） |
| 元件圆角半径忽大忽小 | 全部统一 `rounding_size` |
| 直角箭头一会上一会下 | 主流向统一一个方向 |
| 标注字号 5 pt 看不清 | 至少 6.5 pt |
| 元件名缩写没解释（"DUT"、"AWG"） | 第一次出现写全称 + (DUT) |
| 阴影深得像油画 | 阴影 `alpha < 0.2` |
| 路径线宽比元件边线还细 | 路径要比边线粗 |
