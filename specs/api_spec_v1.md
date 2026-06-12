# Especificacion endpoints

Este documento define los endpoints principales del backend del sistema tfg-metricas, orientado al análisis de datasets en formato CSV.

El diseño sigue una arquitectura REST con separación clara entre fases: subida, configuración de reglas y análisis.

---

## 1. Subida de dataset

### POST /datasets/subir

### Descripción
Endpoint encargado de recibir un archivo CSV, almacenarlo en `storage/datasets/{dataset_id}.csv` y devolver información preliminar del dataset sin realizar análisis completo.

### Request
- Tipo: multipart/form-data
- Parámetro:
  - archivo: archivo CSV

### Response 200 OK
```json
{
  "dataset_id": "uuid-aleatorio",
  "filename": "data.csv",
  "rows": 1000,
  "columns": 12,
  "columns_info": [
    {"name": "Survived", "dtype": "int64"},
    {"name": "Age", "dtype": "float64"},
    {"name": "Sex", "dtype": "object"}
  ]
}
```

### Response 400 Bad Request
```json
{
  "valid": false,
  "message": "Archivo no válido o corrupto"
}
```

---

## 2. Configuración de reglas

### POST /datasets/{dataset_id}/rules

### Descripción
El usuario define la columna objetivo (target) y las restricciones de calidad (constraints) para las features del dataset. El backend valida que las columnas existan y que los tipos sean coherentes, y guarda la configuración en `storage/datasets/{dataset_id}-rules.json`.

### Request
```json
{
  "target_column": "Survived",
  "constraints": {
    "Age": {"min": 0, "max": 120, "not_null": true},
    "Fare": {"min": 0},
    "Sex": {"allowed_values": ["male", "female"]}
  }
}
```

### Validaciones
- `target_column` debe existir en el dataset.
- Cada columna en `constraints` debe existir en el dataset.
- Los tipos de constraint deben ser coherentes con el dtype de la columna (ej. no aplicar `min`/`max` a una columna de texto).

### Response 200 OK
```json
{
  "status": "configured"
}
```

### Response 400 Bad Request
```json
{
  "status": "error",
  "errors": ["La columna 'X' no existe en el dataset"]
}
```

---

## 3. Ejecución de análisis

### POST /datasets/{dataset_id}/analyze

### Descripción
Ejecuta el análisis completo del dataset usando las reglas previamente configuradas. Las métricas (ISO, básicas, papers) reciben el contexto con `target_column` y `constraints` para aquellos cálculos que lo necesiten.

### Response 200 OK
```json
{
  "dataset_id": "uuid",
  "status": "completed",
  "metrics": [
    {
      "id": "Eft-ML-1",
      "name": "Feature Effectiveness",
      "description": "Proporción de muestras que cumplen las restricciones definidas para las features",
      "source": "ISO",
      "raw_value": 0.85,
      "normalized_value": 0.85,
      "interpretation": "El 85% de las muestras cumplen con las restricciones definidas para las features."
    }
  ]
}
```

### Response 400 Bad Request
```json
{
  "status": "error",
  "message": "No hay reglas configuradas para este dataset"
}
```

---

## Flujo general del sistema

1. El usuario sube un CSV mediante `POST /datasets/subir`.
2. El sistema almacena el CSV, asigna un `dataset_id` y devuelve información de columnas.
3. El usuario configura `target_column` y `constraints` mediante `POST /datasets/{id}/rules`.
4. El sistema valida y guarda las reglas en `{dataset_id}-rules.json`.
5. El usuario solicita el análisis con `POST /datasets/{id}/analyze`.
6. El sistema ejecuta las métricas con el contexto de las reglas.
7. Los resultados se devuelven al frontend.

---

## Notas de diseño

- Separación clara entre subida, configuración y análisis.
- Uso de `dataset_id` como identificador único.
- Las reglas se persisten en disco para permitir re-análisis.
- Arquitectura extensible para futuras métricas.
- Flujo orientado a experiencia de usuario.
