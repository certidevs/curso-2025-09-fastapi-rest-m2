from fastapi import FastAPI

app = FastAPI()

@app.get("/animales")
def obtener_animales():
    return {
        "animales": ["Tigre", "León", "Okapi", "Binturong"]
    }

@app.get("/zoologico")
def obtener_zoologico():
    return {
        "nombre": "Zoológico Grajilla",
        "total_animales": 25,
        "abierto": True,
        "horario": "9:00 - 19:00"
    }

@app.get("/estadisticas")
def obtener_estadisticas():
    return {
        "informacion_general": {
            "nombre": "Zoológico Grajilla",
            "ubicacion": "Plaza Parus Major"
        },
        "datos_animales": {
            "total_especies": 4,
            "animales_populares": ["Tigre", "Binturong"]
        },
        "estado_operacional": {
            "abierto": True,
            "empleados_presentes": 5000
        }
    }