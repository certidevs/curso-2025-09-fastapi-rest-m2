"""
El método GET sirve para OBTENER (traer) datos.
"""

# importams FastAPI para crear nuestra aplicación
from fastapi import FastAPI

# creamos la instancia de nuestra aplicación FastAPI
# esta instancia debe crearse una sola vez al inicio del archivo
app = FastAPI()

# creamos la ruta raíz ("/")
# el decorador @app.get("/") le dice a FastAPI que cuando alguien visite
# la ruta raíz ("/"), tiene que ejecutar la función leer_raíz
@app.get("/")
def leer_raiz():
    # devolvemos un diccionario y FastAPI lo convierte en JSON
    return {"mensaje": "¡Hola desde la ruta raíz!"}

@app.get("/inicio")
def obtener_informacion():
    return {"autor": "La Grajilla", "descripcion": "API molona de ejemplo para explicar en clase", "fecha": "2025-10-24"}