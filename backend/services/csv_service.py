from fastapi import HTTPException
import csv
import io

import pandas as pd

def procesar_csv(contenido: bytes, nombre: str):
    try:
        texto = contenido.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Archivo CSV inválido o codificado incorrectamente")

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

