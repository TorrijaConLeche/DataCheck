from typing import Literal

from pydantic import BaseModel, Field


class ColumnInfo(BaseModel):
    name: str
    dtype: str
    unique_values: list[str] | None = None


class UploadResponse(BaseModel):
    dataset_id: str
    filename: str
    rows: int
    columns: int
    columns_info: list[ColumnInfo]


class FeatureConstraints(BaseModel):
    min: float | None = None
    max: float | None = None
    allowed_values: list[str | int | float] | None = None
    regex: str | None = None
    not_null: bool = False


class RulesRequest(BaseModel):
    target_column: str
    constraints: dict[str, FeatureConstraints] = Field(default_factory=dict)


class RulesResponse(BaseModel):
    status: Literal["configured", "error"]
    errors: list[str] | None = None
