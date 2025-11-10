"""
pip install -r requirements.txt
API REST de FastAPI con SQLAlchemy y SQLite
"""
from fastapi import FastAPI
from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# Configurar base de datos
engine = create_engine('sqlite:///ecommerce.db')
SessionLocal = sessionmaker(bind=engine)

# Crear clase Base
class Base(DeclarativeBase):
    pass

# crear entidades que heredan de Base (models.py)
class Product(Base):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

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
    products = session.query(Product).all()
    session.close()
    return products

# GET one product
# POST create product
# PUT update product
# DELETE remove product

# HTML:
# GET all products HTML
# GET one product HTML
# POST create/update product