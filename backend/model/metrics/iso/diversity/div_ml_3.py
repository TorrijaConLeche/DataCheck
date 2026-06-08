import pandas as pd

from model.base_metric import BaseMetric
from model.metric_result import MetricResult
from model.metric_source import MetricSource

# Pendiente: el usuario debe definir estas metricas
TARGET_COLUMN = "Survived"
DIV_THRESHOLD = 30

class DivML3Metric(BaseMetric):
    id = "Div-ML-3"
    name = "Category size diversity"
    description = "Proporción de categorías por debajo de un umbral de cardinalidad mínima."
    source = MetricSource.ISO


    def compute(self, df: pd.DataFrame) -> MetricResult:
        labels = df[TARGET_COLUMN]
        counts = labels.dropna().value_counts()
        num_classes = int(counts.shape[0])
        classes_below_threshold = int((counts < DIV_THRESHOLD).sum())

        ratio = 0.0 if num_classes == 0 else classes_below_threshold / num_classes
        normalized_value = 1.0 - ratio

        return MetricResult(
            id=self.id,
            name=self.name,
            description=self.description,
            source=self.source,
            raw_value={
                "label_column": TARGET_COLUMN,
                "classes_below_threshold": classes_below_threshold,
                "total_classes": num_classes,
                "threshold": DIV_THRESHOLD,
                "ratio": ratio,
            },
            normalized_value=normalized_value,
            interpretation=self._interpret(ratio),
        )

    def _interpret(self, ratio: float) -> str:
        if ratio == 0:
            return "Todas las clases cumplen el umbral de cardinalidad."
        if ratio < 0.33:
            return "Pocas clases están por debajo del umbral."
        if ratio < 0.66:
            return "Varias clases están por debajo del umbral."
        return "La mayoría de las clases están por debajo del umbral."
