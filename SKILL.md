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

If missing, **recommend user to install** (this is a one-time setup, not optional):

> 你的系统还没有安装 LaTeX 环境。beamer PPT 需要 xelatex 编译，我来帮你装一下：

Then provide the command for user's OS and **offer to run it**:

| OS | Command |
|----|---------|
| macOS | `brew install --cask mactex-no-gui` (推荐，约3.5GB，装一次永久可用) |
| Ubuntu/Debian | `sudo apt install texlive-xetex texlive-lang-chinese texlive-fonts-recommended` |
| Fedora/RHEL | `sudo dnf install texlive-xetex texlive-xecjk` |
| Windows (WSL) | `sudo apt install texlive-xetex texlive-lang-chinese` |
| Arch | `sudo pacman -S texlive-xetex texlive-langchinese` |

Wait for installation to complete, verify with `which xelatex`, then proceed.

If user explicitly refuses to install (rare), fallback: deliver `.tex` + `.sty` + figures, suggest Overleaf.

### 0.3 Beamer Template (Ask User First)

Ask user about existing school beamer template:

> 你的学校/课题组有现成的 beamer 模板吗？（比如导师或师兄给过的 .sty 文件）
> - 有：请放到当前目录，我直接使用
> - 没有：我来帮你找或用内置通用模板

If user has a template: use it directly, skip the built-in theme.

If user has NO template:
1. Ask for school name
2. Search for existing public beamer templates for that school:
   - GitHub search: `{school name} beamer template`
   - Common sources: Overleaf Gallery, CTAN
3. If found: download and use (notify user which template)
4. If not found: use built-in `assets/beamerthemeAcademic.sty` with school logo
   - Ask: "你能提供学校 logo 图片吗？（放到当前目录即可）"
   - If no logo available: search online for the school's logo, or proceed without logo

### 0.4 Configuration

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
- **Chapnote preference**: "每页要不要显示'对应论文 §X.X'的标注？"（some users find it helpful for committee, others find it cluttered）

### 0.5 Language Strategy

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

### 2.0 Chapter Structure Principle

**Follow the thesis's own structure as the PRIMARY basis for PPT chapters.**

- If thesis has explicit chapters (第一章...第四章): map directly to PPT chapters
- If thesis has no chapters (like a conference paper with sections): group related sections into 3-5 logical chapters for the PPT
- Do NOT invent arbitrary chapter divisions that don't match the thesis logic
- The PPT chapter structure should feel natural to someone who has read the thesis

### 2.1 First Pass: Structure Proposal

After reading the thesis, propose the high-level structure directly in conversation:

> ## 📐 PPT 结构提案
>
> 根据你的论文结构，我建议这样安排：
>
> **总页数**：42 页（约 20 分钟答辩）
>
> | 章 | 标题 | 页数 | 对应论文 | 说明 |
> |---|------|------|---------|------|
> | 一 | 研究背景与科学问题 | 8页 | 第1章 | 背景+命题+假设+创新点 |
> | 二 | 数据构建与描述性分析 | 7页 | 第2章 | 数据来源+特征工程+时序总览 |
> | 三 | 演化模式与驱动机制 | 15页 | 第3章 | H1+H2+H3 三个假设检验 |
> | 四 | 结论与展望 | 5页 | 第4章 | 主要结论+局限+展望+成果 |
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

- Users who don't know markdown can follow along naturally in chat
- Iterative refinement is faster (no "go check that file" round-trip)
- Each chapter gets individual attention

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

**The #1 sign of AI-generated slides is overuse of `\begin{itemize}` and uniform page structure.**

Core rules:
1. Each page COMBINES multiple elements (段落+keybox, 段落+公式+段落, 段落+表格+结论)
2. Adjacent pages MUST use different composition patterns
3. `\begin{itemize}` is BANNED. Only `\enumerate` with intro paragraph allowed
4. 80% of pages use paragraph-style writing, not bullet points
5. Use inline patterns: `$\bullet$ \textbf{term}`, `\alert{keyword}`, `\textbf{title}\,——\,explanation`

**Read `references/writing-style.md` for 6 concrete composition patterns with LaTeX code examples.**

### Content Quality Rules

| Constraint | Value |
|-----------|-------|
| Text per page (text-only) | 150–200 chars |
| Text per page (with figure) | 100–150 chars |
| Equations per page | max 2 |
| Table rows | 3–8 |
| `\alert{}` keywords per page | 1–2 |
| Page structure | COMBINE multiple elements (see writing-style.md) |
| `\itemize` | BANNED |

### Section Divider = Outline Page (Enforced)

Every chapter boundary MUST use an Outline page (`\tableofcontents[currentsection]`).
This provides visual rhythm and structural navigation for the audience.

### Anti-AI Title & Content Check

Before finalizing, check all titles and content. **Read `references/writing-style.md`** for the full red-flag list.

Quick check: "这个标题/段落像答辩学生写的还是 AI 写的？" 如果像 AI，改到像人。

### Figure & Table Numbering

All figures and tables in the presentation MUST be numbered sequentially:

- Figures: `图 1`, `图 2`, `图 3`... (using `\figcap{图 1\;描述文字}`)
- Tables: in frame title or above table, mark as `表 1`, `表 2`...

Example:
```latex
\figcap{图 1\;Transformer 编码器--解码器架构}
\figcap{图 2\;多头注意力并行投影机制}
```

Table title pattern:
```latex
\frametitle{机器翻译 BLEU 对比（表 2）}
% or inside the frame:
{\small\textbf{表 1}\;不同层类型的复杂度对比}
```

Numbering must be consistent throughout — do not skip or repeat numbers.

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
