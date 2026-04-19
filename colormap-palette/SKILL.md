---
name: colormap-palette
version: 1.0.0
description: "用户偏好的精选配色方案库。当用户要求写文档、画示意图、画图表、生成 matplotlib / seaborn / plotly / TikZ / Mermaid / PPT 配色、绘制 schematic / 论文插图 / Nature 风格图 / flowchart / 架构图 / 数据可视化 时使用。关键词：配色、colormap、palette、调色板、色系、好看的颜色、配色方案、paper figure、schematic、示意图、折线图、柱状图、热力图、colorbar。优先级：日落 Sunset / 樱花 Sakura / 莫奈 Monet / 莫兰迪 Morandi / 蒂芙尼 Tiffany 五个为用户最爱，默认首选。"
---

# colormap-palette

用户精选配色库（19 套）。当你要为用户生成**任何**带颜色的产物——图表代码、示意图、PPT 色条、配色建议、文档装饰——**必须**从这里挑色，不要用 matplotlib 默认 tab10 / viridis / jet 等。

## 使用原则

1. **默认首选「最爱 5 套」**（按优先级排列）：
   - **Sunset 日落** — 暖色温度递进，适合能量、功率、热力、渐进过程
   - **Sakura 樱花** — 粉色单色系，适合柔和单变量、女性主题、生物/医学
   - **Monet 莫奈** — 印象派多彩柔光，适合多条曲线、多类别对比
   - **Morandi 莫兰迪** — 低饱和高级灰，适合严肃科研/论文插图、商务 PPT
   - **Tiffany 蒂芙尼** — 青绿清新，适合界面、产品、海洋/大气类主题

2. **选择逻辑**：
   - 如果**数据是渐进的**（温度、时间、浓度、能量）→ 用连续型：Sunset / Sakura / Ocean / Monet
   - 如果**数据是离散类别**（≤8 组）→ 用离散型：Morandi / Tiffany / Monet / Wes Anderson
   - 如果是**Nature/Science 论文**且用户没指定风格 → 默认 Morandi 或 Monet；正式可用 Nature-Journal / Science-Journal
   - 如果是**PPT / 示意图**需要吸睛 → Sunset / Tiffany / Macaron
   - 如果是**中国/日本/传统主题** → Chinese-Traditional / Japanese-Wafu / Dunhuang / Sakura

3. **使用时的交付物**：
   - 写代码时直接把 hex 列表内联到代码里（见下方完整色表），不要让用户手动去查
   - 向用户说明你选了哪套、为什么选
   - 给出的配色必须是下面列表里的完整 hex 字符串

## 完整色表（按优先级排序）

### ★ 最爱 5 套 ★

**Sunset 日落** — 暖色能量递进
```python
sunset = ["#FFE5B4", "#FFC988", "#FFA14A", "#FF6F3C", "#E63946", "#A4343A", "#6A0F49", "#2E1A47"]
```

**Sakura 樱花** — 粉色柔和递进
```python
sakura = ["#FFF5F7", "#FFE0EC", "#FFB7CE", "#FF8FAB", "#F46197", "#C44B7F", "#8B3A62", "#4A1D3F"]
```

**Monet 莫奈** — 印象派多彩柔光
```python
monet = ["#A7C5D8", "#7FA5B9", "#B8C8A0", "#D8D4A5", "#E8B9A6", "#C98A8A", "#9B7B9B", "#5C6B8A"]
```

**Morandi 莫兰迪** — 低饱和高级灰
```python
morandi = ["#D7C7BC", "#C3AE94", "#B8A99A", "#A3A3A3", "#9DA9AC", "#8D9C8C", "#7E7F76", "#5C5C5C"]
```

**Tiffany 蒂芙尼** — 青绿清新
```python
tiffany = ["#E8F6F3", "#A8DADC", "#81C9C4", "#4FB3A9", "#2E8B85", "#1F5F5B", "#F5E6CA", "#DDB892"]
```

### 其它 14 套（按需调用）

**Macaron 马卡龙** — 甜美粉嫩（PPT、插画）
```
["#F7B7A3", "#F6D5A7", "#FFE6A7", "#D4E7C5", "#A8D5BA", "#AEDFF7", "#C9B1E1", "#F5A6C6"]
```

**Chinese-Traditional 中国传统色** — 敦厚雅致
```
["#E8B4B8", "#C08081", "#8C4646", "#5C4033", "#A68A64", "#C9B380", "#6B8E5A", "#3E5F4E"]
```

**Japanese-Wafu 日式和风** — 淡雅克制
```
["#F5E1DA", "#E8B9AB", "#BB9691", "#7C5E5A", "#B5C4B1", "#6E8B7A", "#435E51", "#2F4538"]
```

**Nordic 北欧** — 冷静极简
```
["#2B3A42", "#3F5765", "#7A99A8", "#BDCED7", "#E5E9EC", "#D9B08C", "#A88674", "#5B4438"]
```

**VanGogh 梵高** — 浓烈对比（星空）
```
["#0B3D91", "#1E5AAA", "#3E7CB1", "#F2C14E", "#F4A261", "#E07A5F", "#3D5A80", "#0A2342"]
```

**Wes-Anderson 韦斯安德森** — 电影复古
```
["#F7C59F", "#EFBC9B", "#FFB997", "#A5C4D4", "#7A9CA5", "#D49A6A", "#B55A30", "#5E3023"]
```

**Dunhuang 敦煌** — 沉稳厚重
```
["#D9A86C", "#B87333", "#8B3A3A", "#5C2A2A", "#C9A66B", "#6B8E4E", "#3F5E5A", "#2B1E1A"]
```

**Pantone-Classic 潘通经典**
```
["#5F4B8B", "#88B04B", "#F7CAC9", "#92A8D1", "#955251", "#B565A7", "#009B77", "#DD4124"]
```

**Cyberpunk 赛博朋克** — 霓虹未来
```
["#0D0221", "#1B1B3A", "#3C096C", "#7209B7", "#F72585", "#FF006E", "#00F5D4", "#00BBF9"]
```

**Ocean 海洋** — 深蓝渐变（连续型极好）
```
["#E0F7FA", "#A0DEE5", "#5BC0BE", "#3A9188", "#1C5D7A", "#0E3A5F", "#08244F", "#020F27"]
```

**Forest 森林** — 绿色自然
```
["#E8F0D9", "#BACD99", "#8BAE68", "#5E8C45", "#3F6B34", "#2D5228", "#1A3A1F", "#4A3723"]
```

**Nature-Journal Nature 期刊**（NPG 风格，论文多类别分组）
```
["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F", "#8491B4", "#91D1C2", "#DC0000"]
```

**Science-Journal Science 期刊**（AAAS 风格）
```
["#3B4992", "#EE0000", "#008B45", "#631879", "#008280", "#BB0021", "#5F559B", "#A20056"]
```

**Retro-Film 复古胶片**
```
["#D4B483", "#C1666B", "#48A9A6", "#E4DFDA", "#4F6D7A", "#8A3033", "#F4A261", "#2A2B2A"]
```

## Matplotlib 用法示例

```python
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

# 离散色：直接喂 cycler
morandi = ["#D7C7BC", "#C3AE94", "#B8A99A", "#A3A3A3",
           "#9DA9AC", "#8D9C8C", "#7E7F76", "#5C5C5C"]
plt.rcParams["axes.prop_cycle"] = plt.cycler(color=morandi)

# 连续色：做成 colormap 给 imshow / contourf / scatter(c=...)
sunset = ["#FFE5B4", "#FFC988", "#FFA14A", "#FF6F3C",
          "#E63946", "#A4343A", "#6A0F49", "#2E1A47"]
cmap_sunset = LinearSegmentedColormap.from_list("sunset", sunset, N=256)
plt.imshow(data, cmap=cmap_sunset)
```

## 图片预览

每套配色都有一张展示图（离散色块 + 连续渐变 + 折线示例）：
- 用户级：`~/.claude/skills/colormap-palette/previews/<Name>.png`（如存在）
- 项目级：`<project>/colormap/<Name>.png`

当用户要求"看看效果"、"给我看看 XX 配色长啥样"时，Read 对应 PNG 让用户确认。

## Reminder

**不要回到 matplotlib 默认色（tab:blue / viridis / jet / hsv）**，除非用户明确要求。这是用户持续表达过的偏好。
