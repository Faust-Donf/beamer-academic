# Example: Transformer Paper (Attention Is All You Need)

使用 beamer-academic skill 生成的示例 PPT，基于 Vaswani et al. (2017) 的经典论文。

## 文件

- `defense.tex` — 完整 LaTeX 源码（26 页）
- `defense.pdf` — 编译后的 PDF
- `beamerthemeAcademic.sty` — 主题文件

## 特点展示

- 蓝色配色方案（理工科通用）
- 会议报告风格（15 分钟）
- TikZ 架构图（Encoder-Decoder）
- TikZ 多头注意力可视化
- 段落+公式、段落+表格+结论等多种组合排版
- Outline 分隔页
- 纯文字致谢页

## 编译

```bash
xelatex defense.tex && xelatex defense.tex
```

需要 XeLaTeX + 中文字体（macOS 默认有宋体/黑体）。
