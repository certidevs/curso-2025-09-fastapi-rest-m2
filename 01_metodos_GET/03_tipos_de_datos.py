from fastapi import FastAPI

# creamos la instancia de la aplicación FastAPI
app = FastAPI()

@app.get("/")
def leer_raiz():
    return {"mensaje": "Vamos a ver los tipos de datos"}

@app.get("/tipos-datos")
def mostrar_tipos():
    return {
        "texto": "Hola, grajillas",
        "numero_entero": 23,
        "numero_decimal": 3.14,
        "booleano": True,
        "lista_numeros": [1, 2, 3, 4],
        "lista_textos": ["Carbonero común", "Grajilla occidental", "Lavandera blanca"],
        "listas_booleanos": [True, False, True],
        "listas_mixtas": [7, "texto", True],
        "valor_nulo": None
    }