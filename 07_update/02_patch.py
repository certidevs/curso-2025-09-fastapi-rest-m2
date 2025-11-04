from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

usuarios_db = [
    {"id": 1, "nombre": "Grajilla", "email": "grajilla@aves.com", "edad": 27},
    {"id": 2, "nombre": "Rabilargo", "email": "rabilargo@aves.com", "edad": 25}
]

class Usuario(BaseModel):
    nombre: str
    email: str
    edad: int
    
class UsuarioPatch(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    edad: Optional[int] = None

@app.get("/usuarios")
def obtener_usuarios():
    return usuarios_db

@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    for user in usuarios_db:
        if user["id"] == usuario_id:
            return user
    raise HTTPException(status_code=404, detail="404 - Usuario no encontrado")

# PATCH
@app.patch("/usuarios/{usuario_id}")
def actualizar_usuario_parcial(usuario_id: int, usuario_patch: UsuarioPatch):
    usuario_index = None
    for i, user in enumerate(usuarios_db):
        if user["id"] == usuario_id:
            usuario_index = i
    
    if usuario_index is None:
        raise HTTPException(status_code=404, detail="404 - Usuario no encontrado")
    
    datos_actualizacion = usuario_patch.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        usuarios_db[usuario_index][campo] = valor
        
    return {
        "mensaje": "Usuario actualizado de forma parcial",
        "usuario": usuarios_db[usuario_index]
    }