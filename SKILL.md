# Beamer Academic - 学术报告 Beamer 幻灯片生成器

一键从论文生成高质量学术报告 Beamer 幻灯片（答辩/开题/会议），内置 13 种专业版式模板，支持交互式修改。

## 触发词

beamer-academic, 学术PPT, 答辩PPT, 论文答辩幻灯片, beamer幻灯片, 开题PPT, 学术报告PPT, 会议PPT, beamer slides

## 前置条件

- 当前目录下有论文文件（`.pdf` 或 `.docx`）
- 系统已安装 `xelatex`（macOS: `brew install --cask mactex`）
- 系统已安装中文字体（macOS 默认有宋体/黑体/楷体）

## 执行流程

### Phase 0: 环境检查与配置

1. **检查论文文件**：在当前目录查找 `.pdf` 或 `.docx` 文件
   - 找到多个：询问用户使用哪个
   - 未找到：提示用户将论文放到当前目录

2. **检查编译环境**：
   ```bash
   which xelatex
   ```
   不存在则提示安装方法。

3. **检查/创建 config.yaml**：
   - 如已有 `config.yaml`：读取配置
   - 如没有：询问用户以下基本信息后生成
     - 学校名称
     - 院系名称
     - 姓名
     - 导师姓名+职称
     - 专业
     - 报告类型（答辩/开题/会议）
     - 配色偏好（蓝/红/绿/紫/青）

---

### Phase 1: 素材提取

**目标**：从论文中提取图片、表格、公式，建立素材库。

**操作**：
```
mkdir -p materials/{figures,tables}
```

1. **提取图片**：
   - PDF 论文：使用 `pdfimages` 或读取 PDF 中的图片引用
   - 将所有图片复制到 `materials/figures/`
   - 按论文中出现顺序命名：`fig_001.png`, `fig_002.png`, ...

2. **提取表格**：
   - 读取论文中的表格内容
   - 转为 LaTeX `booktabs` 格式
   - 保存到 `materials/tables/table_001.tex`, `table_002.tex`, ...

3. **提取公式**：
   - 读取论文中的关键公式
   - 保存为 LaTeX 源码到 `materials/equations.md`
   - 格式：`## 公式名称\n```latex\n...\n```\n`

4. **提取结构**：
   - 分析论文章节结构
   - 保存到 `materials/structure.md`
   - 格式：章节层级 + 每节核心内容摘要（50字以内）

**产出**：`materials/` 目录及其内容

---

### Phase 2: 大纲生成

**目标**：生成 `outline.md`——每一页的版式分配与内容摘要。

**输入**：`materials/structure.md` + 论文全文 + `_registry.yaml` 版式规则

**版式选型规则**（按优先级）：
1. 第一页必须是 `cover`
2. 第二页必须是 `toc`
3. 每章第一页必须是 `section-divider`
4. 含核心公式/模型定义 → `formula`
5. 含多行数据对比结果 → `table`
6. 图片信息量大（多面板、热力图） → `full-image`
7. 图片辅助说明（文为主） → `text-left-image-right`
8. 图为主体+数据解读 → `image-left-text-right`
9. 纯概念解释/背景叙述 → `text-only`
10. 每章最后有明确结论 → `conclusion-box`
11. 两章之间 → `transition`
12. 并列要点（创新、局限、展望） → `list`
13. 最后一页 → `thanks`

**节奏控制**：
- 避免连续 3 页使用相同版式
- 每章内版式应多样化（至少 3 种不同版式）
- 信息密度递进：先易后难，先概念后数据

**outline.md 格式**：
```markdown
# 答辩PPT大纲

## 基本信息
- 报告类型: 答辩
- 目标页数: 42
- 时间: 20分钟

## 页面大纲

### P1 [cover]
标题: XXXX
作者/导师/专业/日期

### P2 [toc]
章节结构: 6章

### P3 [section-divider]
一、研究背景与科学问题

### P4 [text-only]
标题: XXXX
内容摘要: （50字描述本页要讲什么）

### P5 [text-left-image-right]
标题: XXXX
左文: （内容摘要）
右图: fig_001.png (图说)

...
```

**★ 断点**：生成 `outline.md` 后暂停，告知用户：

> 大纲已生成，请查看 `outline.md`。你可以：
> - 直接说"ok"继续生成
> - 说"P7改成满版图"等修改指令
> - 说"第三章加一页方法流程图"等增删页面指令

等待用户确认后进入 Phase 3。

---

### Phase 3: 内容生成

**目标**：根据 `outline.md` 逐页生成完整 `.tex` 文件。

**操作流程**：

1. **生成文件头**：
   ```latex
   \documentclass[aspectratio={{ASPECT_RATIO}}, {{FONT_SIZE}}]{beamer}
   \usepackage{beamerthemeAcademic}
   {{COLOR_COMMAND}}  % 如 \usered

   % 中文字体
   \usepackage{xeCJK}
   \setCJKmainfont{{{CJK_MAIN}}}[BoldFont={{CJK_SANS}}, ItalicFont=Kaiti SC]
   \setCJKsansfont{{{CJK_SANS}}}
   \setCJKmonofont{{{CJK_MONO}}}
   \setmainfont{Times New Roman}
   \setsansfont{Helvetica}

   % 通用宏包
   \usepackage{amsmath, amssymb, amsfonts}
   \usepackage{booktabs}
   \usepackage{colortbl}
   \usepackage{multirow}
   \usepackage{array}
   \usepackage{hyperref}
   \usepackage{tikz}
   \usetikzlibrary{arrows.meta, positioning, calc}

   \setlength{\emergencystretch}{2em}
   \graphicspath{{materials/figures/}{./}}
   \AtBeginSection[]{}

   % 个人信息
   \title[{{SHORT_TITLE}}]{{{FULL_TITLE}}}
   \author[{{AUTHOR}}]{{{AUTHOR}}}
   \institute[{{INSTITUTE}}]{{{INSTITUTE}} {{DEPARTMENT}}}
   \date{{{DATE}}}
   \setsupervisor{{{SUPERVISOR}}}
   \setmajor{{{MAJOR}}}

   \begin{document}
   ```

2. **逐页生成**：
   - 读取 `outline.md` 中每页的 layout 分配
   - 从 `layouts/` 目录加载对应版式骨架
   - 根据论文内容填充各个 slot
   - 注意：
     - 每页文字控制在 **150-200字**（按1分钟/页计算）
     - 公式直接从 `materials/equations.md` 引用
     - 图片路径指向 `materials/figures/`
     - 表格从 `materials/tables/` 引用或内联
     - 使用 `\alert{}` 标注每页 1-2 个关键词

3. **生成文件尾**：
   ```latex
   \end{document}
   ```

4. **复制主题文件**：
   ```bash
   cp ~/.claude/skills/beamer-academic/theme/beamerthemeAcademic.sty ./
   ```

**产出**：`defense.tex` + `beamerthemeAcademic.sty`

---

### Phase 4: 编译

**操作**：
```bash
xelatex -interaction=nonstopmode defense.tex && xelatex -interaction=nonstopmode defense.tex
```

**错误处理**：
- 如编译失败，读取 `defense.log` 分析错误
- 常见问题自动修复：
  - 图片找不到：检查路径，尝试备选扩展名
  - 字体缺失：切换到系统可用字体
  - hbox overfull：添加 `\emergencystretch` 或调整文字
  - 未定义命令：检查宏包依赖
- 修复后重新编译（最多 3 次尝试）

**产出**：`defense.pdf`

---

### Phase 5: 交互修改循环

**展示结果**：
> ✅ PDF 已生成：`./defense.pdf`
> 
> 共 XX 页，请查看后告诉我需要修改什么。你可以说：
> - "P7 的公式太密了，分成两页"
> - "第三章增加一页方法流程图"
> - "全局配色换成红色"
> - "P12 的表格加上高亮行"
> - "满意了，结束"

**修改类型处理**：

| 修改类型 | 处理方式 |
|---------|---------|
| 单页内容修改 | 直接编辑 .tex 对应 frame |
| 增删页面 | 更新 outline.md → 重新生成受影响部分 |
| 全局样式修改 | 修改 .sty 或文件头配置 |
| 版式切换 | 替换对应页的 layout 骨架 |

每次修改后自动重新编译并告知结果。

**结束条件**：用户说"满意"/"结束"/"ok不改了"。

---

## 版式库参考

本 skill 内置 13 种经过实战验证的学术报告版式：

| 版式 | 文件 | 适用场景 |
|------|------|---------|
| 封面页 | `cover.tex` | 第一页 |
| 多级目录 | `toc.tex` | 第二页 |
| 章节分隔 | `section-divider.tex` | 每章开头 |
| 纯文段 | `text-only.tex` | 概念解释、背景叙述 |
| 左文右图 | `text-left-image-right.tex` | 文为主+配图 |
| 左图右文 | `image-left-text-right.tex` | 图为主+解读 |
| 公式页 | `formula.tex` | 模型/公式定义 |
| 表格页 | `table.tex` | 数据对比结果 |
| 满版图 | `full-image.tex` | 大图/多面板图 |
| 结论框 | `conclusion-box.tex` | 核心结论高亮 |
| 过渡页 | `transition.tex` | 承上启下 |
| 列表页 | `list.tex` | 并列要点 |
| 致谢页 | `thanks.tex` | 最后一页 |

版式详细定义见 `layouts/_registry.yaml`，每种版式的 LaTeX 骨架见 `layouts/*.tex`。

---

## 内容生成质量规则

### 文字风格
- **学术但不晦涩**：用完整句子，避免纯列表堆砌
- **段落化**：每页 2-3 段连贯文字，不是 bullet point 列表
- **关键词标注**：每页用 `\alert{}` 标注 1-2 个最核心的术语或结论
- **避免空洞**：不写"具有重要意义"等套话，直接说具体发现

### 页面密度
- 纯文段页：150-200 字
- 左文右图/左图右文：文字部分 100-150 字
- 公式页：公式 1-2 个 + 解释 80-120 字
- 表格页：表格 3-8 行 + 结论 80-120 字
- 满版图页：仅图说 1 句话

### 结构节奏
- 每章 5-8 页
- 背景章可以稍短（4-6 页）
- 方法+结果章最长（6-10 页）
- 结论章简洁（3-5 页）

---

## 配色方案

通过 `config.yaml` 的 `color_scheme` 字段切换：

| 方案 | 命令 | RGB | 适合 |
|------|------|-----|------|
| 蓝色（默认）| `\useblue` | (26, 58, 92) | 理工科、通用 |
| 红色 | `\usered` | (139, 0, 0) | 人文社科、中国高校传统色 |
| 绿色 | `\usegreen` | (0, 100, 60) | 农林环境、生命科学 |
| 紫色 | `\usepurple` | (75, 0, 110) | 文科、艺术 |
| 青色 | `\useteal` | (0, 80, 100) | 医学、海洋 |

---

## 注意事项

1. **图片质量**：建议使用 300dpi 以上的图片，矢量图（PDF/SVG）更佳
2. **公式来源**：优先从论文中直接提取 LaTeX 源码，避免重新手写
3. **编译次数**：至少编译 2 次以确保交叉引用正确
4. **字体兼容**：macOS 与 Linux 的中文字体名不同，`config.yaml` 中有说明
5. **备份**：每次大改之前建议 `cp defense.tex defense_backup.tex`
