from fastapi import FastAPI, HTTPException

app = FastAPI()

libros = [
    {"id": 1, "titulo": "El Quijote", "autor": "Cervantes"},
    {"id": 2, "titulo": "Cien años de soledad", "autor": "García Márquez"},
    {"id": 3, "titulo": "1984", "autor": "Orwell"}
]

@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int):
    for i, libro in enumerate(libros):
        if libro["id"] == libro_id:
            libros.pop(i)
            return {"mensaje": "Libro eliminado correctamente"}
    
    raise HTTPException(status_code=404, detail="404 - Libro no encontrado")