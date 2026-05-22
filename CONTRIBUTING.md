# Contributing to Beamer Academic

感谢你对本项目的兴趣！欢迎贡献代码、版式模板、配色方案或文档改进。

## 如何贡献

### 报告 Bug

1. 打开一个 [Issue](https://github.com/Faust-Donf/beamer-academic/issues/new?template=bug_report.md)
2. 描述问题：你做了什么、期望什么结果、实际发生了什么
3. 附上相关截图或 `.log` 文件

### 添加新版式

1. Fork 本仓库
2. 在 `references/layouts.md` 中添加新的 layout section
3. 在 `references/layout-registry.yaml` 中注册（定义 `when` 和 `slots`）
4. 在 `SKILL.md` 的 Layout Selection Rules 中添加触发条件
5. 提交 PR 并说明适用场景

### 添加新配色

1. 在 `assets/beamerthemeAcademic.sty` 中添加 `\definecolor` 和对应的 `\useXXX` 命令
2. 在 `assets/config.yaml` 注释中添加选项说明
3. 在 README 配色方案表中添加一行

### 改进 SKILL.md

如果你在使用中发现流程可以优化（比如某个 Phase 的提问方式不好），欢迎直接修改 `SKILL.md` 并提 PR。

## 开发规范

- Commit message 遵循 [Conventional Commits](https://www.conventionalcommits.org/)：`feat:`, `fix:`, `docs:`, `refactor:`
- SKILL.md 保持在 500 行以内
- 所有用户交互都在对话内完成，不要求用户打开文件
- 版式模板使用 `{{SLOT}}` 占位符格式

## 行为准则

参见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## 许可

贡献的代码将以 MIT 协议发布。
