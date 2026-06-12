export interface ColumnInfo {
  name: string;
  dtype: string;
  unique_values: string[] | null;
}

export interface DatasetInfo {
  dataset_id: string;
  filename: string;
  rows: number;
  columns: number;
  columns_info: ColumnInfo[];
}
