export interface ColumnInfo {
  name: string;
  dtype: string;
}

export interface DatasetInfo {
  dataset_id: string;
  filename: string;
  rows: number;
  columns: number;
  columns_info: ColumnInfo[];
}
