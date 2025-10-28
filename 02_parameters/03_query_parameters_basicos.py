"""
Los query parameters (parámetros de consulta) son datos clave-valor que se utilizan para filtar, ordenar y paginar.

Se añaden después de la ruta con un signo de interrogación de cierre ?.
Se separan con un ampersand &.
"""

from fastapi import FastAPI

app = FastAPI()

# paginación simple
@app.get("/users")
def get_users(limit: int = 10):
    return {
        "users": [f"Usuario {i}" for i in range(1, limit+1)],
        "total": limit,
        "limit": limit
    }

# paginación completa
@app.get("/products")
def get_products(limit: int=10, skip: int = 0):
    # crear lista productos con salto y límite
    products = [f"Producto {i}" for i in range(skip + 1, skip + limit + 1)]
    
    return {
        "products": products,
        "limit": limit,
        "skip": skip,
        "total_shown": len(products)
    }

# filtrado
@app.get("/items")
def get_items(category: str = "all"):
    if category == "all":
        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Todos los items"]
    else:
        items = [f"Item {i} de {category}" for i in range(1, 4)]
    
    return {
        "item": items,
        "category": category,
        "total": len(items)
    }