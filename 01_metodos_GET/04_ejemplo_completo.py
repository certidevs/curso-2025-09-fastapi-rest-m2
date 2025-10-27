from fastapi import FastAPI

app = FastAPI()

@app.get("/perfil-completo")
def obtener_perfil():
    return {
        "usuario": {
            "nombre": "La Grajilla",
            "apellido": "Occidental",
            "edad": 27,
            "email": "grajilla@occidental.com",
            "telefono": "123 45 67 89"
        },
        "configuracion": {
            "tema": "oscuro",
            "notificaciones": True,
            "idioma": "español",
            "zona_horaria": "Madrid"
        },
        "estadisticas": {
            "visitas": 15,
            "ultimo_acceso": "2025-10-27",
            "tiempo_sesion": 75,
            "actividad_semanal": [5, 4, 4, 8, 9, 4, 4]
        }
    }