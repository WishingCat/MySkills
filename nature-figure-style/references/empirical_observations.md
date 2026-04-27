# 实证观察记录（v2.0 ground truth）

本文件是 nature-figure-style skill 所有数值规则的依据。基于
`/Users/wishingcat/Research/Nature 绘图/Nature 期刊绘图风格提取/figures_extracted/`
中 22 篇 Nature / Nature Photonics 论文（2019–2026）的图表分析。如果将来 skill 的某条规则需要修订，先回到这里看证据，不要随手改。

## 论文清单

| 简称 | 期刊 / 年 | 关键词 |
|------|-----------|--------|
| Paper 01 | Nat. Photon. 2026 | MeV 电子衍射、ultrafast nonlinear |
| Paper 03 | Nat. Photon. 2026 | optical convolutional spectrometer |
| Paper 10 | Nat. Photon. 2026 | twisted optical fibres、topology |
| Paper 11 | Nat. Photon. 2025 | super-resolution 成像 |
| Paper 13 | Nat. Photon. 2025 | colloidal QD lasing |
| Paper 14 | Nat. Photon. 2025 | chiral OLED |
| Paper 15 | Nat. Photon. 2025 | quantum photonic network |
| Paper 16 | Nat. Photon. 2025 | HHG in liquids |
| Paper 18 | Nat. Photon. 2025 | tensor processing |
| Chen 2023 | Nat. Photon. 17 | chaotic LiDAR |
| Cheng 2025 | Nat. Photon. 19 | micro-FP reference cavity |
| Dinani 2025 | Nat. Photon. 19 | thermalisation routing |
| Feng 2024 | Nat. Photon. | LN microwave photonic processor |
| Geravand 2025 | Nat. Photon. | MRM coherent dynamics |
| Giorgetta 2024 | Nat. Photon. | free-form dual-comb |
| Han 2024 | Nat. Photon. | 100 km dual-comb |
| He 2019 | Nat. Photon. | hybrid Si-LN MZM |
| Hu 2021 | Nature | EO frequency shifter |
| Jin 2025 | Nat. Photon. | soliton microcomb |
| Kalinin 2025 | Nature | analog optical computer |
| Wang 2024 | Nature | LiTaO₃ PIC |
| Yao 2025 | Nature | LN computing for spectroscopy |

## A. 架构 / 示意图风格（cross-paper synthesis）

### A.1 渲染流派（按使用频率排序）

1. **Hybrid（3D 上 + 2D 下）**——最常见。3D isometric chip / 设备 hero 图占上半，下半是 measurement setup 的 2D block / 光路图。例：Chen 2023, Cheng 2025, Yao 2025, Kalinin 2025。
2. **纯 3D isometric** chip / device 渲染——单层或多层堆叠，~30° 等距投影，软渐变着色，避免镜面反射。例：Geravand 2025, Wang 2024, He 2019, Hu 2021。
3. **纯 2D vector block** 图——measurement setup、network topology、process flow、光路图。例：Paper 15, Paper 18 (lower), Giorgetta 2024, Han 2024。
4. **Photo + vector overlay**——把真实显微图 / 卫星图 / 光路实物图叠加在 vector 上，常用 false-color overlay 把 photo 配色和 schematic 配色对齐。例：Paper 03, Han 2024, Giorgetta 2024 Fig 5, Cheng 2025 inset。

### A.2 背景

22 篇 100% 用 **纯白 #FFFFFF** 背景。极少数情况下用 #F7F7F7 极浅灰当 grouping divider。绝不用渐变天空 / 彩色背景。3D 物体下方有 **柔和阴影**（10% 黑色 + 高斯模糊），但不深。

### A.3 光束 / 光路画法

| 方法 | 来源 | 何时用 |
|------|------|--------|
| 细实色线 1.4–2 pt | 几乎所有 vector schematic | 平面光路、芯片波导 |
| Gradient ribbon (red→yellow→blue) | Paper 03, Yao 2025 | broadband / spectral 输入 |
| Gaussian glow / volumetric halo | Kalinin 2025, Dinani 2025, Paper 16, Jin 2025 | 3D hero 主光束 |
| 虚线 (dashes 3,2) | 全员 | 控制 / feedback / virtual / proposed |
| 圆锥 / 扇形 ray fan | Paper 01, Chen 2023 LiDAR | 投射式光束（强调发散） |

光束颜色严格 follow COMB_COLORS 公约（详见 SKILL.md）。Pump 和 signal 用对比色（红 vs 蓝最常见）。

### A.4 组件几何（recurring conventions）

- **激光器**：小立方 / 圆柱（3D），或带"光腔"斜面的矩形（2D）。常涂 **红 #D6322B** 表示 1550 nm 通信波段，绿 #2A8E3A 表示 SHG/可见，蓝 #1F5FAE 表示 LO/参考。
- **光纤**：平滑 Bezier / 弧线，**统一 1 pt 描边**；外护套常黄色 #F0C03A，纤芯红/蓝/绿 区分通道。
- **芯片俯视图**：圆角矩形 + 内部 1–2 条波导线（红或粉色）+ 边缘电极（金黄）。
- **Microring**：细圆轮廓（无填充或浅 teal 填充），与 bus 波导相切。
- **MZM**：两条平行波导 + 上方电极指。
- **BS / PBS**：45° 倾斜短矩形，半填充表示半反半透。
- **Photodetector**：白圆 + 半月填充（深蓝 #1E3A78 或黑），开口朝光来方向。
- **频谱仪 / oscilloscope**：标"绿屏"图标（#2BA84A）。
- **Microscope 实拍 chip**：黑色 0.5 pt 边框 + 白色 µm scale bar 在右下。

### A.5 标注 / callout

- 引线：**细 0.4–0.5 pt**, 黑色 / 深灰，**无箭头**（用 `'-'` 不用 `'-|>'`）。
- 终端：在元件那侧加一个 **小填充黑点**（直径 ~1 pt）作为锚点。
- 文字：**6.5–7.5 pt sans-serif**，水平排列（不要顺着引线方向旋转）。
- 物理量名 italic（λ, ϕ, V_π），单位 / 元件名 upright。
- 引线尽量短，**不交叉**。

### A.6 Panel label（架构图）

完全和数据图一致：**bold lowercase a/b/c**，sans，**~9–10 pt**，**top-left**，**无括号无句点**，距离 panel 边 ~4 pt。

### A.7 Inset / 放大插图

- 边框：**细 0.5 pt 黑色**矩形。
- 连接：**两条发散 dashed gray 0.5 pt** 引线，从父图区域到 inset 的两个角，构成梯形。
- 内容：和父图同色系；显微 inset 常 desaturate 后再 false-color overlay。

### A.8 箭头

- 实心三角头（filled triangle），头部 ~3 pt 长。
- 描边宽 0.5–0.8 pt（匹配元件描边）。
- **不用 open V-arrow**。
- 直箭头表示 signal flow，曲箭头表示 feedback loop / cyclic process。

## B. 数据图表风格（cross-paper synthesis）

### B.1 Spine（轴线方框）

| 流派 | 流行度 | 何时用 |
|------|--------|--------|
| 闭合方框（4 spines） | 多数（特别是 2024–2026 NPhoton） | 谱图、log-log、polar、密集时间序列、heatmap |
| L+B 半框 | 老派 / 极简风 | 简洁折线、柱状、bar |

**Tick 方向 100% 向内**（`direction='in'`）—— **这是 22 篇里最稳定的特征**，旧版 skill 错说外。
闭合方框时 tick 镜像到上 / 右两侧（`xtick.top: True, ytick.right: True`）。

Minor ticks **几乎总是开**，特别是 log 轴必有。
Major tick 长度 ~3 pt，minor ~1.5–1.8 pt。
Tick label 字号 **6–7 pt**。

### B.2 字号层级

| 元素 | pt |
|------|----|
| panel 标号 a/b/c | 9–10 加粗 |
| 轴标签 (xlabel/ylabel) | 7–8 |
| 刻度数字 | 6–7 |
| legend / inline 标注 | 6–7 |

整图字号区间 **6–10 pt**，绝不超过 12。

### B.3 线宽

- 主数据线：**0.8–1.2 pt**（22 篇里集中在 1.0 pt）。
- 拟合 / 理论 / 参考虚线：**0.5–0.7 pt**。
- 极密集时间序列：**0.5 pt**（如 Han 2024 Fig 3）。
- 坐标轴 spine：**0.6 pt**。

### B.4 配色（categorical 5–6 色）

实证最高频组合：

```python
[ "#E63946",  # 红 (Yao, Jin, Kalinin)
  "#F4A261",  # 橙 (Yao, Jin)
  "#E9C46A",  # 金 (Yao)
  "#2A9D8F",  # 青绿 (Yao, Jin, Kalinin)
  "#264653",  # 深蓝 (Yao, Kalinin)
  "#7E3FA8",  # 紫 (Giorgetta beat path, He 2019)
]
```

替代组（早期 NPhoton 2019–2023）：

```python
[ "#D6322B",  # 红
  "#1F5FAE",  # 蓝
  "#2A8E3A",  # 绿
  "#E08A2A",  # 橙
  "#7E3FA8",  # 紫
  "#B23A8C",  # 品红
]
```

约定：
- **solid = measured，dashed = simulated/theory**（同色相）。He 2019 Fig 2 标准用法。
- **black dots + colored fit line** 是常见组合。
- **inline 颜色标注**：曲线旁直接写文字（颜色匹配），代替 legend。

### B.5 Marker

- 主：**filled circles ~3 pt**。
- 添加 dimension 时：**filled squares / triangles**（同色相）。
- **白边缘 0.3 pt** 偶尔出现（密集散点时增加可读性）。
- **空心 marker 罕见**。

### B.6 误差表示

实证频次：**shaded confidence band（透明色填充）≫ errorbar（带帽）**。

- Band: alpha 0.15–0.25，颜色和主线一致，`edgecolor='none'`。
- Errorbar: cap size 2–3 pt，elinewidth 0.5–0.8 pt。优先 T-cap，不用大 cap。
- 离散 vs 连续：连续曲线用 band；离散点用 errorbar。

### B.7 Heatmap / colormap

| Colormap | 高频用途 | 示例论文 |
|----------|----------|----------|
| viridis | spectrogram、2D 测量矩阵、hyperspectral | Giorgetta, Yao, Paper 03 |
| inferno / magma | 强度图、streak camera、super-res | Paper 11, Paper 13, Dinani |
| 暖偏 viridis (cyan→yellow→red) | 数据偏正向、强度 | Jin 2025, Yao 2025 |
| diverging RdBu_r | 带正负的物理量（band, 相位） | Paper 10 |
| 黑底 cyan→white | eye diagram | He 2019, Geravand, Wang 2024 |
| jet / rainbow | parametric sweep（hue=参数序号） | Geravand polar |
| earth tone fill | topographic profile | Han 2024 |

Colorbar：
- **垂直右侧**或**水平上侧**。
- **细长**（fraction ~0.04，aspect ~10:1）。
- **轮廓 0.5 pt** 或无框。
- Tick 在外侧；标签只在 min/max（中间偶尔加 1–2 个）。
- 文字 rotated 270° 在右侧 colorbar 上。

### B.8 Legend

- **几乎都无框**（`frameon=False`）。
- 位置：plot 内 top-right 最常见。
- 字号 **6–7 pt**，handle 短（`handlelength=1.5`）。
- 当框时：**thin gray 0.4 pt 边 + 白底**。
- **inline 标注**频繁替代 legend。

### B.9 Multi-panel layout

- 共享 x 的堆叠面板：**panel 间无间隙**（gap=0），共享轴只在最下方画 label。
- 2×2 / 2×3 网格：`wspace=0.25–0.35`, `hspace=0.30–0.40`。
- Subplot panel label 始终 top-left outside frame。

### B.10 注释 / 参考线

- **垂直 dotted gray (#888) 0.5 pt** 标关键频率 / 共振。
- **水平 dashed gray** 标阈值（3 dB、baseline）。
- **箭头注释**：thin filled triangle head，6 pt italic 文字。

### B.11 特殊轴

- **Log axes**: minor ticks 必开；y label 写 `10ⁿ` 不写 `1e+n`。
- **Dual y-axis**: 左右 spine + tick + label 颜色配对各自的 line color。
- **Polar**: 全圆 grid 极淡 gray（#D0D0D0），方位标在 0/90/180/270。
- **3D scatter / surface**: 简单 wireframe box + grid，无 fancy lighting。

## C. 期刊间细微差异

- **Nature Photonics**：偏 photonics-specific 的 LNOI/Si 配色 + 强 hybrid 风格。
- **Nature 主刊**（Hu 2021, Wang 2024, Kalinin 2025, Yao 2025）：更偏 polished 3D hero，application-context illustrations 更多。
- **Nature Communications / Methods / Reviews**：本批没覆盖；推断走更朴素的 NPG biology 配色。

## D. 风格 fingerprint（用于一眼识别）

合格的 Nature 风格图必须满足：白底 + sans + 加粗小写 a/b/c top-left + 6–10 pt 字号 + inward ticks（多数有 minor）+ 0.6 pt 描边 + 无框 legend + shaded error band 或细 errorbar + 5 色饱和但不刺眼调色板 + 实拍/3D/vector 三种素材自然混搭。

任何一项不匹配都会破坏 Nature 感。
