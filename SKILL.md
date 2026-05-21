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

## Phase 2: Outline Generation

Generate `outline.md` assigning a layout to each page.

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

### outline.md Format

```markdown
### P1 [cover]
Title / Author / Supervisor / Date

### P2 [toc]
4 chapters with sub-items

### P3 [section-divider]
一、研究背景

### P4 [text-only]
Title: XXX
Content: (50-word summary)

### P5 [text-left-image-right]
Title: XXX
Left: (summary)
Right: fig_001.png
```

### Checkpoint

After generating `outline.md`, **pause and present it to user**:

> 大纲已生成，请查看 outline.md。说"ok"继续，或提修改意见（如"P7改成满版图"）。

Wait for confirmation before proceeding.

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
