from dataclasses import dataclass
from typing import Any

from .metric_source import MetricSource


@dataclass(slots=True)
class MetricResult:
    id: str
    name: str
    description: str
    source: MetricSource
    raw_value: Any
    normalized_value: float | None = None
    interpretation: str | None = None

