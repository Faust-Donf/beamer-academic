# Layout Library

13 professional page layouts for academic Beamer slides.
Each section contains the LaTeX skeleton and slot definitions for one layout type.

## Table of Contents

1. [cover](#cover) — 封面页
2. [toc](#toc) — 多级目录页
3. [section-divider](#section-divider) — 章节分隔页
4. [text-only](#text-only) — 纯文段页
5. [text-left-image-right](#text-left-image-right) — 左文右图
6. [image-left-text-right](#image-left-text-right) — 左图右文
7. [formula](#formula) — 公式推导页
8. [table](#table) — 数据表格页
9. [full-image](#full-image) — 满版图页
10. [conclusion-box](#conclusion-box) — 结论框页
11. [transition](#transition) — 过渡衔接页
12. [list](#list) — 列表页
13. [thanks](#thanks) — 致谢页

---

## cover

```latex
% Layout: cover (封面页)
% 使用场景: 第一页，展示论文标题、答辩人、导师、专业、院校、日期
% 依赖: \setsupervisor, \setmajor 命令（由主题定义）
%
% Slots:
%   {{TITLE}}       - 论文标题（可含换行 \\）
%   {{AUTHOR}}      - 答辩人姓名
%   {{SUPERVISOR}}  - 导师姓名+职称
%   {{MAJOR}}       - 专业名称
%   {{INSTITUTE}}   - 院校名称
%   {{DATE}}        - 答辩日期

\begin{frame}[plain]
  \titlepage
\end{frame}
```

---

## toc

```latex
% Layout: toc (多级目录页)
% 使用场景: 第二页，展示全文章节结构大纲
%
% Slots:
%   {{CHAPTERS}} - 章节列表，格式为 tabbing 环境内容
%
% 示例填充:
%   \textbf{\color{accentcolor}1}\>\textbf{研究背景与科学问题}\\[1pt]
%   \>\>{\scriptsize\color{textgray}关键词1、关键词2、关键词3}\\[4pt]

\begin{frame}
  \frametitle{汇报提纲}
  \vskip0.05cm
  {\footnotesize
  \begin{tabbing}
  \hspace{0.55cm}\=\hspace{0.80cm}\=\hspace{8cm}\kill
  {{CHAPTERS}}
  \end{tabbing}
  }
\end{frame}
```

---

## section-divider

```latex
% Layout: section-divider (章节分隔页)
% 使用场景: 每章开头，全色底+序号圆圈+章标题
%
% Slots:
%   {{CHAPTER_NUMBER}} - 中文数字（一、二、三...）
%   {{CHAPTER_TITLE}}  - 章标题文字

\sectiondivider{{{CHAPTER_NUMBER}}}{{{CHAPTER_TITLE}}}
```

---

## text-only

```latex
% Layout: text-only (纯文段页)
% 使用场景: 2-3段连贯文字解释概念性内容
%
% Slots:
%   {{TITLE}}      - 页标题
%   {{CHAPNOTE}}   - 对应论文章节标注（可选，留空则不显示）
%   {{PARAGRAPHS}} - 2-3段正文，段间用 \vskip0.2cm 分隔
%
% 注意: 每段控制在80-120字，总字数不超过300字

\begin{frame}
  \frametitle{{{TITLE}}}
  {{CHAPNOTE_LINE}}
  \vskip0.15cm

  {{PARAGRAPHS}}
\end{frame}

% --- chapnote 使用说明 ---
% 如有 chapnote，{{CHAPNOTE_LINE}} 替换为:
%   \chapnote{对应论文 \S X.X}
% 如无，则删除该行
```

---

## text-left-image-right

```latex
% Layout: text-left-image-right (左文右图)
% 使用场景: 文字描述为主，配合1-2张说明性图片
%
% Slots:
%   {{TITLE}}       - 页标题
%   {{CHAPNOTE}}    - 对应论文章节标注（可选）
%   {{LEFT_TEXT}}   - 左侧文字（120-180字，可含多段）
%   {{IMAGES}}      - 右侧图片区域（1-2张图+figcap）
%
% 布局: 左50% 文字 | 右50% 图片

\begin{frame}
  \frametitle{{{TITLE}}}
  {{CHAPNOTE_LINE}}
  \begin{columns}[T, onlytextwidth]
    \column{0.50\textwidth}
    \vskip0.15cm
    {{LEFT_TEXT}}

    \column{0.50\textwidth}
    \vskip0.05cm
    {{IMAGES}}
  \end{columns}
\end{frame}

% --- IMAGES 区域示例 ---
% 单张图:
%   \includegraphics[width=\linewidth, height=5.5cm, keepaspectratio]{image.png}
%   \figcap{图说文字}
%
% 双张图（上下排列）:
%   \includegraphics[width=\linewidth, height=3.4cm, keepaspectratio]{img1.png}
%   \figcap{图说1}
%   \vskip0.20cm
%   \includegraphics[width=\linewidth, height=3.4cm, keepaspectratio]{img2.png}
%   \figcap{图说2}
```

---

## image-left-text-right

```latex
% Layout: image-left-text-right (左图右文)
% 使用场景: 图/表是主体信息载体，右侧文字做数据解读
%
% Slots:
%   {{TITLE}}       - 页标题
%   {{CHAPNOTE}}    - 对应论文章节标注（可选）
%   {{LEFT_IMAGE}}  - 左侧图片（占40-62%宽度）
%   {{RIGHT_TEXT}}  - 右侧解读文字（100-150字）
%   {{STATS_TABLE}} - 可选的小型统计结果表
%
% 布局: 左40-62% 图片 | 右38-60% 文字+表

\begin{frame}
  \frametitle{{{TITLE}}}
  {{CHAPNOTE_LINE}}
  \vskip0.05cm
  \begin{columns}[T, onlytextwidth]
    \column{0.52\textwidth}
    \vskip0.1cm
    {{LEFT_IMAGE}}

    \column{0.48\textwidth}
    \vskip0.3cm
    \small
    {{RIGHT_TEXT}}

    {{STATS_TABLE}}
  \end{columns}
\end{frame}

% --- LEFT_IMAGE 示例 ---
%   \includegraphics[width=\linewidth, height=0.62\textheight, keepaspectratio]{image.png}
%   \figcap{图 X\;图说文字}
%
% --- STATS_TABLE 示例（可选）---
%   \vskip0.2cm
%   \begin{tabular}{@{}ll@{}}
%     \toprule
%     指标 & 数值 \\
%     \midrule
%     $R^{2}$ & $0.310$ \\
%     $P$ & $0.001$ \\
%     \bottomrule
%   \end{tabular}
```

---

## formula

```latex
% Layout: formula (公式推导页)
% 使用场景: 展示1-2个核心公式/模型定义
%
% Slots:
%   {{TITLE}}       - 页标题
%   {{CHAPNOTE}}    - 对应论文章节标注（可选）
%   {{INTRO_TEXT}}  - 公式引入文字（50-80字）
%   {{EQUATIONS}}   - LaTeX公式（displaymath环境）
%   {{EXPLANATION}} - 符号解释或结论文字（80-120字）
%
% 注意: 公式不超过2个/页，过多则拆分

\begin{frame}
  \frametitle{{{TITLE}}}
  {{CHAPNOTE_LINE}}
  \vskip0.1cm

  {{INTRO_TEXT}}

  \vskip0.1cm
  {{EQUATIONS}}
  \vskip0.1cm

  {{EXPLANATION}}
\end{frame}

% --- EQUATIONS 示例 ---
% 单公式:
%   \[
%     d_{ij} = \frac{\sum_{k=1}^{p} w_k \delta_{ijk} s_{ijk}}{\sum_{k=1}^{p} w_k \delta_{ijk}}
%   \]
%
% 双公式对比:
%   \[
%     \mathrm{BM}:\; dX_t = \sigma\, dW_t,\qquad
%     \mathrm{OU}:\; dX_t = \alpha(\theta - X_t)\,dt + \sigma\, dW_t.
%   \]
%
% --- EXPLANATION 示例 ---
%   \small
%   其中 $R_k$ 为连续性状取值范围，$\delta_{ijk}$ 为有效观测指示——
%   当任一样本缺失时该维度\alert{不参与距离计算}。
```

---

## table

```latex
% Layout: table (数据表格页)
% 使用场景: 展示实验结果、对比数据、多组统计量
%
% Slots:
%   {{TITLE}}      - 页标题
%   {{CHAPNOTE}}   - 对应论文章节标注（可选）
%   {{INTRO_TEXT}} - 表格说明文字（可选，50字以内）
%   {{TABLE}}      - booktabs 格式表格
%   {{CONCLUSION}} - 表下结论文字（80-120字）
%
% 注意: 表格行数3-8行，列数3-6列

\begin{frame}
  \frametitle{{{TITLE}}}
  {{CHAPNOTE_LINE}}
  \vskip0.1cm

  {{INTRO_TEXT}}

  \vskip0.15cm
  \begin{center}\small
  \setlength{\tabcolsep}{4pt}
  {{TABLE}}
  \end{center}

  \vskip0.2cm
  \small
  {{CONCLUSION}}
\end{frame}

% --- TABLE 示例 ---
%   \begin{tabular}{@{}lcccc@{}}
%     \toprule
%     \textbf{方法} & \textbf{精度} & \textbf{召回率} & \textbf{F1} & \textbf{$P$值} \\
%     \midrule
%     基线 & 0.72 & 0.68 & 0.70 & --- \\
%     \rowcolor{black!5}
%     \textbf{本文} & \textbf{0.89} & \textbf{0.85} & \textbf{0.87} & $0.003^*$ \\
%     \bottomrule
%   \end{tabular}
%
% 技巧:
%   - 用 \rowcolor{black!5} 高亮关键行
%   - 用 \alert{} 标注关键数值
%   - 用 \addlinespace[2pt] 增加行间距
```

---

## full-image

```latex
% Layout: full-image (满版图页)
% 使用场景: 图表信息量大，需要尽可能大地展示
%
% Slots:
%   {{TITLE}}      - 页标题
%   {{CHAPNOTE}}   - 对应论文章节标注（可选）
%   {{IMAGE_PATH}} - 图片文件路径
%   {{CAPTION}}    - 底部图说（一句话）
%
% 布局: 图片通过 tikz overlay 居中放大，占页面约70%面积

\begin{frame}
  \frametitle{{{TITLE}}}
  {{CHAPNOTE_LINE}}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=center] at ([yshift=-0.25cm]current page.center) {%
      \includegraphics[width=0.90\paperwidth, height=0.70\paperheight, keepaspectratio]{{{IMAGE_PATH}}}};
  \end{tikzpicture}
  \vskip-0.4cm
  \begin{flushleft}\scriptsize\itshape\color{textgray}
  {{CAPTION}}
  \end{flushleft}
\end{frame}

% --- 注意事项 ---
% 1. 图片通过 tikz overlay 定位，不受正常文本流影响
% 2. caption 放在左下角，用灰色小字
% 3. 如果图片有白色背景，效果最佳
% 4. 适合：时序图、散点图、热力图、多面板组合图
```

---

## conclusion-box

```latex
% Layout: conclusion-box (结论框页)
% 使用场景: 章/分析结束时总结核心发现，用高亮框突出关键结论
%
% Slots:
%   {{TITLE}}      - 页标题
%   {{CHAPNOTE}}   - 对应论文章节标注（可选）
%   {{BODY_TEXT}}  - 总结性正文（100-150字）
%   {{KEYBOX}}     - 高亮框内容（核心结论，50-80字）
%
% 视觉效果: 正文在上，keybox 在下方用浅灰底+细线框突出

\begin{frame}
  \frametitle{{{TITLE}}}
  {{CHAPNOTE_LINE}}
  \vskip0.2cm

  {{BODY_TEXT}}

  \vskip0.3cm

  \keybox{{{KEYBOX}}}
\end{frame}

% --- KEYBOX 内容示例 ---
%   \textbf{H2 成立}\,——\,Sinsk 事件邻域存在\alert{超出随机预期}的
%   形态空间结构性收缩，且收缩具有\alert{选择性过滤}特征。
%
% --- keybox 命令定义（在主题.sty中）---
%   \newcommand{\keybox}[1]{%
%     \begin{center}
%     \begin{tikzpicture}
%       \node[draw=lightline, line width=0.5pt, fill=black!4,
%             rounded corners=2pt, inner sep=6pt,
%             text width=0.92\linewidth, align=left, font=\small]{#1};
%     \end{tikzpicture}
%     \end{center}
%   }
```

---

## transition

```latex
% Layout: transition (过渡衔接页)
% 使用场景: 两章之间的逻辑桥梁，承上启下
%
% Slots:
%   {{TITLE}}     - 页标题（如 "从H1到H2：为何...？"）
%   {{SUMMARY}}   - 上一章结论概括（50-80字）
%   {{QUESTIONS}} - 引出的问题/下一步方向（itemize格式，2-3条）
%
% 结构: 先总结→再提问→引出下一章

\begin{frame}
  \frametitle{{{TITLE}}}
  \vskip0.2cm

  {{SUMMARY}}

  \vskip0.25cm

  {{QUESTIONS}}
\end{frame}

% --- SUMMARY 示例 ---
%   \alert{H1 已确认形态边界的先导地位}。沿这一线索，自然引出第二层问题：
%   既然形态多样性是丰富度变化的领先信号，那么\alert{是什么驱动了形态边界本身的变化}？
%
% --- QUESTIONS 示例 ---
%   \begin{itemize}\setlength\itemsep{0.4em}
%     \item \textbf{短期外源冲击 (H2)}\,——\,环境扰动是否在形态边界上留下结构性变点？
%     \item \textbf{长期内在约束 (H3)}\,——\,演化轨迹为何能够回归而非持续恶化？
%   \end{itemize}
```

---

## list

```latex
% Layout: list (列表页)
% 使用场景: 罗列3-5个并列要点（创新点、局限、展望、科研成果等）
%
% Slots:
%   {{TITLE}}      - 页标题
%   {{CHAPNOTE}}   - 对应论文章节标注（可选）
%   {{INTRO_TEXT}} - 引入文字（可选，50字以内）
%   {{ITEMS}}      - enumerate 列表内容
%
% 注意: 每条有简短解释，不是纯标题列表

\begin{frame}
  \frametitle{{{TITLE}}}
  {{CHAPNOTE_LINE}}
  \vskip0.15cm

  {{INTRO_TEXT}}

  \vskip0.2cm

  {{ITEMS}}
\end{frame}

% --- ITEMS 示例（enumerate 风格）---
%   \begin{enumerate}\setlength\itemsep{0.45em}
%     \item \textbf{属级数据整合与时间标尺统一}\,——\,以 \alert{272 属} 为基础，
%           构建对齐 ICS 标尺的出现-缺失矩阵;
%     \item \textbf{面向视角差异的形态表征 (VASM)}\,——\,将壳体几何分解为
%           视角无关核心层与视角特异层;
%     \item \textbf{多元时间序列方向性分析}\,——\,基于 VAR/Granger 与小波相干，
%           将经验叙事推进为\alert{可检验的统计命题};
%   \end{enumerate}
%
% --- ITEMS 示例（itemize 风格，适合局限/展望）---
%   \begin{itemize}\setlength\itemsep{0.4em}
%     \item 化石记录不完整，FAD/LAD 存在时间不确定性;
%     \item 主分析样本量有限 ($N=21$)，受小样本约束;
%     \item 分类学替代树以林奈层级近似系统发育关系。
%   \end{itemize}
```

---

## thanks

```latex
% Layout: thanks (致谢页)
% 使用场景: 最后一页，感谢答辩委员会
%
% Slots:
%   {{GATE_IMAGE}}  - 校门/标志建筑图文件名（可选，无则不显示图片）
%   {{THANKS_TEXT}} - 致谢主标语（如 "恳请各位老师批评指正"）
%   {{AUTHOR_INFO}} - 作者简短信息（如 "XX大学 XX学院 | 姓名"）
%
% 两种模式:
%   - 有 gate_image: 显示校门图 + 致谢文字
%   - 无 gate_image: 简洁致谢页（纯文字居中）

% === 模式A: 有校门图 ===
\begin{frame}[plain]
  \begin{tikzpicture}[remember picture, overlay]
    \fill[accentcolor] (current page.north west) rectangle
      ([yshift=-0.12cm]current page.north east);
    \fill[accentcolor] ([yshift=0.12cm]current page.south west) rectangle
      (current page.south east);
  \end{tikzpicture}
  \vbox to \paperheight\bgroup
    \vskip0.6cm
    \begin{center}
      {\color{accentcolor}\sffamily\fontsize{12pt}{14pt}\selectfont\addfontfeature{LetterSpace=20.0}THANK YOU}
    \end{center}
    \vskip0.4cm
    \begin{center}
      \includegraphics[width=0.86\paperwidth]{{{GATE_IMAGE}}}
    \end{center}
    \vfill
    \begin{center}
      {\color{accentcolor}\rule{1.6cm}{0.6pt}\hspace{0.5cm}\raisebox{0.18em}{$\bullet$}\hspace{0.5cm}\rule{1.6cm}{0.6pt}}\\[0.6cm]
      {\color{accentcolor}\sffamily\fontsize{26pt}{34pt}\selectfont\bfseries {{THANKS_TEXT}}}\\[0.5cm]
      {\color{textgray}\sffamily\fontsize{10pt}{12pt}\selectfont {{AUTHOR_INFO}}}
    \end{center}
    \vskip1.0cm
  \egroup
\end{frame}

% === 模式B: 无校门图（简洁版）===
% \begin{frame}[plain]
%   \begin{tikzpicture}[remember picture, overlay]
%     \fill[accentcolor] (current page.north west) rectangle (current page.south east);
%     \node[white, font=\fontsize{12pt}{14pt}\selectfont\sffamily] at ([yshift=2cm]current page.center)
%       {\addfontfeature{LetterSpace=20.0}THANK YOU};
%     \node[white, font=\fontsize{26pt}{34pt}\selectfont\bfseries\sffamily] at (current page.center)
%       {{{THANKS_TEXT}}};
%     \node[white!80, font=\fontsize{10pt}{12pt}\selectfont\sffamily] at ([yshift=-2cm]current page.center)
%       {{{AUTHOR_INFO}}};
%   \end{tikzpicture}
% \end{frame}
```

---

