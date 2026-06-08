import pandas as pd

from model.base_metric import BaseMetric
from model.metric_result import MetricResult
from model.metric_source import MetricSource

# Pendiente: el usuario debe definir el target
TARGET_COLUMN = "Survived"


class DivML2Metric(BaseMetric):
    id = "Div-ML-2"
    name = "Relative label abundance"
    description = "Proporción de elementos de datos que tienen una etiqueta en el conjunto de datos."
    source = MetricSource.ISO

    def compute(self, df: pd.DataFrame) -> MetricResult:
        total_rows = len(df)
        labels = df[TARGET_COLUMN]
        labeled_rows = int(labels.notna().sum())

        ratio = 0.0 if total_rows == 0 else labeled_rows / total_rows

        return MetricResult(
            id=self.id,
            name=self.name,
            description=self.description,
            source=self.source,
            raw_value={
                "label_column": TARGET_COLUMN,
                "labeled_rows": labeled_rows,
                "total_rows": total_rows,
                "ratio": ratio,
            },
            normalized_value=ratio,
            interpretation=self._interpret(ratio),
        )

    def _interpret(self, ratio: float) -> str:
        if ratio == 1:
            return "Todas las filas tienen etiqueta."
        if ratio >= 0.95:
            return "Casi todas las filas tienen etiqueta."
        if ratio >= 0.8:
            return "El dataset presenta algunas filas sin etiquetar."
        return "El dataset presenta muchas filas sin etiquetar."
