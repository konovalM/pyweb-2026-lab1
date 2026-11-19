# О проекте

## Предметная область

**«Предиктивная сенсорика»** (Predictive Sensorics) — предиктивная диагностика
промышленного оборудования по данным датчиков вибрации, температуры и тока.
Цель публикаций — делиться методиками и результатами вычислительных
экспериментов в воспроизводимом виде.

## Стек публикации

| Слой | Инструмент |
|------|-----------|
| Генератор сайта | MkDocs + Material |
| Формулы | MathJax 3 (`pymdownx.arithmatex`) |
| Библиография | `mkdocs-bibtex` из `docs/refs.bib` |
| Графики | matplotlib (статика) + Plotly (интерактив) |
| Данные → графики | хук `scripts/gen_figures.py` на `on_pre_build` |
| CI/CD | GitHub Actions |
| Хостинг | GitHub Pages + Selectel (SSH-деплой) |

## Воспроизводимость

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve           # предпросмотр на http://127.0.0.1:8000
mkdocs build --strict  # строгая сборка: битые ссылки = ошибка
```

## Лицензии

- **Контент** (тексты, формулы, таблицы, рисунки) — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (`LICENSE-content`).
- **Код** (конфигурация, workflow'ы, скрипты) — [MIT](https://opensource.org/license/mit/) (`LICENSE`).

Разделение лицензий соответствует п.13 задания: контент и код публикуются
под разными лицензиями.
