from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# modelo básico
class Usuario(BaseModel):
    nombre: str
    edad: int
    activo: bool

# modelo con campos opcionales y valores por defecto
class Producto(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None
    disponible: bool = True