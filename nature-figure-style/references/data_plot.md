# 数据图表完整规则（Nature 风格 / matplotlib）

适用于折线、柱状、散点、热力、谱图、箱线图、双 y 轴、log 轴、误差带、inset 等所有数据图。

## 0. 三个动作的固定开场

任何数据图脚本第一步必须做这三件事，缺一不可：

```python
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# 1. 加载 Nature 样式 + 默认调色板（推荐）
from nature_figure_helpers import setup_nature_style
setup_nature_style()                # 默认 nature_photonics_modern 5 色
# 或者只加载样式不换 cycle：
# plt.style.use(str(Path(__file__).resolve().parents[1] / 'assets' / 'nature.mplstyle'))

# 2. 显式列出当前默认调色板（实证最高频；Yao 2025 / Jin 2025 / Kalinin 2025）
nature_photonics_modern = ["#E63946", "#F4A261", "#E9C46A", "#2A9D8F", "#264653",
                            "#7E3FA8", "#F46197", "#888888"]

# 3. 设定画布尺寸（按 Nature 单/双栏）
fig, ax = plt.subplots(figsize=(3.5, 2.6), dpi=300)  # 单栏 89mm ≈ 3.5 inch
# 双栏：figsize=(7.2, 2.8 ~ 4.5)
```

## 1. 画布尺寸（按印刷栏宽来）

| 用途 | 宽度 | 高度建议 |
|------|------|----------|
| Nature 正图单栏 | 89 mm = 3.5 in | 2.0 – 2.8 in |
| Nature 正图双栏 | 183 mm = 7.2 in | 2.5 – 5.0 in |
| Nature 1.5 栏 | 120 mm = 4.7 in | 2.5 – 3.5 in |
| 投稿前临时大图 | 9 – 12 in | 等比 |

**保存格式**：投稿用 PDF 或 EPS（矢量），预览用 PNG @ 300 dpi。

```python
fig.savefig('fig1.pdf', bbox_inches='tight', pad_inches=0.02)
fig.savefig('fig1.png', dpi=300, bbox_inches='tight', pad_inches=0.02)
```

## 2. 字号（按印刷可读性）

固定层级，不要乱：

| 元素 | pt | matplotlib key |
|------|----|-----|
| panel 标号 a/b/c | 8–9 加粗 | `axes.titlesize` 或手动 `ax.text` |
| 轴标签 (`xlabel`, `ylabel`) | 7–8 | `axes.labelsize` |
| 刻度数字 | 6–7 | `xtick.labelsize`, `ytick.labelsize` |
| legend / 文本注释 | 6–7 | `legend.fontsize` |
| 标题（如有） | 8 | `axes.titlesize` |

mplstyle 里已经预设。如果某图字太挤可以全局缩 1 pt，不要单独改某一项。

## 3. 坐标轴（spine + tick）

### 默认：闭合方框（4 spines）

实证观察：现代 Nature Photonics（2024–2026）多数面板用闭合方框，特别是谱图、log-log、polar、密集时间序列、heatmap。`nature.mplstyle` 默认就是 4 spine + 上/右镜像 tick。

```python
# 默认就开了；无需手动设置。
# 强制确认：
for sp in ax.spines.values():
    sp.set_visible(True)
    sp.set_linewidth(0.6)
ax.tick_params(top=True, right=True)
```

### 例外：L+B 半框（适合简洁折线/柱状）

```python
from nature_figure_helpers import half_frame
half_frame(ax)
# 等价于：
# ax.spines[['top','right']].set_visible(False)
# ax.tick_params(top=False, right=False)
```

什么时候用 L+B 半框：简洁折线图、柱状图、散点（强调数据轮廓）。何时用闭合方框：谱图、log-log、polar、heatmap、密集时间序列、需要"信号窗口"感的。

### Tick 方向：**向内**（in）是 Nature 通用约定

`nature.mplstyle` 默认 `xtick.direction: in, ytick.direction: in`。

实证依据：22 篇里 100% 用 inward ticks。**这是最稳定的 Nature fingerprint**——一图朝外立刻显得不专业。skill v1.0 错说 outward 是默认，已修正。

### Minor ticks：开

```python
from matplotlib.ticker import AutoMinorLocator
ax.xaxis.set_minor_locator(AutoMinorLocator(2))  # 主刻度间塞 1 个 minor
ax.yaxis.set_minor_locator(AutoMinorLocator(2))
```

minor tick 长度大约是 major 的 60%；mplstyle 已配。

### Tick 数量：少而稀疏

```python
from matplotlib.ticker import MaxNLocator
ax.xaxis.set_major_locator(MaxNLocator(5))  # 全轴 5 个主刻度足够
ax.yaxis.set_major_locator(MaxNLocator(4))
```

挤了一堆刻度数字会显得业余。

### Log 轴

```python
ax.set_yscale('log')
ax.yaxis.set_major_locator(plt.LogLocator(base=10, numticks=6))
ax.yaxis.set_minor_locator(plt.LogLocator(base=10, subs=np.arange(2, 10), numticks=12))
ax.yaxis.set_minor_formatter(plt.NullFormatter())  # minor 不显示数字
```

主刻度标 10⁰ 10¹ 10²... 形式（matplotlib 默认就是），不要改成 1, 10, 100。

## 4. 轴标签 / 单位

格式：**`量名称 + 空格 + 单位（圆括号）`**

```python
ax.set_xlabel('Wavelength (nm)')
ax.set_ylabel('Transmission (a.u.)')   # arbitrary units
ax.set_ylabel('Frequency noise (Hz²/Hz)')
ax.set_ylabel(r'$\delta f$ (kHz)')      # LaTeX 数学符号
```

**不要写**：`Wavelength [nm]`（方括号是工程图风格）、`Wavelength, nm`（逗号是俄式）、`Wavelength/nm`（斜杠是英式但 Nature 不偏好）。

**`(a.u.)` 是 Nature 标志**——任何归一化或无量纲量都用 `(a.u.)`，不写 `(arb. units)` 或 `(normalized)`。

## 5. 配色（每条线/类别一种颜色）

定性多类别（≤8 组）从默认 `nature_photonics_modern` 按顺序取（实证最高频组合）：

```python
colors = ["#E63946", "#F4A261", "#E9C46A", "#2A9D8F", "#264653"]
for i, (x, y, label) in enumerate(datasets):
    ax.plot(x, y, color=colors[i], label=label, linewidth=1.0)
```

Solid = 实测，dashed (同色相) = 理论 / 拟合（He 2019 标准用法）：

```python
ax.plot(x, y_meas, color=colors[0], linewidth=1.0, label='Measured')
ax.plot(x, y_theory, color=colors[0], linewidth=0.7,
        linestyle='--', dashes=(3, 2), label='Theory')
```

定量连续映射用 LinearSegmentedColormap 或 matplotlib 自带的 viridis / inferno / magma：

```python
# 安全默认：viridis（spectrogram、2D 矩阵、hyperspectral）
ax.imshow(data, cmap='viridis', aspect='auto')

# 强度图 / streak / super-res：inferno 或 magma
ax.imshow(intensity, cmap='inferno', aspect='auto')

# 带正负：RdBu_r（红正蓝负）
ax.imshow(signed_data, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')

# 自定义暖偏 viridis（Yao 2025、Jin 2025 风格）
from matplotlib.colors import LinearSegmentedColormap
warm = LinearSegmentedColormap.from_list("warm_v",
    ["#264653", "#2A9D8F", "#E9C46A", "#E76F51"], N=256)
ax.imshow(data, cmap=warm, aspect='auto')
```

**配色原则**：
- 红 + 蓝是最经典的双色对比（实验组 vs 参考组），#E63946 / #264653 是 modern 配对
- 红 / 蓝 / 绿 / 橙 是四色对比的标配
- 同类对比（如不同温度）用 sequential colormap 或同色族深浅渐变
- **不要用 7 个完全不同的高饱和色**——超过 5 类时分组成 2-3 个色族
- **不用 jet**（除非物理量本身需要 hue↔波长映射）

## 6. 数据元素

### 折线

```python
ax.plot(x, y, color='#3C5488', linewidth=1.2,
        marker='o', markersize=3, markerfacecolor='white',
        markeredgewidth=0.8, label='Sample A')
```

- 线宽 1.0–1.5 pt（默认 1.2）
- marker 直径 3–5 pt
- 数据点稀疏时空心 marker（`markerfacecolor='white'`），密集时实心
- 不要又粗线又大点又满色——选两个突出，第三个收一收

### 误差棒

```python
ax.errorbar(x, y, yerr=err, fmt='o', color='#E64B35',
            markersize=3, capsize=2, capthick=0.6,
            elinewidth=0.6, zorder=2)
```

误差棒线宽要细（0.5–0.8 pt），cap 短（2 pt），别比数据点粗。

### 误差填充带（推荐，比误差棒更现代）

```python
ax.plot(x, y_mean, color='#3C5488', linewidth=1.2)
ax.fill_between(x, y_mean - y_std, y_mean + y_std,
                color='#3C5488', alpha=0.2, edgecolor='none')
```

`alpha=0.15–0.25`，没有边线（`edgecolor='none'`）。

### 散点

```python
ax.scatter(x, y, s=12, c='#00A087', edgecolors='white',
           linewidths=0.4, alpha=0.85, zorder=3)
```

`s=10–25` 是合适的 Nature 风格大小。带 1 px 白边能让点在密集时不糊。

### 柱状

```python
ax.bar(x, y, width=0.7, color='#4DBBD5',
       edgecolor='#3C5488', linewidth=0.5)
```

不要太粗的边线，不要 3D 阴影。分组柱状用 `dodge`（matplotlib 没现成的，自己 offset）。

### 热力图

```python
im = ax.imshow(data, cmap=cmap, aspect='auto', origin='lower',
               extent=[x_min, x_max, y_min, y_max],
               interpolation='nearest')   # 像素清晰
cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
cbar.set_label('Intensity (a.u.)')
cbar.ax.tick_params(width=0.5, length=2)
cbar.outline.set_linewidth(0.5)
```

colorbar 要细（`fraction=0.04`），紧贴主图（`pad=0.02`），轮廓也是细线。

## 7. Legend

```python
ax.legend(frameon=False, loc='upper right',
          fontsize=6.5, handlelength=1.5, handletextpad=0.4,
          labelspacing=0.3, borderpad=0.2)
```

- **无边框**（`frameon=False`）是 Nature 默认
- 字号 6–7 pt
- handle 短一点（`handlelength=1.5`），缩间距（`handletextpad=0.4`）
- 直接写在数据点旁边的 inline 标注通常比 legend 更优雅

inline 标注示例：

```python
ax.annotate('Sample A', xy=(x[-1], y[-1]), xytext=(5, 0),
            textcoords='offset points', fontsize=6.5,
            color='#3C5488', va='center')
```

## 8. Panel 标号

每个子图左上贴 `a` `b` `c`（小写、加粗）：

```python
ax.text(-0.18, 1.05, 'a', transform=ax.transAxes,
        fontsize=9, fontweight='bold', va='top', ha='left')
```

`-0.18` 是把字母推到坐标轴左外侧；视画布大小调到 -0.12 ~ -0.22 之间。

或者用工具函数（见 `assets/nature_figure_helpers.py`）：

```python
from nature_figure_helpers import add_panel_label
add_panel_label(ax, 'a')
```

## 9. 双 y 轴

```python
ax2 = ax.twinx()
ax.plot(x, y1, color='#E64B35', linewidth=1.2)
ax2.plot(x, y2, color='#3C5488', linewidth=1.2)

ax.set_ylabel('Power (mW)', color='#E64B35')
ax2.set_ylabel('Wavelength shift (pm)', color='#3C5488')
ax.tick_params(axis='y', colors='#E64B35')
ax2.tick_params(axis='y', colors='#3C5488')
ax.spines['left'].set_color('#E64B35')
ax2.spines['right'].set_color('#3C5488')
ax2.spines['top'].set_visible(False)
```

左轴和右轴的颜色要 **配套**——刻度、轴线、标签、数据线统一一种颜色。

## 10. Inset（小图嵌大图）

```python
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
axin = inset_axes(ax, width='35%', height='35%', loc='upper right',
                  borderpad=0.6)
axin.plot(x_zoom, y_zoom, color='#E64B35', linewidth=0.9)
axin.tick_params(labelsize=5)
for sp in axin.spines.values():
    sp.set_linewidth(0.4)
# inset 框出 zoom 区域
from matplotlib.patches import Rectangle
ax.add_patch(Rectangle((x_zoom[0], y_zoom.min()),
                       x_zoom[-1] - x_zoom[0], y_zoom.max() - y_zoom.min(),
                       fill=False, edgecolor='gray', linewidth=0.5,
                       linestyle='--'))
```

inset 用于：放大局部、换坐标系（log）看尾部、对比常数线。

## 11. Subplot 网格

```python
fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.0),
                         gridspec_kw={'hspace': 0.35, 'wspace': 0.30})
```

- 子图间距 `wspace=0.25-0.35`, `hspace=0.30-0.40`
- 用 `constrained_layout=True` 自动避免重叠（matplotlib ≥ 3.5）
- 复杂布局用 `gridspec.GridSpec` 划栅格

## 12. 字体回退

如果系统没有 Helvetica：

```python
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Helvetica', 'Arial', 'Liberation Sans',
                                    'DejaVu Sans']
```

mplstyle 已配。如果出图时 matplotlib 报 `findfont: Font family ['Helvetica'] not found`，安装 Helvetica 或改用 Arial（Mac/Win 自带）。

## 反例速查

下列写法 **明显不像 Nature**，看到要改：

| 反例 | 改成 |
|------|------|
| `plt.legend()` 默认带边框 | `plt.legend(frameon=False)` |
| `linewidth=2` 或 `lw=3` | `linewidth=1.0–1.5` |
| `cmap='viridis'` 直接用 | 用 colormap-palette 里的 cmap |
| `tab:blue`, `'r'`, `'b'` 单字母色 | 显式 hex |
| `ax.grid(True)` 满网格 | 不开网格，或 `alpha=0.3` 极淡 |
| panel 标号 `(a)` 或 `A` | 粗体小写 `a` |
| `Wavelength [nm]` 方括号 | `Wavelength (nm)` 圆括号 |
| 标题写一长串句子 | 标题留空，说明放 caption |
| `dpi=72` 出图 | `dpi=300`，矢量 PDF/EPS |
