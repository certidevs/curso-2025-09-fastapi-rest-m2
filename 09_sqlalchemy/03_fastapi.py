"""
pip install -r requirements.txt
API REST de FastAPI con SQLAlchemy y SQLite
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# Configurar base de datos
engine = create_engine('sqlite:///ecommerce.db', echo=True) # echo True para mostrar SQL solo en desarrollo
SessionLocal = sessionmaker(bind=engine)

# Crear clase Base
class Base(DeclarativeBase):
    pass

# SQLALCHEMY MODELS : crear entidades que heredan de Base (models.py)
class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

# PYDANTIC MODELS : crear schemas pydantic (schemas.py)
class ProductDTO(BaseModel):
    nombre: str | None = None

# Crear tablas
Base.metadata.create_all(engine)

# API REST FastAPI con SQLAlchemy
app = FastAPI(title='Products App', version='1.0.0')

@app.get('/')
def home():
    return {'mensaje': 'Products API'}

# API REST:
# GET all products JSON
@app.get('/api/products')
def find_all():
    session = SessionLocal()
    # opción tradicional query
    # products = session.query(Product).all()
    
    # opción moderna select
    statement = select(Product)
    products = session.execute(statement).scalars().all()
    
    session.close()
    return products

# GET one product BY ID
@app.get('/api/products/{id}')
def find_by_id(id: int):
    session = SessionLocal()
    # opción tradicional query
    # product = session.query(Product).filter(Product.id == id).first()
    
    # opción moderna
    product = session.execute(
        select(Product).where(Product.id == id)
    ).scalar_one_or_none()
    
    session.close()
    if not product:
        raise HTTPException(status_code=404, detail='Not found')
    return product


# POST create product
@app.post('/api/products')
def create(product_dto: ProductDTO):
    session = SessionLocal()
    product = Product(nombre=product_dto.nombre)
    session.add(product) # guardar en base de datos INSERT
    session.commit()
    session.refresh(product) # actualizar id de product
    session.close()
    return product


# PUT update product
# DELETE remove product

# HTML:
# GET all products HTML
# GET one product HTML
# POST create/update product