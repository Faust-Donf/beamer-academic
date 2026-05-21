# LaTeX File Header Template

Standard preamble for generated Beamer files. Fill placeholders from `config.yaml`.

```latex
\documentclass[aspectratio={{ASPECT_RATIO}}, {{FONT_SIZE}}]{beamer}

% ---------- Theme ----------
\usepackage{beamerthemeAcademic}
{{COLOR_COMMAND}}

% ---------- CJK Fonts (macOS) ----------
\usepackage{xeCJK}
\setCJKmainfont{{{CJK_MAIN}}}[BoldFont={{CJK_SANS}}, ItalicFont=Kaiti SC]
\setCJKsansfont{{{CJK_SANS}}}
\setCJKmonofont{{{CJK_MONO}}}
\setmainfont{Times New Roman}
\setsansfont{Helvetica}

% ---------- Packages ----------
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{booktabs}
\usepackage{colortbl}
\usepackage{multirow}
\usepackage{array}
\usepackage{hyperref}
\usepackage{tikz}
\usepackage{pifont}
\usetikzlibrary{arrows.meta, positioning, calc}

\setlength{\emergencystretch}{2em}
\graphicspath{{materials/figures/}{./}}
\AtBeginSection[]{}

% ---------- Accent colors for hypotheses (optional) ----------
\definecolor{textgray}{RGB}{90, 90, 90}
\definecolor{lightline}{RGB}{200, 200, 200}

% ---------- Metadata ----------
\title[{{SHORT_TITLE}}]{{{FULL_TITLE}}}
\author[{{AUTHOR}}]{{{AUTHOR}}}
\institute[{{INSTITUTE}}]{{{INSTITUTE}} {{DEPARTMENT}}}
\date{{{DATE}}}
\setsupervisor{{{SUPERVISOR}}}
\setmajor{{{MAJOR}}}

\begin{document}
```

## Color Command Mapping

| config.yaml `color_scheme` | LaTeX command |
|---------------------------|--------------|
| `blue` | `\useblue` |
| `red` | `\usered` |
| `green` | `\usegreen` |
| `purple` | `\usepurple` |
| `teal` | `\useteal` |

## Font Defaults by OS

| OS | CJK_MAIN | CJK_SANS | CJK_MONO |
|----|-----------|----------|----------|
| macOS | Songti SC | Heiti SC | STFangsong |
| Linux | Noto Serif CJK SC | Noto Sans CJK SC | Noto Sans Mono CJK SC |
