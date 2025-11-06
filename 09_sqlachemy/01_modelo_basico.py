from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, Boolean

app = FastAPI()

# modelo Pydantic
class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int
    disponible: bool

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