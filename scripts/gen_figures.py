"""
Генерация графиков из исходных данных для научной страницы.

Воспроизводимый конвейер «данные → результат → сайт»:
    data/degradation.csv  ──►  docs/assets/generated/*.png / *.html

Запускается двумя способами:
  1. Самостоятельно:         python scripts/gen_figures.py
  2. Как MkDocs-хук:         подключён в mkdocs.yml (hooks:) и срабатывает
     на on_pre_build — поэтому `mkdocs build` всегда собирает графики из
     актуальных данных (достаточно изменить CSV → пересобрать сайт).

Статический график (matplotlib) и интерактивный (Plotly) закрывают
требование P2: «статический график + интерактивный график».
"""
from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")  # без дисплея, для CI
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "degradation.csv"
OUT = ROOT / "docs" / "assets" / "generated"

# Порог тревоги по RMS виброускорения (ISO 10816, зона C/D), мм/с^2
RMS_ALARM = 2.8


def load() -> pd.DataFrame:
    return pd.read_csv(DATA)


def static_rms(df: pd.DataFrame) -> pathlib.Path:
    """Статический график: рост RMS виброускорения и порог отказа (matplotlib)."""
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=120)
    ax.plot(df["cycle"], df["vibration_rms"], lw=1.1, color="#00796b",
            label="RMS виброускорения")
    ax.axhline(RMS_ALARM, ls="--", color="#d84315",
               label=f"Порог тревоги ISO 10816 = {RMS_ALARM} мм/с²")
    # Момент пересечения порога — оценка точки отказа
    crossed = df.loc[df["vibration_rms"] >= RMS_ALARM, "cycle"]
    if not crossed.empty:
        ax.axvline(crossed.iloc[0], ls=":", color="#455a64", alpha=0.7)
        ax.text(crossed.iloc[0] - 20, RMS_ALARM + 0.25,
                f"пересечение порога\n(цикл {int(crossed.iloc[0])})",
                ha="right", fontsize=8, color="#455a64")
    ax.set_xlabel("Цикл наблюдения, ч")
    ax.set_ylabel("RMS виброускорения, мм/с²")
    ax.set_title("Деградация подшипника: тренд виброускорения")
    ax.grid(alpha=0.25)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    out = OUT / "degradation_rms.png"
    fig.savefig(out)
    plt.close(fig)
    return out


def interactive_health(df: pd.DataFrame) -> pathlib.Path:
    """Интерактивный график: индекс здоровья HI(t) и эксцесс (Plotly)."""
    # Прореживаем до ~300 точек, чтобы html был лёгким
    d = df.iloc[::4]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=d["cycle"], y=d["health_index"], name="Индекс здоровья HI",
        line=dict(color="#00796b", width=2), yaxis="y1"))
    fig.add_trace(go.Scatter(
        x=d["cycle"], y=d["kurtosis"], name="Эксцесс (kurtosis)",
        line=dict(color="#d84315", width=1.5, dash="dot"), yaxis="y2"))
    fig.update_layout(
        title="Индекс здоровья и эксцесс сигнала (наведите курсор)",
        xaxis=dict(title="Цикл наблюдения, ч"),
        yaxis=dict(title="HI ∈ [0,1]", color="#00796b", range=[0, 1.05]),
        yaxis2=dict(title="Эксцесс", color="#d84315", overlaying="y",
                    side="right"),
        legend=dict(orientation="h", y=1.12),
        margin=dict(l=60, r=60, t=70, b=50),
        template="plotly_white", height=430)
    out = OUT / "rul_interactive.html"
    # include_plotlyjs='cdn' — лёгкий html; график тянет plotly.js с CDN
    fig.write_html(out, include_plotlyjs="cdn", full_html=True,
                   config={"displayModeBar": True, "responsive": True})
    return out


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    df = load()
    p1 = static_rms(df)
    p2 = interactive_health(df)
    print(f"[gen_figures] {p1.relative_to(ROOT)}  ({p1.stat().st_size // 1024} КБ)")
    print(f"[gen_figures] {p2.relative_to(ROOT)}  ({p2.stat().st_size // 1024} КБ)")


# --- Точка входа для MkDocs-хука ---
def on_pre_build(config, **kwargs):  # noqa: ARG001
    build()


if __name__ == "__main__":
    build()
