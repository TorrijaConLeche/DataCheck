import math

import pandas as pd

from model.base_metric import BaseMetric
from model.metric_result import MetricResult
from model.metric_source import MetricSource


TARGET_COLUMN = "Survived"


class BalML8Metric(BaseMetric):
    id = "Bal-ML-8"
    name = "Label distribution balance"
    description = "Divergencia entre la distribución real de etiquetas y una distribución uniforme."
    source = MetricSource.ISO

    def compute(self, df: pd.DataFrame) -> MetricResult:
        if TARGET_COLUMN not in df.columns:
            raise KeyError(f"No existe la columna objetivo '{TARGET_COLUMN}' en el dataset")

        labels = df[TARGET_COLUMN].dropna()
        total = int(labels.shape[0])

        if total == 0:
            real_dist = pd.Series(dtype="float64")
            ideal_dist = []
            js_distance = 1.0
        else:
            real_dist = labels.value_counts(normalize=True).sort_index()
            num_classes = int(real_dist.shape[0])
            ideal_dist = [1 / num_classes] * num_classes
            js_distance = self._jensen_shannon_distance(real_dist.values, ideal_dist)

        normalized_value = 1.0 - js_distance

        return MetricResult(
            id=self.id,
            name=self.name,
            description=self.description,
            source=self.source,
            raw_value={
                "label_column": TARGET_COLUMN,
                "real_distribution": real_dist.to_dict(),
                "ideal_distribution": ideal_dist,
                "jensen_shannon_distance": js_distance,
            },
            normalized_value=normalized_value,
            interpretation=self._interpret(js_distance),
        )


    # Pendiente: utilizar scipy para calcular la distancia de Jensen-Shannon
    def _jensen_shannon_distance(self, p: list[float] | pd.Series | tuple, q: list[float]) -> float:
        p_values = [float(value) for value in p]
        q_values = [float(value) for value in q]
        m_values = [(a + b) / 2 for a, b in zip(p_values, q_values)]
        return math.sqrt(0.5 * (self._kl_divergence(p_values, m_values) + self._kl_divergence(q_values, m_values)))

    def _kl_divergence(self, p: list[float], q: list[float]) -> float:
        epsilon = 1e-12
        total = 0.0
        for pi, qi in zip(p, q):
            if pi <= 0:
                continue
            total += pi * math.log((pi + epsilon) / (qi + epsilon), 2)
        return total

    def _interpret(self, js_distance: float) -> str:
        if js_distance == 0:
            return "La distribución de etiquetas es perfectamente equilibrada."
        if js_distance < 0.2:
            return "La distribución de etiquetas presenta un balance alto."
        if js_distance < 0.4:
            return "La distribución de etiquetas presenta un balance moderado."
        return "La distribución de etiquetas presenta un desbalance alto."

