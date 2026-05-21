---
name: beamer-academic
description: >
  Generate high-quality academic Beamer slides from a thesis/paper (PDF, Word, or LaTeX source).
  Supports thesis defense, proposal presentations, and conference talks. Built-in layout library
  with 13 professional page types, 5 color schemes, and interactive editing loop.
  Use when: (1) User asks to create thesis defense slides/PPT, (2) User wants to generate
  academic presentation from a paper, (3) User mentions beamer, 答辩PPT, 学术报告, 开题PPT,
  论文幻灯片, or academic slides, (4) User has a PDF/docx/tex thesis and wants presentation output.
---

# Beamer Academic

Generate publication-quality Beamer slides from an academic paper in one automated pipeline.

## Pipeline Overview

```
论文 → 素材提取 → 大纲生成 → [用户确认] → 内容填充 → 编译 → [交互修改循环]
```

## Phase 0: Environment Check & Input Clarification

### 0.1 Locate Thesis File

Search current directory for thesis in priority order:
1. `.tex` (LaTeX source — best quality, figures/equations directly reusable)
2. `.docx` (Word — good for text extraction, figures embedded)
3. `.pdf` (PDF — acceptable but figure extraction may lose quality)

If multiple candidates found, ask user which one.
If none found, prompt: "请把论文文件放到当前目录（支持 .tex / .docx / .pdf）"

**Recommend .tex or .docx over PDF**: PDF figure extraction can produce low-quality raster images.
If user only has PDF, warn:
> 注意：PDF 提取的图片可能有质量损失。如果你有论文的 Word 或 LaTeX 源文件，建议优先使用。

### 0.2 Check LaTeX Environment

```bash
which xelatex
```

If missing, provide install guidance by OS:

| OS | Command |
|----|---------|
| macOS | `brew install --cask mactex-no-gui` (推荐，约3.5GB) 或完整版 `brew install --cask mactex` |
| Ubuntu/Debian | `sudo apt install texlive-xetex texlive-lang-chinese texlive-fonts-recommended` |
| Fedora/RHEL | `sudo dnf install texlive-xetex texlive-xecjk` |
| Windows (WSL) | `sudo apt install texlive-xetex texlive-lang-chinese` |
| Arch | `sudo pacman -S texlive-xetex texlive-langchinese` |

If user cannot or does not want to install LaTeX locally, offer alternative:
> 也可以只生成 .tex 文件，然后上传到 Overleaf (https://www.overleaf.com) 在线编译。

In this case, skip Phase 4 compilation and deliver `.tex` + `.sty` + figures as final output.

### 0.3 Configuration

Check for `config.yaml` in current directory:
- Exists: read and use.
- Missing: ask user for basic info, then generate from template at `assets/config.yaml`.

Required user info (ask if not in config):
- Institution name and department
- Author name, supervisor, major
- Report type: `defense` | `proposal` | `conference`
- Color preference: `blue` | `red` | `green` | `purple` | `teal`

## Phase 1: Material Extraction

Create `materials/` directory. Extraction strategy depends on input format:

### From .tex source (best)
1. **Figures**: locate `\includegraphics` paths, copy originals → `materials/figures/`
2. **Tables**: extract `tabular`/`table` environments → `materials/tables/`
3. **Equations**: extract `equation`/`align`/`$$` blocks → `materials/equations.md`
4. **Structure**: parse `\chapter`/`\section` hierarchy → `materials/structure.md`

### From .docx
1. **Figures**: extract embedded images (python-docx or unzip) → `materials/figures/`
2. **Tables**: extract table contents → `materials/tables/`
3. **Equations**: extract OMML/LaTeX equations → `materials/equations.md`
4. **Structure**: parse heading hierarchy → `materials/structure.md`

### From .pdf (fallback)
1. **Figures**: use `pdfimages` or read PDF for embedded images → `materials/figures/`
   - ⚠️ Quality may degrade. Prefer vector (PDF/SVG) extraction when possible.
2. **Tables**: read and reconstruct → `materials/tables/`
3. **Equations**: read and convert to LaTeX → `materials/equations.md`
4. **Structure**: parse chapter/section from text → `materials/structure.md`

## Phase 2: Outline Generation (MANDATORY USER APPROVAL)

**This phase produces the blueprint for the entire presentation. Do NOT proceed to Phase 3 without explicit user approval.**

Generate `outline.md` with full structural detail: chapter → section → per-page layout assignment.

### Layout Selection Rules (priority order)

1. Page 1 → `cover`
2. Page 2 → `toc`
3. Each chapter start → `section-divider`
4. Core formula/model definition → `formula`
5. Multi-row data comparison → `table`
6. High-information figure (multi-panel, heatmap) → `full-image`
7. Text-primary with supporting figure → `text-left-image-right`
8. Figure-primary with interpretation → `image-left-text-right`
9. Pure concept/background → `text-only`
10. Chapter-end with clear conclusion → `conclusion-box`
11. Between chapters → `transition`
12. Parallel bullet points → `list`
13. Final page → `thanks`

### Rhythm Constraints

- No 3 consecutive pages with same layout
- Each chapter uses at least 3 different layouts
- Total: 35–50 pages (defense), 25–35 (proposal), 15–25 (conference)

### outline.md Format (MUST include chapter/section/page three-level structure)

```markdown
# 答辩PPT大纲

## 基本信息
- 类型: 答辩
- 总页数: 42
- 时长: 20分钟
- 章节数: 4

---

## 第一章 研究背景与科学问题（共8页：P3–P10）

### §1.1 研究现状（P4–P5）

#### P4 [text-left-image-right]
- 标题: 寒武纪辐射与软体动物的演化窗口
- 左文: 介绍寒武纪时间窗口、软体动物门地位（约150字）
- 右图: fig_001.png（地质年代柱状图）
- 关键词: 演化窗口、软体动物门

#### P5 [text-only]
- 标题: 经典命题：Disparity vs. Diversity
- 内容: 形态多样性与丰富度的时间先后关系争论（约180字）
- 关键词: 形态多样性、分类丰富度

### §1.2 研究目标与假设（P6–P8）

#### P6 [text-only]
- 标题: 现有研究的四点不足
- 内容: 列举四个gap（约160字）
- 关键词: 研究不足

#### P7 [table]
- 标题: 研究目标与三个核心假设
- 表格: H1/H2/H3 + 核心假设 + 检验方法（3行4列）
- 结论文字: 三者递进关系说明

#### P8 [list]
- 标题: 论文的主要创新
- 条目: 5个创新点，每条一句话

### §1.3 过渡（P9–P10）

#### P9 [conclusion-box]
- 标题: 第一章小结
- 正文: 总结背景章要点
- 高亮框: 本文核心命题

#### P10 [transition]
- 标题: 从问题到数据
- 承上: 第一章确立了三个假设
- 启下: 接下来介绍数据构建

---

## 第二章 数据构建与描述性分析（共7页：P11–P17）

### §2.1 数据来源（P12–P13）
...

---

## 第三章 ...

---

## 第四章 结论与展望（共5页：P38–P42）
...
```

### HARD GATE: User Approval

After generating `outline.md`, **STOP and present the full outline to user**. Display it in a clear, readable format:

> ## 📋 答辩PPT大纲（共 XX 页）
>
> 请仔细检查以下大纲，确认后我才会开始生成 beamer 内容。
>
> [展示完整 outline.md 内容]
>
> ---
> **请确认或修改：**
> - 说 "ok" 或 "确认" → 开始生成
> - 说 "第二章加一页方法流程图" → 我修改大纲后再次确认
> - 说 "P7改成满版图" → 调整版式
> - 说 "第三章太长了，砍掉2页" → 精简结构
>
> ⚠️ 大纲确认后再修改结构会比较麻烦，建议在这一步把整体结构定好。

**Do NOT generate any .tex content until user explicitly says "ok" / "确认" / "继续" / "没问题".**

If user provides modifications:
1. Update outline.md
2. Re-present the updated version
3. Ask for confirmation again
4. Loop until approved

## Phase 3: Content Generation

1. Copy `assets/beamerthemeAcademic.sty` to current directory.
2. Generate `defense.tex` file header. Read `references/tex-header.md` for template.
3. For each page in `outline.md`:
   - Load layout skeleton from `references/layouts.md` (find section by layout id)
   - Fill slots with thesis content + extracted materials
4. Close with `\end{document}`.

### Content Quality Rules

| Constraint | Value |
|-----------|-------|
| Text per page (text-only) | 150–200 chars |
| Text per page (with figure) | 100–150 chars |
| Equations per page | max 2 |
| Table rows | 3–8 |
| `\alert{}` keywords per page | 1–2 |
| Paragraph style | Full sentences, not bullet lists |

## Phase 4: Compilation & Layout Verification

### 4.1 Compile

```bash
xelatex -interaction=nonstopmode defense.tex && xelatex -interaction=nonstopmode defense.tex
```

On failure: read `defense.log`, fix common issues (missing image, font, overfull hbox), retry up to 3 times.

If user has no LaTeX environment, skip compilation and deliver `.tex` + `.sty` + `materials/figures/`.

### 4.2 Layout Bug Detection

After compilation, check `defense.log` for these common layout issues:

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Overfull \vbox` on frame | Content exceeds page height | Reduce text, split into 2 pages, or shrink font |
| `Overfull \hbox` with image | Image too wide for column | Add `keepaspectratio`, reduce `width` |
| Image overlaps text in columns | `\column` width sum > `\textwidth` | Ensure left + right column ≤ 1.0 |
| tikz overlay covers text | `[remember picture, overlay]` node position wrong | Adjust `yshift`/`xshift` values |
| Text runs below frame | Too many paragraphs | Cut to 150-200 chars or split page |

**Proactive overlap prevention** (apply during Phase 3 content generation):
- For `text-left-image-right`: left text ≤ 150 chars, image height ≤ `3.4cm` per image
- For `image-left-text-right`: right text ≤ 120 chars, image height ≤ `0.60\textheight`
- For `full-image`: use **only** tikz overlay positioning, no surrounding text except `\figcap`
- For `formula`: max 2 equations, with `\vskip0.1cm` spacing between
- Never put more than 3 `\vskip` commands in one frame (sign of overstuffing)

**If overlap detected in compiled PDF** (user reports "P7图文重叠了"):
1. Identify the frame in `.tex`
2. Check: is text too long? Is image too tall? Are column widths correct?
3. Apply fix: reduce text / shrink image / split into 2 pages
4. Recompile and verify

## Phase 5: Interactive Editing

Present result:

> ✅ PDF 已生成：./defense.pdf（共 XX 页）
> 说修改意见（如"P7公式拆两页"），或说"满意"结束。

Handle modifications:

| Type | Action |
|------|--------|
| Single page content edit | Edit corresponding `\begin{frame}...\end{frame}` |
| Add/remove page | Update outline.md, regenerate affected section |
| Global style change | Modify .sty or header |
| Layout switch | Replace frame with different layout skeleton |

After each edit, recompile and present again. Loop until user says done.

## Reference Files

- `references/layouts.md` — All 13 layout skeletons with slot definitions and LaTeX code
- `references/tex-header.md` — Standard .tex file preamble template
- `references/layout-registry.yaml` — Layout selection rules in structured format

## Assets

- `assets/beamerthemeAcademic.sty` — Beamer theme file (copied to user project)
- `assets/config.yaml` — Configuration template (copied to user project)
