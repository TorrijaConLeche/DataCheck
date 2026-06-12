import csv
import io
import os
import uuid

import pandas as pd
from fastapi import HTTPException

from services.storage import DATASETS_DIR, dataset_path


def _leer_dataframe(contenido: bytes) -> pd.DataFrame:
    try:
        texto = contenido.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Archivo CSV inválido o codificado incorrectamente",
        )

    texto = texto.strip()
    if not texto:
        raise HTTPException(status_code=400, detail="Archivo CSV inválido")

    sample = "\n".join(texto.splitlines()[:10])
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        raise HTTPException(status_code=400, detail="Archivo CSV inválido")

    try:
        df = pd.read_csv(io.StringIO(texto), sep=dialect.delimiter)
    except Exception:
        raise HTTPException(status_code=400, detail="Archivo CSV inválido")

    if df.empty:
        raise HTTPException(status_code=400, detail="Archivo CSV inválido")

    return df


def procesar_y_guardar_csv(contenido: bytes) -> tuple[str, pd.DataFrame]:
    df = _leer_dataframe(contenido)

    os.makedirs(DATASETS_DIR, exist_ok=True)

    dataset_id = str(uuid.uuid4())
    ruta = dataset_path(dataset_id)

    with open(ruta, "wb") as f:
        f.write(contenido)

    return dataset_id, df


def cargar_dataset(dataset_id: str) -> pd.DataFrame:
    ruta = dataset_path(dataset_id)
    if not os.path.isfile(ruta):
        raise HTTPException(
            status_code=404,
            detail=f"No existe el dataset '{dataset_id}'",
        )
    return pd.read_csv(ruta)
