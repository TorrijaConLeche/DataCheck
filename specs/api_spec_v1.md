# Especificacion endpoints

Este documento define los endpoints principales del backend del sistema tfg-metricas, orientado al análisis de datasets en formato CSV.

El diseño sigue una arquitectura REST con separación clara entre fases: subida, validación, confirmación, análisis y consulta de resultados.

---

## 1. Subida de dataset

### POST /datasets/subir

### Descripción
Endpoint encargado de recibir un archivo CSV, validar su formato básico y devolver información preliminar del dataset sin realizar análisis completo.

### Request
- Tipo: multipart/form-data
- Parámetro:
  - archivo: archivo CSV

### Response 200 OK
{
  "nombre_archivo": "data.csv",
  "filas": 1000,
  "columnas": 12,
  "columnas_nombres": ["A", "B", "C"]
}

### Response 400 Bad Request
{
  "valid": false,
  "message": "Archivo no válido o corrupto"
}

---

## 2. Confirmación de análisis

### POST /datasets/{dataset_id}/confirm

### Descripción
Confirma que el usuario desea proceder con el análisis del dataset previamente subido y validado.

Estado: previsto para una fase posterior.

### Request
{
  "proceed": true
}

### Response 200 OK
{
  "dataset_id": "uuid",
  "status": "confirmed"
}

---

## 3. Ejecución de análisis

### POST /datasets/{dataset_id}/analyze

### Descripción
Ejecuta el análisis completo del dataset, incluyendo el cálculo de métricas y generación de interpretación de resultados.

Estado: previsto para una fase posterior. Actualmente el cálculo de métricas ya está disponible a nivel interno mediante `MetricEngine`.

### Response 200 OK
{
  "dataset_id": "uuid",
  "status": "completed",
  "metrics": {
    "rows": 1000,
    "columns": 12,
    "missing_values": 32,
    "duplicate_rows": 5
  },
  "interpretation": "El dataset presenta una calidad moderada con presencia de valores nulos en algunas columnas."
}

---

## 4. Obtención de resultados

### GET /datasets/{dataset_id}/results

### Descripción
Devuelve los resultados del análisis previamente ejecutado.

Estado: previsto para una fase posterior.

### Response 200 OK
{
  "dataset_id": "uuid",
  "status": "completed",
  "metrics": {
    "rows": 1000,
    "columns": 12,
    "missing_values": 32
  },
  "interpretation": "Texto explicativo del análisis realizado."
}

---

## 5. Estado del dataset

### GET /datasets/{dataset_id}/status

### Descripción
Devuelve el estado actual del dataset dentro del flujo de procesamiento.

Estado: previsto para una fase posterior.

### Estados posibles
- uploaded
- valid
- confirmed
- processing
- completed
- error

### Response 200 OK
{
  "dataset_id": "uuid",
  "status": "processing"
}

---

## Flujo general del sistema

1. El usuario sube un dataset mediante /datasets/subir
2. El sistema valida el archivo y devuelve información básica
3. El usuario confirma el análisis con /datasets/{id}/confirm
4. El sistema ejecuta el análisis con /datasets/{id}/analyze
5. El frontend puede consultar el estado con /datasets/{id}/status
6. Los resultados finales se obtienen desde /datasets/{id}/results

---

## Notas de diseño

- Separación clara entre validación y análisis
- Uso de dataset_id como identificador único
- Arquitectura extensible para futuras métricas
- Flujo orientado a experiencia de usuario
