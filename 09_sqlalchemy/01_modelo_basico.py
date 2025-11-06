from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Boolean

app = FastAPI()

# modelo Pydantic
class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int
    disponible: bool


# configuración de base de datos
DATABASE_URL = "sqlite:///09_sqlalchemy/productos_prueba.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)


# base declarativa
class Base(DeclarativeBase):
    pass

# modelo ORM SQLAlchemy (tabla)
class ProductoORM(Base):
    __tablename__ = "productos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    disponible: Mapped[bool] = mapped_column(Boolean, nullable=False)


# crear tablas
Base.metadata.create_all(bind=engine)


# crear 3 productos
db = SessionLocal()
try:
    productos_existentes = db.query(ProductoORM).first()
    if not productos_existentes:
        productos = [
            ProductoORM(id=1, nombre="Leche", precio=1.99, stock=30, disponible=True),
            ProductoORM(id=2, nombre="Queso", precio=10.99, stock=15, disponible=True),
            ProductoORM(id=3, nombre="Yogur", precio=2.99, stock=25, disponible=True)
        ]
        db.add_all(productos)
        db.commit()
finally:
    db.close()