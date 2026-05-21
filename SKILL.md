---
name: beamer-academic
description: >
  Generate high-quality academic Beamer slides from a thesis/paper PDF. Supports thesis defense,
  proposal presentations, and conference talks. Built-in layout library with 13 professional
  page types, 5 color schemes, and interactive editing loop.
  Use when: (1) User asks to create thesis defense slides/PPT, (2) User wants to generate
  academic presentation from a paper, (3) User mentions beamer, 答辩PPT, 学术报告, 开题PPT,
  论文幻灯片, or academic slides, (4) User has a PDF/docx thesis and wants presentation output.
---

# Beamer Academic

Generate publication-quality Beamer slides from an academic paper in one automated pipeline.

## Pipeline Overview

```
论文.pdf → 素材提取 → 大纲生成 → [用户确认] → 内容填充 → 编译 → [交互修改循环]
```

## Phase 0: Environment Check

1. Locate thesis file (`.pdf` or `.docx`) in current directory. If multiple, ask user which one.
2. Verify `xelatex` is available: `which xelatex`. If missing, suggest install command.
3. Check for `config.yaml` in current directory:
   - Exists: read and use.
   - Missing: ask user for basic info, then generate from template at `assets/config.yaml`.

Required user info (ask if not in config):
- Institution name and department
- Author name, supervisor, major
- Report type: `defense` | `proposal` | `conference`
- Color preference: `blue` | `red` | `green` | `purple` | `teal`

## Phase 1: Material Extraction

Create `materials/` directory. Extract from thesis:

1. **Figures** → `materials/figures/` (named `fig_001.png`, `fig_002.png`, ...)
2. **Tables** → `materials/tables/` (as LaTeX booktabs snippets)
3. **Equations** → `materials/equations.md` (LaTeX source)
4. **Structure** → `materials/structure.md` (chapter/section hierarchy + 50-word summaries)

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

## Phase 4: Compilation

```bash
xelatex -interaction=nonstopmode defense.tex && xelatex -interaction=nonstopmode defense.tex
```

On failure: read `defense.log`, fix common issues (missing image, font, overfull hbox), retry up to 3 times.

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
