import pandas as pd

from model.base_metric import BaseMetric
from model.metric_result import MetricResult
from model.metric_source import MetricSource


# Pendiente: el usuario debe definir el target
TARGET_COLUMN = "Survived"


class DivML1Metric(BaseMetric):
    id = "Div-ML-1"
    name = "Label richness"
    description = "Ratio de etiquetas diferentes en el dataset"
    source = MetricSource.ISO

    def compute(self, df: pd.DataFrame) -> MetricResult:
        total_rows = len(df)
        labels = df[TARGET_COLUMN]
        distinct_labels = int(labels.dropna().nunique())

        ratio = 0.0 if total_rows == 0 else distinct_labels / total_rows

        return MetricResult(
            id=self.id,
            name=self.name,
            description=self.description,
            source=self.source,
            raw_value={
                "label_column": TARGET_COLUMN,
                "distinct_labels": distinct_labels,
                "total_rows": total_rows,
                "ratio": ratio,
            },
            normalized_value=ratio,
            interpretation=self._interpret(ratio),
        )

    def _interpret(self, ratio: float) -> str:
        if ratio == 0:
            return "No se han encontrado etiquetas válidas en el dataset."
        if ratio < 0.1:
            return "La riqueza de etiquetas es baja."
        if ratio < 0.3:
            return "La riqueza de etiquetas es moderada."
        return "La riqueza de etiquetas es alta."
