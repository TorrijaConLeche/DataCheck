from __future__ import annotations

from collections.abc import Iterable

from .base_metric import BaseMetric
from .metrics.basic import NullPercentageMetric
from .metrics.iso.balance import BalML3Metric, BalML8Metric
from .metrics.iso.diversity import DivML1Metric, DivML2Metric, DivML3Metric


class MetricRegistry:
    def __init__(self) -> None:
        self._metrics: dict[str, BaseMetric] = {
            # REGISTRAMOS METRICAS AQUI
            "null_percentage": NullPercentageMetric(),
            "Div-ML-1": DivML1Metric(),
            "Div-ML-2": DivML2Metric(),
            "Div-ML-3": DivML3Metric(),
            "Bal-ML-3": BalML3Metric(),
            "Bal-ML-8": BalML8Metric(),

        }

    def register(self, metric: BaseMetric) -> BaseMetric:
        metric_id = metric.id.strip()
        if not metric_id:
            raise ValueError("El metric.id no puede estar vacío")
        if metric_id in self._metrics:
            raise ValueError(f"La métrica '{metric_id}' ya está registrada")

        self._metrics[metric_id] = metric
        return metric

    def register_many(self, metrics: Iterable[BaseMetric]) -> None:
        for metric in metrics:
            self.register(metric)

    def get(self, metric_id: str) -> BaseMetric | None:
        return self._metrics.get(metric_id)

    def list(self) -> list[BaseMetric]:
        return list(self._metrics.values())

    def items(self) -> list[tuple[str, BaseMetric]]:
        return list(self._metrics.items())

    def clear(self) -> None:
        self._metrics.clear()

    def as_dict(self) -> dict[str, BaseMetric]:
        return dict(self._metrics)


METRIC_REGISTRY = MetricRegistry()


def register_metric(metric: BaseMetric) -> BaseMetric:
    return METRIC_REGISTRY.register(metric)


def get_metric(metric_id: str) -> BaseMetric | None:
    return METRIC_REGISTRY.get(metric_id)


def list_metrics() -> list[BaseMetric]:
    return METRIC_REGISTRY.list()
