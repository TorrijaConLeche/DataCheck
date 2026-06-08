from fastapi import FastAPI
from fastapi.testclient import TestClient
from api.datasets import router
import io

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_subir_csv_valido():
    csv_content = "col1,col2\n1,2\n3,4"

    response = client.post(
        "/datasets/subir",
        files={
            "archivo": ("test.csv", csv_content, "text/csv")
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["nombre_archivo"] == "test.csv"
    assert data["filas"] == 2
    assert data["columnas"] == 2
    assert "col1" in data["columnas_nombres"]


def test_subir_archivo_invalido():
    fake_content = b"esto no es un csv ni nada"

    response = client.post(
        "/datasets/subir",
        files={
            "archivo": ("test.txt", fake_content, "text/plain")
        }
    )

    assert response.status_code == 400