from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/preferencias")
def obtener_preferencias(
    accept_language: str = Header(default="es-ES"),
    accept_enconding: str = Header(default="gzip")
):
    return {
        "idioma_prefereido": accept_language,
        "codificacion_aceptada": accept_enconding
    }