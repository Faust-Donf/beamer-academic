# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.4.0] - 2026-05-22

### ✨ Added
- Phase 1.2: Material confirmation — present figure catalog in-conversation, let user mark priorities
- Phase 0.4: Language strategy — handle English thesis → Chinese PPT with terminology mapping
- Phase 5.1: Guided modification — offer 2-3 concrete choices instead of making user describe changes
- Phase 6: Speaker notes & rehearsal — per-page notes, time pacing table, beamer notes integration

## [1.3.0] - 2026-05-22

### ✨ Added
- Phase 2 rewritten as 3-pass in-conversation brainstorm (structure → per-chapter → final confirm)
- All confirmation happens in chat, never requires user to open .md files
- Each chapter gets individual attention with per-page layout table

### 🗑️ Removed
- File-based outline.md confirmation (replaced by in-conversation flow)

## [1.2.0] - 2026-05-21

### ✨ Added
- Phase 0: Support `.tex` (best) > `.docx` > `.pdf` input priority with quality warnings
- Phase 0: LaTeX environment detection for all OS (macOS/Ubuntu/Fedora/Arch/WSL)
- Phase 0: Overleaf fallback for users without local LaTeX
- Phase 4.2: Layout bug detection — overlap prevention rules and auto-fix table
- Mandatory outline approval with three-level structure (chapter → section → page)

## [1.1.0] - 2026-05-21

### ♻️ Changed
- Restructured to standard skill format with YAML frontmatter
- `layouts/*.tex` → `references/layouts.md` (single reference file)
- `theme/` → `assets/` (standard skill asset directory)
- SKILL.md rewritten in imperative form, under 500 lines

### ✨ Added
- `references/tex-header.md` — LaTeX preamble template
- `scripts/compile.sh` — compilation helper script

## [1.0.0] - 2026-05-21

### ✨ Added
- Initial release
- 13 professional page layouts (cover, toc, section-divider, text-only, text-left-image-right, image-left-text-right, formula, table, full-image, conclusion-box, transition, list, thanks)
- 5 color schemes (blue, red, green, purple, teal)
- Universal academic beamer theme (`beamerthemeAcademic.sty`)
- Full pipeline: material extraction → outline → content → compile → interactive edit
- Layout registry with selection rules (`_registry.yaml`)
- User configuration template (`config.yaml`)

[1.4.0]: https://github.com/Faust-Donf/beamer-academic/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/Faust-Donf/beamer-academic/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/Faust-Donf/beamer-academic/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Faust-Donf/beamer-academic/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Faust-Donf/beamer-academic/releases/tag/v1.0.0
