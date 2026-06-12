import { MetricSource } from './metric-source';

export interface MetricResult {
  id: string;
  name: string;
  description: string;
  source: MetricSource;
  raw_value: unknown;
  normalized_value: number | null;
  interpretation: string | null;
}
