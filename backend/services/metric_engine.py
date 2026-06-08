import pandas as pd

from model.base_metric import BaseMetric
from model.metric_result import MetricResult
from model.registry import METRIC_REGISTRY, MetricRegistry


class MetricEngine:
    def __init__(self, registry: MetricRegistry = METRIC_REGISTRY) -> None:
        self.registry = registry

    def run(self, df: pd.DataFrame) -> list[MetricResult]:
        results: list[MetricResult] = []

        for metric in self.registry.list():
            results.append(self._compute_metric(metric, df))

        return results

    def _compute_metric(self, metric: BaseMetric, df: pd.DataFrame) -> MetricResult:
        try:
            return metric.compute(df)
        except Exception as exc:
            return MetricResult(
                id=metric.id,
                name=metric.name,
                description=metric.description,
                source=metric.source,
                raw_value=None,
                normalized_value=None,
                interpretation=f"No se pudo calcular la métrica: {exc}",
            )
