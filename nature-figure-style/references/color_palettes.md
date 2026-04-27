# 配色场景化建议

本 skill 的配色基于 22 篇 Nature / Nature Photonics 论文实证（见 `empirical_observations.md`）。`assets/nature_figure_helpers.py` 的 `PALETTES` 字典里有所有色板，外加 `MATERIAL_COLORS` / `COMB_COLORS` 两个语义字典。

## 决策树

```
做 Nature / Science 论文图？
├── 数据图（折线/柱状/热力/散点）
│   ├── 离散类别（≤8 组）
│   │   ├── 现代 Nature Photonics 投稿 → nature_photonics_modern（默认，实证最高频）
│   │   ├── 老派 NPhoton 风（红+蓝+绿+橙） → nature_photonics_classic
│   │   ├── 生物 / Cell / Methods → nature_journal（NPG 8 色）
│   │   ├── 严肃低饱和 → Morandi
│   │   └── 柔和印象派 → Monet
│   └── 连续映射
│       ├── spectrogram / 2D 矩阵 → viridis
│       ├── 强度 / streak / super-res → inferno / magma
│       ├── 带正负的物理量 → RdBu_r
│       ├── eye diagram → 黑底 cyan→white
│       └── 暖色递进 (功率/热) → Sunset；冷色 → Ocean；单色 → Sakura
└── 架构图 / schematic
    ├── 材料色（chip 截面） → MATERIAL_COLORS（si/lnoi/ltoi/sio2/gold/...）
    ├── 光路角色色（dual-comb / pump-probe） → COMB_COLORS（comb1/comb2/beat/shg/...）
    ├── 输入/处理/输出 三段式 → Tiffany 中后段
    └── 主元素填充 → Tiffany / Sakura / Morandi 中段
```

## 高频组合速查

下面几组是高复用率的，可以直接抄。

### 1. Nature Photonics 现代离散调色板（**默认，实证最稳**）

```python
nature_photonics_modern = ["#E63946", "#F4A261", "#E9C46A",
                            "#2A9D8F", "#264653",
                            "#7E3FA8", "#F46197", "#888888"]
```

锚定论文：Yao 2025、Jin 2025、Kalinin 2025、Wang 2024、Geravand 2025（部分）。
适用：≤6 类离散对比、bar、scatter group、多曲线对比。

`setup_nature_style()` 默认就是这套。

### 2. Nature Photonics 老派离散（红+蓝+绿+橙）

```python
nature_photonics_classic = ["#D6322B", "#1F5FAE", "#2A8E3A", "#E08A2A",
                             "#7E3FA8", "#B23A8C", "#222222", "#888888"]
```

锚定论文：Hu 2021、He 2019、Feng 2024、Giorgetta 2024、Han 2024。
适用：希望偏 2019–2023 风的论文图。

### 3. NPG / Cell / Nature Methods 8 色（生物风）

```python
nature_journal = ["#E64B35", "#4DBBD5", "#00A087", "#3C5488",
                  "#F39B7F", "#8491B4", "#91D1C2", "#DC0000"]
```

适用：≤8 类离散对比，特别适合 Cell / Nature Methods / Nature Reviews。**这是 ggsci 的 npg_palette**。

### 4. 双色对比（实验组 vs 参考组）

现代风：
```python
exp = "#E63946"     # 实验
ref = "#264653"     # 参考
```

老派风：
```python
exp = "#D6322B"
ref = "#1F5FAE"
```

### 5. 严肃论文"高级灰"（Morandi）

```python
morandi = ["#D7C7BC", "#C3AE94", "#B8A99A", "#A3A3A3",
           "#9DA9AC", "#8D9C8C", "#7E7F76", "#5C5C5C"]
```

适用：审稿人偏好低调、商务向 Nature 子刊（Methods、Reviews）。

### 4. 多曲线印象派对比（Monet）

```python
monet = ["#A7C5D8", "#7FA5B9", "#B8C8A0", "#D8D4A5",
         "#E8B9A6", "#C98A8A", "#9B7B9B", "#5C6B8A"]
```

适用：6+ 条曲线但又不希望色感杂乱时。

### 5. 暖色连续映射（功率、温度、时间）

```python
sunset = ["#FFE5B4", "#FFC988", "#FFA14A", "#FF6F3C",
          "#E63946", "#A4343A", "#6A0F49", "#2E1A47"]

from matplotlib.colors import LinearSegmentedColormap
cmap_sunset = LinearSegmentedColormap.from_list("sunset", sunset, N=256)
```

适用：heatmap（强度/功率/温度）、time-series 颜色编码、fluorescence imaging。

### 6. 冷色连续映射（深度、噪声、相位）

```python
ocean = ["#E0F7FA", "#A0DEE5", "#5BC0BE", "#3A9188",
         "#1C5D7A", "#0E3A5F", "#08244F", "#020F27"]
cmap_ocean = LinearSegmentedColormap.from_list("ocean", ocean, N=256)
```

## 反例（不要做的事）

1. **不要用 matplotlib 默认 tab10**——`tab:blue` 是 Python data scientist 味，不是 Nature 味。
2. **不要用 jet**——已经被现代色彩科学批判（不感知均匀）。除非用户明确要，否则用 Sunset / Ocean 替代。
3. **不要把 8 色调色板全堆在一张图上**——超过 5 类时分组，同组用同色族。
4. **不要混用饱和度差异大的色**——比如荧光粉 + 莫兰迪灰会很难看。
5. **架构图配色不能照搬数据图**——数据图要色彩对比，架构图要色彩调和。

## 当用户说"按 Nature 风格"但没指定具体期刊

按这个优先级试：
1. 第一选：`nature_photonics_modern`（默认；2024–2026 最高频）
2. 二选：`nature_photonics_classic`（如果是 photonics 偏老派论文）
3. 三选：`nature_journal`（如果是生物 / Cell / Methods）
4. 四选：`Morandi`（严肃低饱和）/ `Monet`（多曲线柔和）

并 **明确告诉用户**："默认选了 nature_photonics_modern（实证 2024–2026 NPhoton 最高频 5 色）。如果想换 classic（老派红+蓝+绿+橙）/ NPG 8 色 / Morandi / Monet，告诉我。"
