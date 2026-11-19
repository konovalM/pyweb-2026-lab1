#!/usr/bin/env bash
# Собирает PDF из REPORT.md через Quarto (движок typst, без LaTeX).
# Запуск:  bash scripts/report-pdf.sh [файл.md]
set -euo pipefail
cd "$(dirname "$0")/.."

SRC="${1:-REPORT.md}"
export PATH="$HOME/.local/share/quarto/bin:$PATH"

command -v quarto >/dev/null || { echo "quarto не найден в PATH"; exit 1; }

quarto render "$SRC" --to typst
echo "Готово: ${SRC%.md}.pdf"
