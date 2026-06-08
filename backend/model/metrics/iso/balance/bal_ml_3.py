import math

import pandas as pd

from model.base_metric import BaseMetric
from model.metric_result import MetricResult
from model.metric_source import MetricSource


TARGET_COLUMN = "Survived"


class BalML3Metric(BaseMetric):
    id = "Bal-ML-3"
    name = "Balance between categories"
    description = "Recíproco del ratio máximo de diferencia del tamaño de categoría frente al tamaño medio."
    source = MetricSource.ISO

    def compute(self, df: pd.DataFrame) -> MetricResult:
        if TARGET_COLUMN not in df.columns:
            raise KeyError(f"No existe la columna objetivo '{TARGET_COLUMN}' en el dataset")

        labels = df[TARGET_COLUMN].dropna()
        counts = labels.value_counts().sort_index()
        category_sizes = counts.tolist()

        if not category_sizes:
            average_category_size = 0.0
            max_difference = 0.0
            raw_metric_value = 0.0
        else:
            average_category_size = float(sum(category_sizes) / len(category_sizes))
            max_difference = float(max(abs(size - average_category_size) for size in category_sizes))
            raw_metric_value = math.inf if max_difference == 0 else average_category_size / max_difference

        normalized_value = self._normalize(raw_metric_value)

        return MetricResult(
            id=self.id,
            name=self.name,
            description=self.description,
            source=self.source,
            raw_value={
                "label_column": TARGET_COLUMN,
                "category_counts": counts.to_dict(),
                "average_category_size": average_category_size,
                "max_difference": max_difference,
                "bal_ml_3": raw_metric_value,
            },
            normalized_value=normalized_value,
            interpretation=self._interpret(normalized_value),
        )

    def _normalize(self, raw_metric_value: float) -> float:
        if math.isinf(raw_metric_value):
            return 1.0
        if raw_metric_value <= 0:
            return 0.0
        return raw_metric_value / (raw_metric_value + 1)

    def _interpret(self, normalized_value: float) -> str:
        if normalized_value == 1:
            return "Las categorías están perfectamente balanceadas."
        if normalized_value >= 0.8:
            return "Las categorías presentan un balance alto."
        if normalized_value >= 0.5:
            return "Las categorías presentan un balance moderado."
        return "Las categorías presentan un desbalance alto."

