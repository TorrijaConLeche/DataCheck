import pandas as pd

from model.base_metric import BaseMetric
from model.metric_result import MetricResult
from model.metric_source import MetricSource


class NullPercentageMetric(BaseMetric):
    id = "null_percentage"
    name = "Porcentaje de nulos"
    description = "Porcentaje de valores nulos presentes en el dataset."
    source = MetricSource.BASIC

    def compute(self, df: pd.DataFrame) -> MetricResult:
        total_cells = df.shape[0] * df.shape[1]
        null_count = int(df.isna().sum().sum())

        if total_cells == 0:
            percentage = 0.0
        else:
            percentage = null_count / total_cells

        return MetricResult(
            id=self.id,
            name=self.name,
            description=self.description,
            source=self.source,
            raw_value={
                "null_values": null_count,
                "total_cells": total_cells,
                "percentage": percentage * 100,
            },
            normalized_value=percentage,
            interpretation=self._interpret(percentage),
        )

    def _interpret(self, percentage: float) -> str:
        if percentage == 0:
            return "El dataset no contiene valores nulos."
        if percentage < 0.05:
            return "El dataset contiene un porcentaje bajo de valores nulos."
        if percentage < 0.20:
            return "El dataset contiene un porcentaje moderado de valores nulos."
        return "El dataset contiene un porcentaje alto de valores nulos."

