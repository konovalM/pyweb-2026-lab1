# Прогноз остаточного ресурса подшипника по вибродиагностике

Страница демонстрирует публикацию результатов вычислительного эксперимента
средствами генератора статических сайтов: нумерованные формулы, таблицы с
объединёнными ячейками, статический и интерактивный графики, подсветку кода и
автоматический список литературы. Эта же страница собрана на втором генераторе
(Sphinx + MyST) — см. раздел [«Сравнение генераторов»](#sravnenie-generatorov).

Задача прогностики технического состояния (PHM[^phm]) — оценить **остаточный
ресурс** (Remaining Useful Life, RUL) узла по косвенным признакам, извлекаемым
из сигнала виброускорения, не доводя оборудование до отказа [@lei2018machinery].

[^phm]: PHM — Prognostics and Health Management, раздел технической диагностики,
    объединяющий детекцию дефекта, оценку тяжести и прогноз остаточного ресурса.

## Признаки деградации { #priznaki }

Базовый скалярный признак — среднеквадратичное значение (RMS) виброускорения на
окне из $N$ отсчётов $a_i$:

\[
\begin{equation}
\mathrm{RMS} = \sqrt{\frac{1}{N}\sum_{i=1}^{N} a_i^{\,2}}
\label{eq:rms}
\end{equation}
\]

RMS растёт монотонно по мере износа, но реагирует поздно. Более ранний индикатор
зарождения дефекта — эксцесс (kurtosis), чувствительный к ударным импульсам
в сигнале [@randall2011rolling]:

\[
\begin{equation}
\mathrm{Kurt} = \frac{\frac{1}{N}\sum_{i=1}^{N}(a_i-\bar a)^4}
{\left(\frac{1}{N}\sum_{i=1}^{N}(a_i-\bar a)^2\right)^{2}}
\label{eq:kurt}
\end{equation}
\]

Для исправного подшипника $\mathrm{Kurt}\approx 3$ (нормальное распределение);
рост выше указывает на появление дефекта. Признак из уравнения \(\eqref{eq:kurt}\)
срабатывает раньше, чем порог по \(\eqref{eq:rms}\) — это видно на интерактивном
графике ниже.

![Рост RMS виброускорения в течение жизненного цикла подшипника и порог тревоги по ISO 10816.](../assets/generated/degradation_rms.png)

## Модель остаточного ресурса { #model }

Надёжность узла описываем распределением Вейбулла [@weibull1951statistical] с
параметром формы $\beta$ и масштаба $\eta$:

\[
\begin{equation}
R(t) = \exp\!\left[-\left(\frac{t}{\eta}\right)^{\beta}\right],
\qquad
\mathrm{RUL}(t_0) = \mathbb{E}[t - t_0 \mid t > t_0]
\label{eq:rul}
\end{equation}
\]

Оценка остаточного ресурса по \(\eqref{eq:rul}\) выполняется в момент $t_0$, когда
индекс здоровья $\mathrm{HI}(t)$ пересекает порог предупреждения. Индекс здоровья
нормирован в $[0,1]$ и восстанавливается из RMS; его динамику вместе с эксцессом
показывает интерактивный график.

<iframe src="../../assets/generated/rul_interactive.html" class="plotly-embed" title="Интерактивный график индекса здоровья и эксцесса" loading="lazy"></iframe>
Figure: Индекс здоровья $\mathrm{HI}(t)$ и эксцесс сигнала (интерактивно, Plotly).

### Пороговые зоны по ISO 10816 { #zony }

Границы зон технического состояния для машин класса II приведены в таблице с
объединёнными ячейками (группировка по решению оператора):

<table markdown>
  <caption>Зоны вибрации и регламент обслуживания (по ISO 10816-3 [@iso10816]).</caption>
  <thead>
    <tr>
      <th rowspan="2">Зона</th>
      <th colspan="2">RMS виброскорости, мм/с</th>
      <th rowspan="2">Решение оператора</th>
    </tr>
    <tr>
      <th>от</th>
      <th>до</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A — новое оборудование</td>
      <td>0.0</td>
      <td>1.4</td>
      <td rowspan="2">Эксплуатация без ограничений</td>
    </tr>
    <tr>
      <td>B — допустимо</td>
      <td>1.4</td>
      <td>2.8</td>
    </tr>
    <tr>
      <td>C — требует контроля</td>
      <td>2.8</td>
      <td>4.5</td>
      <td>Планировать обслуживание</td>
    </tr>
    <tr>
      <td>D — недопустимо</td>
      <td>4.5</td>
      <td>—</td>
      <td>Останов, риск разрушения</td>
    </tr>
  </tbody>
</table>

## Применимость и ограничения { #primenimost }

<div class="two-col" markdown>
<div markdown>
**Где метод работает**

- Подшипники качения и зубчатые передачи с выраженной ударной картиной дефекта.
- Наличие исторических прогонов «run-to-failure» для калибровки порогов
  [@saxena2008cmapss].
- Стационарные режимы нагрузки, где тренд RMS интерпретируем.
</div>
<div markdown>
**Где метод ломается**

- Переменная частота вращения — RMS и эксцесс «плывут» без нормировки по режиму.
- Единичные узлы без обучающей выборки отказов.
- Сильные внешние вибропомехи соседних агрегатов маскируют ранний дефект.
</div>
</div>

## Воспроизводимый расчёт { #raschet }

Код ниже вычисляет признаки \(\eqref{eq:rms}\)–\(\eqref{eq:kurt}\) и момент
пересечения порога — ровно та логика, что питает графики выше:

```python linenums="1"
import numpy as np
import pandas as pd

RMS_ALARM = 2.8  # порог тревоги, мм/с^2 (ISO 10816, зона C)


def features(window: np.ndarray) -> tuple[float, float]:
    """RMS и эксцесс окна виброускорения."""
    rms = np.sqrt(np.mean(window ** 2))                 # (1)
    centered = window - window.mean()
    kurt = np.mean(centered ** 4) / (np.mean(centered ** 2) ** 2)
    return float(rms), float(kurt)


def first_alarm_cycle(df: pd.DataFrame) -> int | None:
    """Первый цикл, где RMS пересекает порог отказа."""
    exceeded = df.loc[df["vibration_rms"] >= RMS_ALARM, "cycle"]
    return int(exceeded.iloc[0]) if not exceeded.empty else None


if __name__ == "__main__":
    data = pd.read_csv("data/degradation.csv")
    print("Порог пересечён на цикле:", first_alarm_cycle(data))
```

!!! note "Как это связано со сборкой сайта"
    Эта логика вынесена в `scripts/gen_figures.py` и вызывается MkDocs-хуком на
    этапе `on_pre_build`: графики пересобираются из `data/degradation.csv` при
    каждой сборке. Подробнее о стеке — на странице [«О проекте»](../about.md).

## Сравнение генераторов { #sravnenie-generatorov }

Та же страница собрана двумя генераторами; поведение по ключевым элементам
научного контента сведено в таблицу (детали и измерения — в отчёте, раздел P2).

| Элемент контента            | MkDocs + Material            | Sphinx + MyST                 |
|-----------------------------|------------------------------|-------------------------------|
| Нумерованные формулы        | MathJax (`arithmatex`, ams)  | MathJax/`amsmath`, `:label:`  |
| `\eqref` из текста          | Да (MathJax tags)            | Да (`{eq}` role)              |
| Таблица с `colspan/rowspan` | Сырой HTML в Markdown        | `{list-table}` / сырой HTML   |
| Статический график          | `![]()` + плагин caption     | `.. figure::` directive       |
| Интерактивный Plotly        | `<iframe>` на html-фрагмент  | `raw:: html` / `nbsphinx`     |
| Автосписок литературы        | `mkdocs-bibtex` (`[@key]`)   | `sphinxcontrib-bibtex`        |
| Подсветка кода              | Pygments (`pymdownx`)        | Pygments (встроено)           |

## Список литературы

\bibliography
