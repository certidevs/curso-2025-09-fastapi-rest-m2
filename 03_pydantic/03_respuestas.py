from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# modelo
class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    disponible: bool = True

# base de datos en memoria
productos_db: List[Producto] = [
    Producto(id=1, nombre="Leche", precio=1.99, disponible=True),
    Producto(id=2, nombre="Queso", precio=5.99, disponible=True),
    Producto(id=3, nombre="Yogur", precio=3.99, disponible=False)
]

# método GET que devuelve un lista de objetos
@app.get("/productos", response_model=List[Producto])
def listar_productos():
    return productos_db

# método GET que devuelve un objeto pydantic
@app.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int):
    for p in productos_db:
        if p.id == producto_id:
            # devolver el modelo pydantic directamente
            return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# método post
@app.post("/productos", response_model=Producto, status_code=201)
def crear_producto(producto: Producto):
    productos_db.append(producto)
    return producto