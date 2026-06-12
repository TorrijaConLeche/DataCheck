import { MetricResult } from './metric-result';
import { DatasetStatus } from './dataset-status';

export interface DatasetAnalysis {
  dataset_id: string;
  status: DatasetStatus;
  metrics: MetricResult[];
  interpretation: string;
}
