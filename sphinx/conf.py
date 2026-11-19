"""
Конфигурация Sphinx + MyST — второй генератор для сравнения в P2.
Собирает ту же научную страницу, что и MkDocs, но на стеке Sphinx.
Сборка: sphinx-build -b html sphinx sphinx/_build/html  (или make -C sphinx html)
"""
import datetime

project = "Predictive Sensorics · Research"
author = "Predictive Sensorics / ИТМО"
copyright = f"{datetime.date.today().year}, Predictive Sensorics (CC BY 4.0)"
language = "ru"

extensions = [
    "myst_parser",              # Markdown (MyST) вместо reStructuredText
    "sphinxcontrib.bibtex",     # автосписок литературы из .bib
    "sphinx.ext.mathjax",       # формулы LaTeX
]

# Источник библиографии — общий с MkDocs (единый refs.bib в docs/)
bibtex_bibfiles = ["../docs/refs.bib"]
bibtex_default_style = "unsrt"      # нумерованный стиль [1], [2], ...
bibtex_reference_style = "label"

# Возможности MyST, нужные для научного контента P2
myst_enable_extensions = [
    "dollarmath",     # $...$ и $$...$$
    "amsmath",        # \begin{equation}, \label, нумерация
    "colon_fence",    # ::: директивы
    "deflist",
    "attrs_inline",
    "html_image",
    "substitution",
]
myst_dmath_double_inline = True
myst_heading_anchors = 3           # автоякоря для перекрёстных ссылок

# Нумерация рисунков/таблиц (для :numref: и подписей)
numfig = True
numfig_format = {"figure": "Рисунок %s", "table": "Таблица %s"}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]
html_title = "Predictive Sensorics · Research (Sphinx)"
