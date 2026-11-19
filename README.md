# Predictive Sensorics · Research Site

Статический сайт для публикации результатов исследований по прогнозированию
технического состояния оборудования (вибродиагностика). Лабораторная работа 1
по курсу «Проектирование и развертывание веб-решений в эко-системе Python».

Основной генератор — **MkDocs + Material**. Та же научная страница собрана ещё
на **Sphinx + MyST** и **Quarto** для сравнения (практическое задание P2).

## Структура

```
docs/                     контент MkDocs (+ research/rul-vibration.md — страница P2)
  refs.bib                единый источник библиографии для всех трёх генераторов
data/degradation.csv      исходные данные эксперимента
scripts/gen_figures.py    data → графики (matplotlib + Plotly); хук mkdocs on_pre_build
scripts/build_all.sh      собрать всеми 3 генераторами + измерения
sphinx/                   вторая сборка (Sphinx + MyST)
quarto/                   третья сборка (Quarto)
.github/workflows/        gh-pages.yml (GitHub Pages) + deploy-selectel.yml (шаблон)
deploy/nginx.conf         пример конфига для своего хостинга
REPORT.md                 отчёт по лабораторной (T1 + P2)
LICENSE / LICENSE-content MIT (код) + CC BY 4.0 (контент)
```

## Локальный запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt            # MkDocs + графики
pip install -r requirements-sphinx.txt     # для сборки Sphinx (опционально)

mkdocs serve            # предпросмотр http://127.0.0.1:8000
mkdocs build --strict   # строгая сборка (битые ссылки = ошибка)

bash scripts/build_all.sh   # собрать всеми тремя генераторами + измерения
```

Quarto ставится отдельно (не через pip): <https://quarto.org/docs/get-started/>.

## Публикация

- **GitHub Pages** — автоматически через `.github/workflows/gh-pages.yml` при push
  в `main` (Settings → Pages → Source → GitHub Actions).
- **Отечественный хостинг (Selectel)** — `deploy-selectel.yml`: включается
  переменной `SELECTEL_ENABLED=true` и секретами с доступом к серверу.
