import json
import os

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile

from model.dataset import (
    ColumnInfo,
    FeatureConstraints,
    RulesRequest,
    RulesResponse,
    UploadResponse,
)
from services.csv_service import cargar_dataset, procesar_y_guardar_csv
from services.storage import rules_path

router = APIRouter(prefix="/datasets", tags=["datasets"])


_DTYPES_NUMERICOS = ("int", "float")


def _es_numerico(dtype: str) -> bool:
    return any(t in dtype.lower() for t in _DTYPES_NUMERICOS)


@router.post("/subir", response_model=UploadResponse)
async def subir_dataset(archivo: UploadFile = File(...)) -> UploadResponse:
    contenido = await archivo.read()

    dataset_id, df = procesar_y_guardar_csv(contenido)

    columns_info = [
        ColumnInfo(name=str(col), dtype=str(dtype))
        for col, dtype in df.dtypes.items()
    ]

    return UploadResponse(
        dataset_id=dataset_id,
        filename=archivo.filename or "dataset.csv",
        rows=int(df.shape[0]),
        columns=int(df.shape[1]),
        columns_info=columns_info,
    )


@router.post("/{dataset_id}/rules", response_model=RulesResponse)
async def configurar_reglas(
    dataset_id: str, payload: RulesRequest
) -> RulesResponse:
    try:
        df = cargar_dataset(dataset_id)
    except HTTPException:
        raise

    errores: list[str] = []

    if payload.target_column not in df.columns:
        errores.append(
            f"La columna objetivo '{payload.target_column}' no existe en el dataset"
        )

    for col, constraints in payload.constraints.items():
        if col not in df.columns:
            errores.append(f"La columna '{col}' no existe en el dataset")
            continue

        if not _es_numerico(str(df[col].dtype)):
            if constraints.min is not None or constraints.max is not None:
                errores.append(
                    f"La columna '{col}' no es numérica: no admite 'min' ni 'max'"
                )

    if errores:
        return RulesResponse(status="error", errors=errores)

    reglas = {
        "target_column": payload.target_column,
        "constraints": {
            col: feat.model_dump(exclude_none=True)
            for col, feat in payload.constraints.items()
        },
    }

    ruta = rules_path(dataset_id)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(reglas, f, indent=2, ensure_ascii=False)

    return RulesResponse(status="configured")
