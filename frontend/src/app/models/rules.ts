export interface FeatureConstraints {
  min: number | null;
  max: number | null;
  allowed_values: (string | number)[] | null;
  regex: string | null;
  not_null: boolean;
}

export interface RulesPayload {
  target_column: string;
  constraints: Record<string, FeatureConstraints>;
}

export interface RulesResponse {
  status: 'configured' | 'error';
  errors: string[] | null;
}
