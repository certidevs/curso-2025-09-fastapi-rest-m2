from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int, include_email: bool = False, format: str = "basic"):
    # diccionario base
    user_data = {
        "user_id": user_id,
        "name": f"Usuario {user_id}",
        "format": format
    }
    
    # añadir email si include_email es True
    if include_email:
        user_data["email"] = f"user{user_id}@example.com"
        
    return user_data

"""
Poner en la url del navegador para comprobar:

- base: 
    http://localhost:8000/users/8
- incluyendo email:
    http://localhost:8000/users/8?include_email=true
- incluyendo format:
    http://localhost:8000/users/8?format=complete
- incluyendo email y format: 
    http://localhost:8000/users/8?include_email=true&format=complete
"""