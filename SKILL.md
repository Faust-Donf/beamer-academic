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
- Time limit (minutes): affects page count and content density
- Language: thesis language vs. PPT language (e.g., 英文论文 → 中文PPT)

### 0.4 Language Strategy

If thesis language ≠ PPT language, establish rules upfront:

> 你的论文是英文，PPT 要做中文版吗？
> 对于专业术语，我会：
> 1. 首次出现用"中文（English）"格式
> 2. 之后统一用中文
> 3. 公式/变量名保持英文不翻译
>
> 这样处理可以吗？

Build a **terminology mapping table** (stored in `materials/terms.md`):
```
| English | 中文 | 首次出现页 |
|---------|------|-----------|
| disparity | 形态多样性 | P4 |
| diversity | 分类丰富度 | P4 |
| Ornstein-Uhlenbeck | OU 过程 | P8 |
```

Ensure **术语一致性**: same concept uses same translation across all pages.

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

### 1.2 Material Confirmation (In-Conversation)

After extraction, present a **figure catalog** to user in conversation:

> ## 🖼️ 素材库（共提取 12 张图）
>
> | # | 文件名 | 来源 | 内容描述 |
> |---|--------|------|----------|
> | 1 | fig_001.png | 论文图1 | 地质年代柱状图 |
> | 2 | fig_002.png | 论文图4 | PCoA 碎石图 |
> | 3 | fig_003.png | 论文图8 | 形态空间散点图 |
> | ... | | | |
>
> **哪些图是你答辩必须展示的？** 可以说：
> - "1, 3, 5, 8 必须用"
> - "图7 不用了，跟图5 重复"
> - "全部都可能用到"

This ensures:
- Key figures won't be missed in layout assignment
- User has a mental model of available materials before the outline phase
- Low-quality or duplicate figures can be flagged early

## Phase 2: Brainstorm Outline (Interactive, In-Conversation)

**This phase determines the entire presentation structure through conversation with the user. All confirmation happens IN THE CHAT — never ask user to open a file.**

### 2.1 First Pass: Structure Proposal

After reading the thesis, propose the high-level structure directly in conversation:

> ## 📐 PPT 结构提案
>
> 根据你的论文，我建议这样安排：
>
> **总页数**：42 页（约 20 分钟答辩）
>
> | 章 | 标题 | 页数 | 说明 |
> |---|------|------|------|
> | 一 | 研究背景与科学问题 | 8页 | 背景+命题+假设+创新点 |
> | 二 | 数据构建与描述性分析 | 7页 | 数据来源+特征工程+时序总览 |
> | 三 | 演化模式与驱动机制 | 15页 | H1+H2+H3 三个假设检验 |
> | 四 | 结论与展望 | 5页 | 主要结论+局限+展望+成果 |
>
> **你觉得这个结构可以吗？** 可以告诉我：
> - "第三章太长了，拆成两章"
> - "加一章文献综述"
> - "总页数控制在35页以内"

Wait for user to confirm or adjust. Loop until structure is approved.

### 2.2 Second Pass: Per-Section Detail

Once chapter structure is approved, expand each chapter **in conversation** (not in a file):

> ## 📋 第一章 详细安排（8页）
>
> | 页码 | 版式 | 标题 | 内容要点 |
> |------|------|------|----------|
> | P3 | 章节分隔 | 一、研究背景与科学问题 | — |
> | P4 | 左文右图 | 寒武纪辐射与软体动物的演化窗口 | 演化窗口介绍 + 地质年代图 |
> | P5 | 纯文段 | 经典命题：Disparity vs. Diversity | 形态多样性与丰富度争论 |
> | P6 | 纯文段 | 驱动机制之一：外源突变 | Sinsk 事件背景 |
> | P7 | 纯文段 | 驱动机制之二：系统发育约束 | OU 过程假说 |
> | P8 | 列表 | 现有研究的四点不足 | 4个gap |
> | P9 | 表格 | 研究目标与三个核心假设 | H1/H2/H3 表格 |
> | P10 | 列表 | 论文的主要创新 | 5个创新点 |
>
> **这章的安排可以吗？** 可以说：
> - "P5和P6合并成一页"
> - "P9加一列'若成立则说明'"
> - "ok，继续下一章"

Present **one chapter at a time**. Wait for approval before showing the next chapter.

### 2.3 Third Pass: Final Confirmation

After all chapters are individually approved, show a **complete summary** in conversation:

> ## ✅ 最终大纲确认
>
> | 章 | 页码范围 | 页数 | 版式分布 |
> |---|---------|------|----------|
> | 封面+目录 | P1–P2 | 2 | cover, toc |
> | 一 研究背景 | P3–P10 | 8 | 分隔×1, 左文右图×1, 纯文段×3, 列表×1, 表格×1, 列表×1 |
> | 二 数据构建 | P11–P17 | 7 | 分隔×1, ... |
> | 三 演化机制 | P18–P32 | 15 | 分隔×1, ... |
> | 四 结论展望 | P33–P37 | 5 | 分隔×1, ... |
> | 致谢 | P38 | 1 | thanks |
> | **合计** | | **38页** | |
>
> **确认后我将开始生成 beamer LaTeX 代码。确认吗？**

**HARD GATE: Do NOT proceed to Phase 3 until user explicitly confirms the final summary.**

### 2.4 Save to outline.md

Only after final confirmation, save the approved structure to `outline.md` for Phase 3 reference. This file is for the AI's internal use — user has already approved everything in conversation.

### Why In-Conversation Instead of File

- Many users don't know how to open/read .md files
- Conversation is the natural interaction medium in Claude Code
- Iterative refinement is faster in chat (no "go check that file" round-trip)
- Each chapter gets individual attention instead of one overwhelming dump

### Layout Selection Rules (used in 2.2 per-page assignment)

1. Each chapter start → `section-divider`
2. Core formula/model definition → `formula`
3. Multi-row data comparison → `table`
4. High-information figure (multi-panel, heatmap) → `full-image`
5. Text-primary with supporting figure → `text-left-image-right`
6. Figure-primary with interpretation → `image-left-text-right`
7. Pure concept/background → `text-only`
8. Chapter-end with clear conclusion → `conclusion-box`
9. Between chapters → `transition`
10. Parallel bullet points → `list`

### Rhythm Constraints

- No 3 consecutive pages with same layout
- Each chapter uses at least 3 different layouts
- Total: 35–50 pages (defense), 25–35 (proposal), 15–25 (conference)

## Phase 3: Content Generation

1. Copy `assets/beamerthemeAcademic.sty` to current directory.
2. Generate `defense.tex` file header. Read `references/tex-header.md` for template.
3. For each page in `outline.md`:
   - Load layout skeleton from `references/layouts.md` (find section by layout id)
   - Fill slots with thesis content + extracted materials
4. Close with `\end{document}`.

### Critical: Section Divider = Outline Page (NOT full-color page)

The section-divider page should be an **Outline page** that shows all chapters with the current
chapter highlighted, NOT a full-color page with just a number. Use `\tableofcontents[currentsection]`
or equivalent tabbing layout where current chapter is bold/colored and others are grayed out.

Example (每章开头的分隔页):
```latex
\begin{frame}
  \frametitle{Outline}
  \tableofcontents[currentsection]
\end{frame}
```

### Critical: TOC Page Format

The TOC page (P2) must use Chinese numbering with em-dash subtitles:
```latex
\begin{frame}
  \frametitle{汇报提纲}
  \vskip0.3cm
  {\footnotesize
  \begin{tabbing}
  \hspace{0.4cm}\=\hspace{0.6cm}\=\kill
  \textbf{\color{accentcolor}一}\>\textbf{研究动机}\,——\,为什么需要新的序列建模方案\\[8pt]
  \textbf{\color{accentcolor}二}\>\textbf{模型架构}\,——\,Transformer 的核心设计\\[8pt]
  \textbf{\color{accentcolor}三}\>\textbf{实验结果}\,——\,翻译质量与消融分析\\[8pt]
  \textbf{\color{accentcolor}四}\>\textbf{总结与展望}\,——\,贡献与未来方向\\
  \end{tabbing}
  }
\end{frame}
```

### Critical: Figure Extraction from PDF

**NEVER use full-page PDF screenshots as figures.** When source is PDF:

1. Use `pdfimages -all paper.pdf materials/figures/` to extract embedded vector/raster images
2. If `pdfimages` not available, use `mutool extract` or Python `PyMuPDF`
3. If only `pdftoppm` is available, crop the figure region ONLY:
   - First identify figure bounding box coordinates
   - Use Python PIL to crop the figure out of the page image
   - Remove surrounding text, page numbers, captions
4. **Quality check**: if extracted figure contains visible paper text around it, it's WRONG — re-crop
5. For well-known papers (Transformer, ResNet, etc.), consider re-drawing key diagrams with tikz

### Critical: Anti-AI Writing Style (NO Bullet List Abuse)

**The #1 sign of AI-generated slides is overuse of `\begin{itemize}` bullet lists.**

Rules:
- **80% of text-only pages must use paragraph style** (连贯段落), NOT bullet points
- `\item` lists are ONLY acceptable for: innovation points, limitations, future work (list layout)
- For explaining a concept: write 2-3 flowing paragraphs with `\vskip0.2cm` between them
- For describing a method: use paragraph + inline `\alert{}` keywords, NOT itemized steps
- Use `\textbf{关键词}\,——\,解释文字` pattern for inline emphasis instead of bullets
- Use `\keybox{}` for a single key conclusion, NOT a list of conclusions

Bad (AI味重):
```latex
\begin{itemize}
  \item Self-attention 复杂度为 $O(n^2 \cdot d)$
  \item 顺序操作为 $O(1)$
  \item 最大路径长度为 $O(1)$
\end{itemize}
```

Good (段落化):
```latex
Self-Attention 的核心优势在于其\alert{常数级最大路径长度}——任意两个位置之间只需
一步即可直接交互，远优于 RNN 的 $O(n)$ 和 CNN 的 $O(\log_k n)$。虽然每层复杂度为
$O(n^2 \cdot d)$，但可通过高度优化的矩阵乘法实现，且顺序操作仅为 $O(1)$，
天然支持\alert{完全并行化}训练。
```

### Content Quality Rules

| Constraint | Value |
|-----------|-------|
| Text per page (text-only) | 150–200 chars, **paragraph style** |
| Text per page (with figure) | 100–150 chars |
| Equations per page | max 2 |
| Table rows | 3–8 |
| `\alert{}` keywords per page | 1–2 |
| Paragraph style | Full sentences, flowing paragraphs, NOT bullet lists |
| `\item` usage | ONLY on list-layout pages (创新点/局限/展望) |
| Inline emphasis | `\textbf{词}\,——\,解释` or `\alert{词}` |

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

## Phase 5: Interactive Editing (Guided Choices)

Present result:

> ✅ PDF 已生成：./defense.pdf（共 XX 页，预计答辩时长 XX 分钟）
> 说修改意见，或说"满意"结束。

### 5.1 Guided Modification (Never Let User Struggle to Express)

When user gives vague feedback, **offer concrete choices** instead of asking them to describe:

| User says | Respond with choices |
|-----------|---------------------|
| "这页不好看" | "你觉得是：A. 文字太密想拆成两页？B. 图太小想换成满版图？C. 想换个版式？" |
| "这里有点奇怪" | "我看到可能的问题：A. 图文重叠了 B. 文字太学术想简化 C. 想加个过渡说明？" |
| "第三章不太行" | "第三章目前15页。你想：A. 整体缩减（砍到10页）？B. 某几页太密拆开？C. 补一页总结？" |
| "改好看点" | "我可以：A. 加几页满版图让节奏更松 B. 关键结论用高亮框突出 C. 换个配色？" |

**Principle**: Always give 2–3 concrete options with preview of effect. User picks, not describes.

### 5.2 Modification Execution

| Type | Action |
|------|--------|
| Single page content edit | Edit corresponding `\begin{frame}...\end{frame}` |
| Add/remove page | Update outline.md, regenerate affected section |
| Global style change | Modify .sty or header |
| Layout switch | Replace frame with different layout skeleton |

After each edit, recompile and present again. Loop until user says done.

## Phase 6: Speaker Notes & Rehearsal Support (Optional)

After user confirms the slides are satisfactory, offer:

> 需要我帮你生成讲稿和配速建议吗？可以帮助你控制答辩节奏。

If user accepts, generate `notes.md`:

### 6.1 Per-Page Speaker Notes

```markdown
## P4 — 寒武纪辐射与软体动物的演化窗口
⏱️ 建议时长: 45秒

### 要点提词
- 演化窗口: 5.41亿年前，持续4000万年
- 软体动物门: 现代海洋第二大门类
- 272个属: 本文研究对象

### 讲稿参考
"首先介绍一下研究背景。寒武纪是海洋生态系统大规模重组的关键时期……"
```

### 6.2 Time Pacing Table

Present pacing summary in conversation:

> ## ⏱️ 时间配速建议（总计 20 分钟）
>
> | 章 | 页数 | 建议时长 | 每页均速 |
> |---|------|---------|---------|
> | 一 研究背景 | 8页 | 4分钟 | 30秒/页 |
> | 二 数据构建 | 7页 | 3.5分钟 | 30秒/页 |
> | 三 演化机制 | 15页 | 9分钟 | 36秒/页（重点章节，可以慢一些） |
> | 四 结论展望 | 5页 | 2.5分钟 | 30秒/页 |
> | 致谢+缓冲 | 1页 | 1分钟 | — |
>
> ⚠️ 第三章是重点，建议对关键结果页多花时间讲解。

### 6.3 Beamer Notes Integration (Optional)

If user wants notes embedded in PDF (for dual-screen presentation mode):

```latex
\setbeameroption{show notes on second screen=right}
```

Add `\note{}` blocks to each frame in `.tex` with the speaker notes content.

## Reference Files

- `references/layouts.md` — All 13 layout skeletons with slot definitions and LaTeX code
- `references/tex-header.md` — Standard .tex file preamble template
- `references/layout-registry.yaml` — Layout selection rules in structured format

## Assets

- `assets/beamerthemeAcademic.sty` — Beamer theme file (copied to user project)
- `assets/config.yaml` — Configuration template (copied to user project)
