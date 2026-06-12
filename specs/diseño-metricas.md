

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
FeatureConstraints
DatasetRules
```

---

## BaseMetric

Todas las métricas heredarán de una clase base común.

Cada métrica deberá definir:

- `id`
    
- `name`
    
- `description`
    
- `source`
    
- `compute(df, context=None)`
    

La función `compute(df, context=None)` recibirá un `DataFrame` y un diccionario opcional con contexto adicional (target_column, constraints, umbrales, etc.) y devolverá un `MetricResult`.

El contexto permite que métricas como `Eft-ML-1` accedan a las restricciones definidas por el usuario, o que `Div-ML-1` y `Bal-ML-3` conozcan la columna objetivo sin tenerla hardcodeada.

---

## FeatureConstraints y DatasetRules

Modelo que permite al usuario definir qué valores son válidos para cada feature del dataset y cuál es la columna objetivo.

### FeatureConstraints

Define las restricciones aplicables a una columna (feature):

```python
@dataclass
class FeatureConstraints:
    min: float | None = None
    max: float | None = None
    allowed_values: list[str | int | float] | None = None
    regex: str | None = None
    not_null: bool = False
```

- `min` / `max`: rango válido para columnas numéricas.
- `allowed_values`: valores permitidos para columnas categóricas.
- `regex`: patrón que debe cumplir el valor (columnas de texto).
- `not_null`: si es `True`, no se permiten valores nulos.

### DatasetRules

Agrupa la configuración completa del usuario para un dataset:

```python
@dataclass
class DatasetRules:
    target_column: str
    constraints: dict[str, FeatureConstraints]
```

- `target_column`: columna que contiene la etiqueta a predecir (target). Ejemplo: `Survived`.
- `constraints`: mapeo de columna → restricciones. Solo aparecen aquí las features (predictores).

Estos datos los envía el usuario mediante `POST /datasets/{id}/rules` y se almacenan en `storage/datasets/{dataset_id}-rules.json`.

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
├── feature_constraints.py
├── registry.py
└── metrics/
    ├── basic/
    └── iso/
        ├── diversity/
        ├── balance/
        └── effectiveness/
```

Cada clase contendrá únicamente la lógica necesaria para calcular esa métrica.

---

## Patrón de diseño

Se usará el patrón **Strategy**.

Cada métrica será una estrategia distinta de cálculo, pero todas compartirán la misma interfaz:

```python
compute(df, context=None) -> MetricResult
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
- `Bal-ML-3`
- `Bal-ML-8`
- `Eft-ML-1`

---

## MetricEngine

El `MetricEngine` será el encargado de ejecutar las métricas.

Responsabilidades:

1. Recibir un `DataFrame`.
    
2. Recibir un `context` opcional con la configuración del usuario (target_column, constraints).
    
3. Obtener las métricas registradas.
    
4. Ejecutar cada métrica pasando el `context`.
    
5. Recoger los resultados.
    
6. Devolver una lista de `MetricResult`.
    

---

## Gestión de errores

Si una métrica falla, no deberá detenerse todo el análisis.

El sistema devolverá un `MetricResult` indicando que esa métrica no ha podido calcularse.

Esto permite que un fallo en una métrica concreta no detenga el análisis completo.

---

## Flujo de análisis

```text
CSV cargado + rules.json
    ↓
DataFrame de Pandas + context (target_column, constraints)
    ↓
MetricEngine
    ↓
Métricas registradas (reciben context)
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



# Metricas ISO

## Auditabilidad
Implementación pendiente, necesita que el dataset a analizar contenga las columnas "auditado" y "auditable" (True o False) para poder calcular estas métricas.

## Diversidad

Las métricas de diversidad se implementan como una clase por cada identificador ISO:

- `Div-ML-1`: riqueza de etiquetas.
- `Div-ML-2`: abundancia relativa de etiquetas.
- `Div-ML-3`: diversidad de tamaño de categorías.

## Balance

Para la característica de balance, de momento se usarán estas métricas:

- `Bal-ML-3`: balance entre categorías.
- `Bal-ML-8`: balance de distribución de etiquetas.

No se implementan todavía las demás métricas de balance porque están orientadas a imagen y metadatos visuales (`brightness`, `resolution`, `bounding boxes`) o necesitan una definición de contexto más concreta para el CSV tabular.

## Efectividad

- `Eft-ML-1`: Feature Effectiveness.
  Proporción de muestras que cumplen con las restricciones definidas por el usuario para las features.

  ```
  Eft-ML-1 = A / B
  ```

  - A: número de muestras que cumplen TODAS las constraints definidas.
  - B: número total de muestras en el dataset.

  Evaluación: para cada fila, se verifica que cada feature con restricciones cumpla su condición (rango numérico, valor permitido, regex, no nulo). Si alguna falla, la fila no cuenta como válida.

  Interpretación: valor entre 0 y 1. Cercano a 1 indica que la mayoría de muestras tienen características aceptables para las features.

## Input del usuario

Algunas métricas ISO no pueden calcularse únicamente a partir del CSV, ya que necesitan información de contexto indicada por el usuario.

Actualmente el usuario configura los siguientes parámetros desde la interfaz, que se envían mediante `POST /datasets/{id}/rules`:

- `target_column`: columna objetivo del dataset. Representa la variable que se quiere predecir (target). Ejemplo: `Survived` en Titanic.
- `constraints`: restricciones de calidad por feature. Cada feature puede tener cero o más restricciones (`min`, `max`, `allowed_values`, `regex`, `not_null`).

Estos valores se persisten en `storage/datasets/{dataset_id}-rules.json` y se pasan como `context` a cada métrica durante el análisis.

Además, ciertas métricas pueden necesitar umbrales adicionales:
- `DIV_THRESHOLD`: umbral mínimo de cardinalidad para considerar que una clase tiene suficientes ejemplos en la métrica `Div-ML-3`. Por ahora se mantiene fijo en el backend.


