from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int

class ProductoPatch(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None

productos_db = [
    {"id": 1, "nombre": "Leche", "precio": 1.99, "stock": 50},
    {"id": 2, "nombre": "Queso", "precio": 5.99, "stock": 25}
]

@app.put("/productos/{producto_id}")
def actualizar_producto_completo(producto_id: int, producto: Producto):
    for i, producto in enumerate(productos_db):
        if producto["id"] == producto_id:
            productos_db[i] = {
                "id": producto_id,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "stock": producto.stock
            }
            return productos_db[i]
    
    raise HTTPException(status_code=404, detail="404 - Producto no encontrado")

@app.patch("/productos/{producto_id}")
def actualizar_producto_parcial(producto_id: int, producto_patch: ProductoPatch):
    producto_index = None
    for i, producto in enumerate(productos_db):
        if producto["id"] == producto_id:
            producto_index = i
    
    if producto_index is None:
        raise HTTPException(status_code=404, detail="404 - Producto no encontrado")
    
    datos_actualizacion = producto_patch.model_dump(exclude_unset=True)
    
    for campo, valor in datos_actualizacion.items():
        productos_db[producto_index][campo] = valor
    
    return productos_db[producto_index]