from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int

@app.post("/libros")
async def crear_libro(libro: Libro):
    return {
        "mensaje": f"Se ha creado el libro {libro.titulo} con éxito",
        "datos": {
            "titulo": libro.titulo,
            "autor": libro.autor,
            "paginas": libro.paginas
        }
    }