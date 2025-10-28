from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

# validación con restricciones
@app.get("/analytics")
def get_analytics(
    # parámetro con validación de rango (0.0 a 10000.0)
    min_price: float = Query(0.0, ge=0.0, le=10000.0),
    # parámetro con validación de rango (1 a 1000)
    max_results: int = Query(100, ge=1, le=1000)
):
    return {
        "filters": {
            "min_price": min_price,
            "max_results": max_results
        },
        "data": f"Resultados filtados con precio mínimo de {min_price} euros",
        "total_found": max_results
    }

# URL para probar:
# http://localhost:8000/analytics?min_price=9.99&max_results=10


# búsqueda avanzada
@app.get("/search")
def advanced_search(
    # parámetro OBLIGATORIO con validación de longitud (2 a 100 caracteres)
    query: str = Query(..., min_length=2, max_length=100),
    category: Optional[str] = Query(None, min_length=2),
    min_price: Optional[float] = Query(None, ge=0.0)
):
    filters = {"query": query}
    
    if category:
        filters["category"] = category
    
    if min_price is not None:
        filters["min_price"] = min_price
    
    return {
        "query": query,
        "filters": filters,
        "results": [f"Resultado para '{query}' #{i}" for i in range(1, 4)],
        "total_results": 3
    }

# URL para probar:
# http://localhost:8000/search?query=busqueda&category=dairy&min_price=2.99