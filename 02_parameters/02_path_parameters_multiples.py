from fastapi import FastAPI

app = FastAPI()

@app.get("/categories/{category_id}/products/{product_id}")
def get_category_product(category_id: int, product_id: int):
    return {
        "category_id": category_id, 
        "product_id": product_id,
        "name": f"Producto {product_id} de la categoría {category_id}"
    }

@app.get("/projects/{project_id}/tasks/{task_id}")
def get_project_task(project_id: int, task_id: int):
    return {
        "project_id": project_id,
        "task_id": task_id,
        "task_title": f"Tarea {task_id} del proyecto {project_id}"
    }