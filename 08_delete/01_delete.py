from fastapi import FastAPI, HTTPException

app = FastAPI()

usuarios = [
    {"id": 1, "nombre": "Grajilla", "email": "grajilla@aves.es"},
    {"id": 2, "nombre": "Lavandera", "email": "lavandera@aves.es"},
    {"id": 3, "nombre": "Carbonero", "email": "carbonero@aves.es"},
]

@app.get("/usuarios")
def obtener_usuarios():
    return usuarios

# DELETE básico
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    for i, usuario in enumerate(usuarios):
        if usuario["id"] == usuario_id:
            usuario_eliminado = usuarios.pop(i)
            return {"mensaje": f"Se ha eliminado el usuario {usuario_eliminado["nombre"]} correctamente"}
    raise HTTPException(status_code=404, detail="404 - Usuario no encontrado")


# DELETE con validación
tareas = [
    {"id": 1, "titulo": "Observar las aves de Jaén", "completada": True},
    {"id": 2, "titulo": "Dormir 8 horas diarias", "completada": False},
    {"id": 3, "titulo": "Comer sano", "completada": False}
]

@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    for i, tarea in enumerate(tareas):
        if tarea["id"] == tarea_id:
            if not tarea["completada"]:
                raise HTTPException(status_code=400, detail="400 - No se pueden eliminar tareas que no están completadas")
            tarea_eliminada = tareas.pop(i)
            return {"mensaje": f"Se ha eliminado la tarea {tarea_eliminada["titulo"]} con éxito"}
    raise HTTPException(status_code=404, detail="404 - Tarea no encontrada")