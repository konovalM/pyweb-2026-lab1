#!/usr/bin/env bash
# Собирает одну и ту же научную страницу тремя генераторами и печатает
# измерения (время сборки, вес страницы) — материал для таблицы P2 в отчёте.
# Запуск:  bash scripts/build_all.sh
set -euo pipefail
cd "$(dirname "$0")/.."

# Активируем venv, если есть
[ -d .venv ] && source .venv/bin/activate

# Quarto, установленный без sudo
export PATH="$HOME/.local/share/quarto/bin:$PATH"

page_kb() { du -k "$1" | cut -f1; }
gzip_kb() { gzip -c "$1" | wc -c | awk '{printf "%.1f",$1/1024}'; }

echo "== MkDocs =="
rm -rf site
t=$( { /usr/bin/time -p sh -c 'mkdocs build --strict >/dev/null 2>&1'; } 2>&1 | awk '/real/{print $2}')
echo "  build: ${t}s  page: $(page_kb site/research/rul-vibration/index.html)KB  gzip: $(gzip_kb site/research/rul-vibration/index.html)KB"

echo "== Sphinx =="
rm -rf sphinx/_build
t=$( { /usr/bin/time -p sh -c 'sphinx-build -q -b html sphinx sphinx/_build/html >/dev/null 2>&1'; } 2>&1 | awk '/real/{print $2}')
echo "  build: ${t}s  page: $(page_kb sphinx/_build/html/rul-vibration.html)KB  gzip: $(gzip_kb sphinx/_build/html/rul-vibration.html)KB"

echo "== Quarto =="
if command -v quarto >/dev/null; then
  rm -rf quarto/_site
  t=$( { /usr/bin/time -p sh -c 'quarto render quarto >/dev/null 2>&1'; } 2>&1 | awk '/real/{print $2}')
  echo "  build: ${t}s  page: $(page_kb quarto/_site/rul-vibration.html)KB  gzip: $(gzip_kb quarto/_site/rul-vibration.html)KB"
else
  echo "  quarto не найден в PATH — пропуск"
fi
