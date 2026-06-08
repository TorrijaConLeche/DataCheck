
### Activar entorno
source .venv/bin/activate

### Instalar ependencias
uv pip install -r requirements.txt

### Ver dependencias instaladas
uv pip list

### Ejecutar fastAPI
uvicorn main:app --reload

