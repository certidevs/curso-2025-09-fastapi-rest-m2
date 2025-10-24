from fastapi import FastAPI

# Crear la instancia de la aplicación
app = FastAPI()

# Escribe aquí tu código para los endpoints GET
@app.get("/libros")
def obtener_libros():
    return {"libros": ["The Pillars of the Earth", "Nacidos de la Bruma", "La Celestina"]}

@app.get("/biblioteca")
def obtener_biblioteca():
    return {
        "nombre": "Biblioteca Grajilla",
        "total_libros": 3,
        "abierta": True
    }