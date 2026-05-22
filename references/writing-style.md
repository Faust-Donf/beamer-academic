# Writing Style Guide

## Anti-AI Title & Content Check

Before finalizing, review ALL page titles and content for AI-flavored writing.

### Title Red Flags (must rewrite)

- ❌ "深入探讨..." / "全面分析..." / "系统研究..."
- ❌ "...的重要性" / "...的必要性"
- ❌ 过于宽泛的标题："方法论" / "实验部分" / "结果与讨论"
- ✅ 具体、有信息量："Gower 距离的混合度量" / "为什么选择 Self-Attention？"
- ✅ 像答辩学生会起的标题，不是综述论文的标题

### Content Red Flags (must rewrite)

- ❌ "值得注意的是..." / "需要指出的是..." / "总而言之..."
- ❌ "本研究具有重要的理论意义和实践价值"
- ❌ "综上所述" / "不难发现" / "显而易见"
- ❌ "在...的基础上" / "鉴于..." / "有鉴于此"
- ✅ 直接陈述事实和数据，不加空洞评价
- ✅ 用论文本身的术语和表达习惯，不要"翻译腔"

### Check Principle

读每一页标题，问自己"这像是答辩学生写的还是 AI 写的？"如果像 AI，改到像人。

---

## Page Composition Patterns (from real defense PPT)

### Pattern 1: 段落 + keybox

One paragraph of context → `\keybox{核心问题/结论}`

```latex
\begin{frame}
  \frametitle{驱动机制之一:外源突变与 Sinsk 事件}
  \chapnote{对应论文 \S 1.1.2}
  \vskip0.1cm

  Sinsk 事件 (约 513\,Ma) 是寒武纪早期具有代表性的生物危机。该时期沉积的黑色页岩中
  几乎寻不到生物扰动构造,指示\alert{缺氧环境的范围扩大}。

  \vskip0.2cm

  \keybox{\textbf{核心问题}:这一外源环境冲击是否能在形态空间中留下\alert{可识别的结构性变点}?}
\end{frame}
```

### Pattern 2: 段落 + 公式 + 段落

Context → display math → interpretation

```latex
\begin{frame}
  \frametitle{驱动机制之二:系统发育约束}
  \vskip0.1cm

  渐变假说关注系统内部约束在长时间尺度上的累积作用...

  \vskip0.2cm
  \[
    \mathrm{BM}:\; dX_t = \sigma\, dW_t,\qquad
    \mathrm{OU}:\; dX_t = \alpha(\theta - X_t)\,dt + \sigma\, dW_t.
  \]
  \vskip0.1cm

  OU 较 BM 多出向均值 $\theta$ 回复的项...
\end{frame}
```

### Pattern 3: 引言 + enumerate

Short intro → `\enumerate` with `\textbf{title}\,——\,explanation`

```latex
\begin{frame}
  \frametitle{现有研究的四点不足}
  \vskip0.15cm

  围绕...既有研究仍存若干局限:

  \vskip0.3cm
  \begin{enumerate}\setlength\itemsep{0.4em}
    \item \textbf{数据整合尺度不足}\,——\,多集中于单一埋藏库;
    \item \textbf{时间框架不统一}\,——\,分箱策略与年代对齐不一致;
  \end{enumerate}
\end{frame}
```

### Pattern 4: 段落 + 表格 + 结论

Context → booktabs table → conclusion paragraph

```latex
\begin{frame}
  \frametitle{研究目标与三个核心假设}
  \vskip0.1cm

  本文围绕"\alert{丰富度根植于多样性}"提出三个假设:

  \vskip0.25cm
  \begin{center}\small
  \begin{tabular}{@{}lll@{}}
    \toprule
    \textbf{编号} & \textbf{核心假设} & \textbf{检验方法} \\
    \midrule
    H1 & ... & ... \\
    \bottomrule
  \end{tabular}
  \end{center}

  \vskip0.25cm
  \small
  三者共同构成完整解释路径。
\end{frame}
```

### Pattern 5: columns(内联标记) + 图

Left text with `$\bullet$` inline markers + right image

```latex
\begin{frame}
  \frametitle{VASM 框架}
  \begin{columns}[T, onlytextwidth]
    \column{0.55\textwidth}
    \vskip0.1cm
    本文提出\alert{VASM 框架},把特征向量分解为两层:

    \vskip0.15cm
    \footnotesize
    $\bullet$ \textbf{全局核心层}:任意视角可估算的无量纲指标...

    \vskip0.1cm
    $\bullet$ \textbf{视角特异层}:仅特定投影可见的卷曲扩张率...

    \column{0.45\textwidth}
    \includegraphics[width=\linewidth]{figure.png}
    \figcap{VASM 示意图}
  \end{columns}
\end{frame}
```

### Pattern 6: 满版图 + 底部一句话

tikz overlay for large figure + `\figcap{}`

```latex
\begin{frame}
  \frametitle{三类指标的时间序列}
  \begin{tikzpicture}[remember picture, overlay]
    \node[anchor=center] at ([yshift=-0.25cm]current page.center) {%
      \includegraphics[width=0.90\paperwidth, height=0.70\paperheight, keepaspectratio]{figure.png}};
  \end{tikzpicture}
  \vskip-0.4cm
  \begin{flushleft}\scriptsize\itshape\color{textgray}
  图说文字
  \end{flushleft}
\end{frame}
```

---

## Rhythm Rule

Adjacent pages MUST use different composition patterns:

```
Bad:  P4段落, P5段落, P6段落, P7段落
Good: P4段落+keybox, P5左文右图, P6段落+公式+段落, P7段落+表格+结论
```
