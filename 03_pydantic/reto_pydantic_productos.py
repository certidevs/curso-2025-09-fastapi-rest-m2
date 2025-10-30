from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# modelo
class Producto(BaseModel):
    nombre: str
    precio: float
    categoria: str
    disponible: bool = True
    descripcion: Optional[str]

# ruta post
@app.post("/productos")
def registrar_producto(producto: Producto):
    return {
        "mensaje": f"Producto {producto.nombre} registrado con éxito con precio {producto.precio}€"
    }