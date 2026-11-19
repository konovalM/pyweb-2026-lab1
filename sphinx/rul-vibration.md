(rul-page)=
# Прогноз остаточного ресурса подшипника по вибродиагностике

Страница собрана на **Sphinx + MyST** и содержит тот же научный контент, что и
MkDocs-версия: нумерованные формулы, таблицу с объединёнными ячейками,
статический и интерактивный графики, подсветку кода и автосписок литературы.

Задача прогностики (PHM[^phm]) — оценить остаточный ресурс узла по косвенным
признакам из сигнала виброускорения {cite}`lei2018machinery`.

[^phm]: PHM — Prognostics and Health Management, раздел технической диагностики.

(priznaki)=
## Признаки деградации

Базовый признак — среднеквадратичное значение (RMS) виброускорения на окне из
$N$ отсчётов $a_i$:

$$
\mathrm{RMS} = \sqrt{\frac{1}{N}\sum_{i=1}^{N} a_i^{\,2}}
$$ (eq:rms)

Более ранний индикатор зарождения дефекта — эксцесс (kurtosis)
{cite}`randall2011rolling`:

$$
\mathrm{Kurt} = \frac{\frac{1}{N}\sum_{i=1}^{N}(a_i-\bar a)^4}
{\left(\frac{1}{N}\sum_{i=1}^{N}(a_i-\bar a)^2\right)^{2}}
$$ (eq:kurt)

Признак {eq}`eq:kurt` срабатывает раньше, чем порог по {eq}`eq:rms` — это
перекрёстные ссылки на нумерованные уравнения.

```{figure} _static/generated/degradation_rms.png
:name: fig-rms
:width: 100%

Рост RMS виброускорения в течение жизненного цикла подшипника и порог тревоги
по ISO 10816.
```

(model)=
## Модель остаточного ресурса

Надёжность узла описываем распределением Вейбулла {cite}`weibull1951statistical`:

$$
R(t) = \exp\!\left[-\left(\frac{t}{\eta}\right)^{\beta}\right],
\qquad
\mathrm{RUL}(t_0) = \mathbb{E}[t - t_0 \mid t > t_0]
$$ (eq:rul)

Оценка по {eq}`eq:rul` выполняется в момент пересечения индексом здоровья порога
предупреждения. Динамику индекса показывает интерактивный график:

```{raw} html
<iframe src="_static/generated/rul_interactive.html"
        style="width:100%;min-height:440px;border:1px solid #ddd;border-radius:6px"
        title="Индекс здоровья и эксцесс (Plotly)" loading="lazy"></iframe>
```

### Пороговые зоны по ISO 10816

Таблица с объединёнными ячейками (`rowspan`/`colspan`) по {cite}`iso10816`:

```{raw} html
<table>
  <caption>Таблица 1. Зоны вибрации и регламент обслуживания (ISO 10816-3).</caption>
  <thead>
    <tr><th rowspan="2">Зона</th><th colspan="2">RMS виброскорости, мм/с</th>
        <th rowspan="2">Решение оператора</th></tr>
    <tr><th>от</th><th>до</th></tr>
  </thead>
  <tbody>
    <tr><td>A — новое</td><td>0.0</td><td>1.4</td>
        <td rowspan="2">Эксплуатация без ограничений</td></tr>
    <tr><td>B — допустимо</td><td>1.4</td><td>2.8</td></tr>
    <tr><td>C — контроль</td><td>2.8</td><td>4.5</td><td>Планировать обслуживание</td></tr>
    <tr><td>D — недопустимо</td><td>4.5</td><td>—</td><td>Останов, риск разрушения</td></tr>
  </tbody>
</table>
```

## Применимость и ограничения

```{raw} html
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin:1rem 0">
  <div>
    <strong>Где метод работает</strong>
    <ul>
      <li>Подшипники качения с выраженной ударной картиной дефекта.</li>
      <li>Наличие прогонов run-to-failure для калибровки порогов.</li>
      <li>Стационарные режимы нагрузки.</li>
    </ul>
  </div>
  <div>
    <strong>Где метод ломается</strong>
    <ul>
      <li>Переменная частота вращения.</li>
      <li>Единичные узлы без обучающей выборки отказов.</li>
      <li>Сильные внешние вибропомехи.</li>
    </ul>
  </div>
</div>
```

Дополнительный источник по калибровке на данных run-to-failure —
{cite}`saxena2008cmapss`.

## Воспроизводимый расчёт

Код вычисляет признаки {eq}`eq:rms`–{eq}`eq:kurt`:

```{code-block} python
:linenos:

import numpy as np
import pandas as pd

RMS_ALARM = 2.8  # порог тревоги, мм/с^2 (ISO 10816, зона C)


def features(window: np.ndarray) -> tuple[float, float]:
    rms = np.sqrt(np.mean(window ** 2))
    centered = window - window.mean()
    kurt = np.mean(centered ** 4) / (np.mean(centered ** 2) ** 2)
    return float(rms), float(kurt)


def first_alarm_cycle(df: pd.DataFrame) -> int | None:
    exceeded = df.loc[df["vibration_rms"] >= RMS_ALARM, "cycle"]
    return int(exceeded.iloc[0]) if not exceeded.empty else None
```

Переход к разделу {ref}`priznaki` — пример перекрёстной ссылки на другой раздел.

## Список литературы

```{bibliography}
```
