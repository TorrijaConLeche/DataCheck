# Visión general

## 1. Nombre del proyecto

El proyecto se denomina provisionalmente **tfg-metricas**.

Se trata de un sistema orientado al análisis automatizado de datasets en formato tabular (CSV), proporcionando métricas cuantitativas y una interpretación de los resultados obtenidos.

---

## 2. Descripción general del sistema

El sistema tiene como objetivo principal permitir a un usuario subir un dataset en formato CSV y obtener un análisis estructurado del mismo.

El flujo general del sistema es el siguiente:

1. El usuario carga un fichero CSV a través de la interfaz.
2. El backend procesa el fichero utilizando Python y Pandas.
3. Se calculan diferentes métricas asociadas al dataset.
4. Los resultados se devuelven al usuario de forma estructurada.
5. El frontend muestra los resultados de manera visual y organizada.
6. El sistema proporciona una interpretación textual de los resultados obtenidos.
7. (No incluido en MVP) El usuario puede descargar un pdf informe de los resultados 


El dataset subido seguirá los siguientes estados previstos:
 status = "uploaded" | "valid" | "confirmed" | "processing" | "completed" | "error"

En el estado actual del backend se dispone de un flujo inicial simplificado: subida/procesado de CSV y ejecución de métricas sobre un `DataFrame`.

Esto ayudará a mejorar la UX.

---

## 3. Objetivo del sistema

El objetivo del sistema es proporcionar una herramienta capaz de:

- Automatizar el análisis básico de datasets tabulares.
- Calcular métricas estadísticas y estructurales relevantes.
- Ofrecer una interpretación de los resultados en lenguaje natural.
- Facilitar la comprensión inicial de un dataset sin necesidad de conocimientos avanzados en análisis de datos.

---

## 4. Naturaleza del análisis

El sistema realizará el cálculo de métricas procedentes de diferentes fuentes, incluyendo:

- Métricas definidas en el estandar ISO_IEC_5259-2-2024 relacionados con calidad de datos para ML.
- Métricas propuestas en literatura científica (papers académicos).
- Métricas estadísticas básicas derivadas del análisis del dataset.

Estas métricas en principio son fijas pero podrían evolucionar durante el desarrollo del proyecto, ampliándose o ajustándose según los resultados obtenidos.

---

## 5. Nivel de inteligencia del sistema

El sistema se apoya en un enfoque híbrido compuesto por:

- Cálculo determinista de métricas.
- Generación de una interpretación textual basada en los resultados obtenidos.

El objetivo de esta capa interpretativa es facilitar la comprensión de los resultados al usuario, traduciendo métricas técnicas a explicaciones más accesibles.

---

## 6. Arquitectura general del sistema

El sistema se divide en tres componentes principales:

### Backend
Implementado en FastAPI. Se encarga de:
- Recepción de archivos CSV.
- Procesamiento de datos con Pandas.
- Cálculo de métricas mediante `MetricEngine` y `MetricRegistry`.
- Exposición de endpoints REST.

### Frontend
Implementado en Angular. Se encarga de:
- Interfaz de usuario.
- Subida de datasets.
- Visualización de resultados.
- Presentación de interpretaciones.

### Almacenamiento de datos y resultados

Previsto para fases posteriores:

backend/
├── storage/
│   ├── datasets/
│   └── results/

1. Upload
    Se genera dataset_id
    backend/storage/datasets/{dataset_id}.csv
    
2. Results
    backend/storage/results/{dataset_id}.json


---

## 7. Alcance del sistema

El sistema se centra exclusivamente en el análisis de datasets en formato CSV.

No incluye:
- Entrenamiento de modelos de machine learning.
- Análisis de datos en tiempo real.
- Integración con bases de datos externas (en la versión inicial).
- Generacion de PDF informe con los resultados (en el MVP).
- Creación de cuenta o historial de datasets.
- Procesamiento de multiples datasets simultaneamente.
