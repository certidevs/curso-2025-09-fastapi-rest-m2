from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# modelos anidados

class Direccion(BaseModel):
    calle: str
    ciudad: str
    codigo_postal: str

class Cliente(BaseModel):
    nombre: str
    email: str
    direccion: Direccion

@app.post("/clientes")
def crear_cliente(cliente: Cliente):
    nombre_cliente = cliente.nombre
    ciudad_cliente = cliente.direccion.ciudad
    return {
        "cliente": nombre_cliente,
        "ubicacion": ciudad_cliente,
        "datos_completos": cliente.model_dump()
    }

# uso de List
class Biblioteca(BaseModel):
    nombre: str
    libros: List[str]
    categorias: List[str]
    capacidad_maxima: int

@app.post("/bibliotecas")
def crear_biblioteca(biblioteca: Biblioteca):
    return {
        "biblioteca": biblioteca.nombre,
        "libros_disponibles": len(biblioteca.libros),
        "categorias": biblioteca.categorias,
        "capacidad": biblioteca.capacidad_maxima
    }