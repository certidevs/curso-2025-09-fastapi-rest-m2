from fastapi import FastAPI, HTTPException

app = FastAPI()

libros = [
    {"id": 1, "titulo": "El Quijote", "autor": "Cervantes"},
    {"id": 2, "titulo": "Cien años de soledad", "autor": "García Márquez"}
]

@app.get("/libros/{libro_id}")
def obtener_libro(libro_id: int):
    for libro in libros:
        if libro["id"] == libro_id:
            return libro
    
    raise HTTPException(status_code=404, detail="404 - Libro no encontrado")