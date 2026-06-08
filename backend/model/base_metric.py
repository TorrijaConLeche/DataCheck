from abc import ABC, abstractmethod

import pandas as pd

from .metric_result import MetricResult
from .metric_source import MetricSource


class BaseMetric(ABC):
    id: str
    name: str
    description: str
    source: MetricSource

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> MetricResult:
        raise NotImplementedError

