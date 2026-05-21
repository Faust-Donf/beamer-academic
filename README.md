<p align="center">
  <img src="docs/cover.png" width="400" alt="Beamer Academic Cover">
</p>

<h1 align="center">Beamer Academic</h1>

<p align="center">
  <strong>一键从论文生成高质量学术答辩 Beamer 幻灯片</strong><br>
  适用于 <a href="https://docs.anthropic.com/en/docs/claude-code">Claude Code</a> 的 Skill，内置 13 种专业版式
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> •
  <a href="#效果展示">效果展示</a> •
  <a href="#版式库">版式库</a> •
  <a href="#自定义">自定义</a>
</p>

---

## 这是什么？

把你的论文 PDF 丢进来，说一句"帮我做答辩PPT"，就能拿到一份 **可以直接上台答辩** 的 Beamer 幻灯片。

不需要会 LaTeX。不需要手动排版。不需要起 4 个 Agent 手动传文件。

**一个 Skill，端到端，从论文到 PDF。**

## 效果展示

以下为真实答辩 PPT 截图（个人信息已模糊）：

<table>
  <tr>
    <td align="center"><strong>封面页</strong></td>
    <td align="center"><strong>多级目录</strong></td>
  </tr>
  <tr>
    <td><img src="docs/cover.png" width="380"></td>
    <td><img src="docs/toc.png" width="380"></td>
  </tr>
  <tr>
    <td align="center"><strong>左文右图</strong></td>
    <td align="center"><strong>表格+假设</strong></td>
  </tr>
  <tr>
    <td><img src="docs/text-image.png" width="380"></td>
    <td><img src="docs/table.png" width="380"></td>
  </tr>
  <tr>
    <td align="center"><strong>图+统计结果</strong></td>
    <td align="center"><strong>致谢页</strong></td>
  </tr>
  <tr>
    <td><img src="docs/full-image.png" width="380"></td>
    <td><img src="docs/thanks.png" width="380"></td>
  </tr>
</table>

## 特性

| 能力 | 说明 |
|------|------|
| 一键生成 | 提供论文（.tex / .docx / .pdf），全流程自动 |
| 13 种版式 | 封面、目录、分隔页、纯文段、左文右图、左图右文、公式、表格、满版图、结论框、过渡、列表、致谢 |
| 交互修改 | 生成后按页码精准修改，无需懂 LaTeX |
| 5 种配色 | 蓝/红/绿/紫/青，一行配置切换 |
| 多场景 | 毕业答辩、开题报告、学术会议 |
| 自动纠错 | 检测图文重叠、溢出等排版问题并自动修复 |

## 快速开始

### 安装

```bash
git clone https://github.com/Faust-Donf/beamer-academic.git ~/.claude/skills/beamer-academic
```

### 前置依赖

**LaTeX 环境**（推荐安装，非必须）：

```bash
# macOS（推荐 no-gui 版，体积小）
brew install --cask mactex-no-gui

# Ubuntu / Debian
sudo apt install texlive-xetex texlive-lang-chinese texlive-fonts-recommended

# Fedora
sudo dnf install texlive-xetex texlive-xecjk

# Windows (WSL)
sudo apt install texlive-xetex texlive-lang-chinese
```

> **没有 LaTeX 环境？** 没关系！Skill 会生成 `.tex` 源文件，你可以上传到 [Overleaf](https://www.overleaf.com) 在线编译。

### 论文输入格式

| 格式 | 推荐度 | 说明 |
|------|--------|------|
| `.tex` | ⭐⭐⭐ | 最佳选择，图片和公式可直接复用 |
| `.docx` | ⭐⭐ | Word 文件，图片质量好 |
| `.pdf` | ⭐ | 可用，但图片提取可能有质量损失 |

### 使用

```bash
mkdir my-defense && cp 论文.docx my-defense/ && cd my-defense
```

然后在 Claude Code 中说：

> 帮我做答辩PPT

或输入 `/beamer-academic`

Skill 会问你几个基本信息（学校、姓名、导师、配色），然后全自动跑完。

## 工作流程

```
论文.pdf ─┐
          ▼
   ┌──────────────┐
   │  素材提取     │  图片 / 表格 / 公式 / 章节结构
   └──────┬───────┘
          ▼
   ┌──────────────┐
   │  大纲生成     │  自动分配 13 种版式
   └──────┬───────┘
          ▼
   ┌──────────────┐
   │ ★ 用户确认 ★ │  ← 唯一需要你动手的地方（说 ok 即可）
   └──────┬───────┘
          ▼
   ┌──────────────┐
   │  内容生成     │  逐页填充版式模板
   └──────┬───────┘
          ▼
   ┌──────────────┐
   │  编译出 PDF   │  xelatex × 2
   └──────┬───────┘
          ▼
   ┌──────────────┐
   │  交互修改     │  "P7公式太密了" → 自动拆页重编译
   └──────────────┘
```

## 版式库

13 种经过实战验证的学术报告版式，覆盖答辩 PPT 的所有页面类型：

| 版式 | 文件 | 何时用 |
|------|------|--------|
| 封面 | `cover.tex` | 第一页 |
| 目录 | `toc.tex` | 第二页，全文结构 |
| 章节分隔 | `section-divider.tex` | 每章开头，全色底 |
| 纯文段 | `text-only.tex` | 背景、动机、概念解释 |
| 左文右图 | `text-left-image-right.tex` | 文字为主 + 图辅助 |
| 左图右文 | `image-left-text-right.tex` | 图为主 + 文字解读 |
| 公式 | `formula.tex` | 模型定义、核心方程 |
| 表格 | `table.tex` | 实验结果、数据对比 |
| 满版图 | `full-image.tex` | 时序图、热力图、大图 |
| 结论框 | `conclusion-box.tex` | 核心结论高亮 |
| 过渡 | `transition.tex` | 承上启下 |
| 列表 | `list.tex` | 创新点、局限、展望 |
| 致谢 | `thanks.tex` | 最后一页 |

每种版式的详细定义见 [`layouts/_registry.yaml`](layouts/_registry.yaml)。

## 配色方案

```yaml
# assets/config.yaml
color_scheme: "blue"   # blue | red | green | purple | teal
```

| 方案 | 色值 | 推荐 |
|------|------|------|
| 蓝色 | `rgb(26, 58, 92)` | 理工科通用（默认） |
| 红色 | `rgb(139, 0, 0)` | 人文社科 |
| 绿色 | `rgb(0, 100, 60)` | 农林、环境、生科 |
| 紫色 | `rgb(75, 0, 110)` | 文科、艺术 |
| 青色 | `rgb(0, 80, 100)` | 医学、海洋 |

## 自定义

### 换成自己学校

```yaml
# assets/config.yaml
institution:
  name: "你的大学"
  department: "你的学院"
  logo: "your-logo.png"
  gate_image: "your-gate.png"   # 致谢页（可选）

color_scheme: "red"
```

### 添加新版式

1. 在 `references/layouts.md` 中添加新的 layout section
2. 在 `references/layout-registry.yaml` 中注册（定义 `when` 和 `slots`）
3. 完成

## 项目结构

```
beamer-academic/
├── SKILL.md                           # 主技能文件（AI 读取）
├── references/
│   ├── layouts.md                     # 13 种版式 LaTeX 骨架
│   ├── layout-registry.yaml          # 版式选型规则
│   └── tex-header.md                  # .tex 文件头模板
├── assets/
│   ├── beamerthemeAcademic.sty        # Beamer 主题文件
│   └── config.yaml                    # 用户配置模板
├── scripts/
│   └── compile.sh                     # 编译脚本
├── docs/                              # README 展示截图
└── README.md                          # 本文档
```

## 背景故事

这个项目源自我用 Claude Code 给自己做毕业答辩 PPT 的经历——做完被导师夸"PPT 很好"。

我把这套工作流总结成 SOP 发到小红书后意外爆火。原始 SOP 需要手动起 4 个 Agent、来回传文件，门槛不低。于是我把整个流程封装成了一个 Skill：**一句话触发，全自动交付**。

原始 SOP（4 步手动版）：
1. Agent1：参考 PPT → beamer 模板
2. Agent2：论文 → 素材库（图/表/公式）
3. Agent3：论文 → 答辩大纲 PRD
4. Agent4：模板 + 素材 + PRD → 最终 PPT

本 Skill 将以上全部封装为一条自动化管道 + 13 种结构化版式模板，开箱即用。

## 作者

**Faustus** · [小红书主页](https://xhslink.com/m/2JQ3fmTu6dz)

> 在小红书收获了 23.7K 次赞与收藏

## License

MIT
