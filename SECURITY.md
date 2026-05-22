# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅        |

## Reporting a Vulnerability

This project is a Claude Code Skill (AI prompt engineering + LaTeX templates). It does not handle authentication, networking, or sensitive data processing.

However, if you discover a security concern (e.g., the skill could be tricked into exposing file system content), please:

1. **Do NOT** open a public issue
2. Contact the maintainer via GitHub private vulnerability reporting
3. Describe the vulnerability and steps to reproduce

We will respond within 7 days.

## Scope

The skill executes:
- `xelatex` for PDF compilation
- File read/write operations within the project directory
- No network requests, no credential handling
