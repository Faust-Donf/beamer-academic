#!/bin/bash
# Compile Beamer LaTeX to PDF (run twice for cross-references)
# Usage: bash scripts/compile.sh [filename]

FILE="${1:-defense.tex}"
BASE="${FILE%.tex}"

echo "Compiling ${FILE}..."
xelatex -interaction=nonstopmode "${FILE}" > /dev/null 2>&1
xelatex -interaction=nonstopmode "${FILE}" > /dev/null 2>&1

if [ -f "${BASE}.pdf" ]; then
    echo "✅ ${BASE}.pdf generated successfully"
    exit 0
else
    echo "❌ Compilation failed. Check ${BASE}.log for errors."
    exit 1
fi
