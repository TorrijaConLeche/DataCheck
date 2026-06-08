

## Objetivo

Las métricas del sistema se implementarán de forma modular, extensible y separada del flujo principal del backend.

Cada métrica deberá poder calcularse sobre un `DataFrame` de Pandas y devolver un resultado estructurado.



---

## Estructura general

El sistema de métricas estará formado por los siguientes elementos:

```text
BaseMetric
MetricResult
MetricEngine
MetricRegistry
MetricSource
```

---

## BaseMetric

Todas las métricas heredarán de una clase base común.

Cada métrica deberá definir:

- `id`
    
- `name`
    
- `description`
    
- `source`
    
- `compute(df)`
    

La función `compute(df)` recibirá un `DataFrame` y devolverá un `MetricResult`.

En el futuro, algunas métricas podrán necesitar contexto adicional, por ejemplo columna objetivo, umbrales o rangos válidos. En la fase actual se mantiene `compute(df)` para simplificar.

---

## MetricSource

Se usará para clasificar el origen de cada métrica.

Valores posibles:

```python
ISO
PAPER
BASIC
```

- `ISO`: métricas procedentes del estándar ISO.
    
- `PAPER`: métricas procedentes de papers académicos.
    
- `BASIC`: métricas estadísticas o estructurales propias.
    

---

## MetricResult

Representará el resultado de calcular una métrica concreta sobre un dataset.

Campos principales:

```python
id
name
description
source
raw_value
normalized_value
interpretation
```

- `raw_value`: valor real calculado.
    
- `normalized_value`: puntuación normalizada entre 0 y 1, donde `1` representa el mejor resultado posible y `0` el peor resultado.
    
- `interpretation`: explicación textual breve del resultado.

El valor directo de la fórmula, especialmente en métricas ISO, deberá conservarse en `raw_value`. Si la fórmula original mide error, riesgo, divergencia o porcentaje negativo para la calidad, `normalized_value` deberá transformarse para mantener siempre la regla `1 = mejor` y `0 = peor`.
    

---

## Implementación de métricas

Cada métrica se implementará como una clase independiente.

Ejemplos:

```text
MissingValuesMetric
DuplicateRowsMetric
CompletenessMetric
ConsistencyMetric
ClassImbalanceMetric
...
```

Estructura actual:

```text
model/
├── base_metric.py
├── metric_result.py
├── metric_source.py
├── registry.py
└── metrics/
    ├── basic/
    └── iso/
        └── diversity/
```

Cada clase contendrá únicamente la lógica necesaria para calcular esa métrica.

---

## Patrón de diseño

Se usará el patrón **Strategy**.

Cada métrica será una estrategia distinta de cálculo, pero todas compartirán la misma interfaz:

```python
compute(df) -> MetricResult
```

Esto permitirá añadir nuevas métricas sin modificar el motor principal del sistema.

---

## MetricRegistry

Las métricas disponibles se registrarán en un punto central.

Ejemplo:

```python
METRIC_REGISTRY = {
    "missing_values": MissingValuesMetric(),
    "duplicate_rows": DuplicateRowsMetric(),
    "completeness": CompletenessMetric(),
}
```

El registro permitirá seleccionar, filtrar y ejecutar métricas de forma ordenada.

Actualmente el registro incluye:

- `null_percentage`
- `Div-ML-1`
- `Div-ML-2`
- `Div-ML-3`

---

## MetricEngine

El `MetricEngine` será el encargado de ejecutar las métricas.

Responsabilidades:

1. Recibir un `DataFrame`.
    
2. Obtener las métricas registradas.
    
3. Ejecutar cada métrica.
    
4. Recoger los resultados.
    
5. Devolver una lista de `MetricResult`.
    

---

## Gestión de errores

Si una métrica falla, no deberá detenerse todo el análisis.

El sistema devolverá un `MetricResult` indicando que esa métrica no ha podido calcularse.

Esto permite que un fallo en una métrica concreta no detenga el análisis completo.

---

## Flujo de análisis

```text
CSV cargado
    ↓
DataFrame de Pandas
    ↓
MetricEngine
    ↓
Métricas registradas
    ↓
Lista de MetricResult
    ↓
results/{dataset_id}.json
```

---


## Criterio principal

No se implementará una clase única con todos los métodos de cálculo.

Cada métrica será independiente, reutilizable y fácil de probar.

El sistema deberá permitir añadir nuevas métricas ISO, de papers o básicas sin modificar la lógica principal del análisis.

## Ejemplo de metricas ISO de diversidad implementadas

Las métricas de diversidad se implementan como una clase por cada identificador ISO:

- `Div-ML-1`: riqueza de etiquetas.
- `Div-ML-2`: abundancia relativa de etiquetas.
- `Div-ML-3`: diversidad de tamaño de categorías.

## Balance

Para la característica de balance, de momento se usarán estas métricas:

- `Bal-ML-3`: balance entre categorías.
- `Bal-ML-8`: balance de distribución de etiquetas.

No se implementan todavía las demás métricas de balance porque están orientadas a imagen y metadatos visuales (`brightness`, `resolution`, `bounding boxes`) o necesitan una definición de contexto más concreta para el CSV tabular.

## Input del usuario

Algunas métricas ISO no pueden calcularse únicamente a partir del CSV, ya que necesitan información de contexto indicada por el usuario.

En la fase actual se contemplan los siguientes parámetros:

- `TARGET_COLUMN`: columna objetivo del dataset. Normalmente representa la variable que se quiere predecir en un modelo de clasificación. Ejemplo: `Survived` en Titanic.
- `DIV_THRESHOLD`: umbral mínimo de cardinalidad para considerar que una clase tiene suficientes ejemplos en la métrica `Div-ML-3`.

Inicialmente estos valores pueden estar definidos de forma fija en el backend. En una fase posterior serán seleccionados por el usuario desde la interfaz.
