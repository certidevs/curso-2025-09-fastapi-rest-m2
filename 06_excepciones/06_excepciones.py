from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

usuarios_db = [
    {"id": 1, "nombre": "Grajilla", "email": "grajilla@aves.com"},
    {"id": 2, "nombre": "Rabilargo", "email": "rabilargo@aves.com"}
]

@app.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: int):
    for usuario in usuarios_db:
        if usuario["id"] == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail="404 - Usuario no encontrado")

class Usuario(BaseModel):
    nombre: str
    email: str
    edad: int

usuarios_memoria: list[dict] = []

@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    if usuario.edad < 18:
        raise HTTPException(status_code=400, detail="400 - La edad debe ser mayor o igual a 18")
    
    for u in usuarios_memoria:
        if u["email"] == usuario.email:
            raise HTTPException(status_code=400, detail="Este correo ya está en uso")
    
    nuevo_usuario = {
        "id": len(usuarios_memoria) + 1,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "edad": usuario.edad
    }
    
    usuarios_memoria.append(nuevo_usuario)
    return nuevo_usuario