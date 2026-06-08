from fastapi import APIRouter, UploadFile, File
import pandas as pd
from services.csv_service import procesar_csv
from services.metric_engine import MetricEngine

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.post("/subir")
async def subir_dataset(archivo: UploadFile = File(...)):

    contenido = await archivo.read()

    df = procesar_csv(contenido, archivo.filename)


    # Calcular una metrica basica
    engine = MetricEngine()

    resultados = engine.run(df)

    return resultados

