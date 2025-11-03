from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Usuario(BaseModel):
    nombre: str
    email: str
    edad: int

@app.post("/usuarios")
async def crear_usuario(usuario: Usuario):
    return {
        "mensaje": f"Usuario {usuario.nombre} creado con éxito",
        "datos": {
            "nombre": usuario.nombre,
            "email": usuario.email,
            "edad": usuario.edad
        }
    }

class Contacto(BaseModel):
    nombre: str
    telefono: str
    email: str

@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    respuesta = f"Gracias {contacto.nombre}, hemos enviado la confirmación al email {contacto.email}"
    return {"respuesta": respuesta}