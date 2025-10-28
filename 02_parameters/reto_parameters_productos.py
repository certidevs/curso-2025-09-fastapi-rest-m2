from fastapi import FastAPI

app = FastAPI()

@app.get("/products/{product_id}")
def get_product(product_id: int, include_price: bool = False, include_stock: bool = False, format: str = "summary"):
    # crear un diccionario inicial con datos básicos
    product_data = {
        "product_id": product_id,
        "name": f"Producto {product_id}",
        "category": f"Categoría {product_id % 3 + 1}",
        "format": format
    }
    
    # añadir precio si include_price es true
    if include_price:
        product_data["price"] = f"{product_id * 10}.99"
    
    # añadir stock si include_stock es true
    if include_stock:
        product_data["stock"] = f"{product_id * 5} unidades"
    
    return product_data

# probar URL:
# http://localhost:8000/products/5?include_price=true&include_stock=true&format=basic