from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/hora-actual")
def obtener_hora():
    ahora = datetime.now()
    return {
        "fecha": ahora.strftime("%Y-%m-%d"),
        "hora": ahora.strftime("%H:%M:%S"),
        "dia_semana": ahora.strftime("%A"),
        "mes": ahora.strftime("%B"),
        "timestamp": ahora.timestamp()
    }