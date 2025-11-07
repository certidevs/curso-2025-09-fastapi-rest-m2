from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Float, Date, DateTime
from datetime import date, datetime
from typing import Optional

# base para modelos sqlalchemy
class Base(DeclarativeBase):
    pass

# modelos pydantic y sqlalchemy

# USUARIO
class Usuario(BaseModel):
    nombre: str
    email: str
    edad: int

class UsuarioORM(Base):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    edad: Mapped[int] = mapped_column(Integer, nullable=False)

# LIBRO
class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int

class LibroORM(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    autor: Mapped[str] = mapped_column(String, nullable=False)
    paginas: Mapped[int] = mapped_column(Integer, nullable=False)

# CATEGORIA
class Categoria(BaseModel):
    nombre: str
    codigo: str

class CategoriaORM(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    codigo: Mapped[str] = mapped_column(String, nullable=False)

# PRODUCTO
class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int
    disponible: Boolean

class ProductoORM(Base):
    __tablename__ = "productos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    precio: Mapped[float] = mapped_column (Float, nullable=False)
    stock: Mapped[int] = mapped_column (Integer, nullable=False)
    disponible: Mapped[bool] = mapped_column (Boolean, nullable=False)

# EVENTO
class Evento(BaseModel):
    nombre: str
    fecha: date
    hora_inicio: datetime
    capacidad: int
    activo: bool

class EventoORM(Base):
    __tablename__ = "eventos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    hora_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False)

# CLIENTE
class Cliente(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ClienteORM(Base):
    __tablename__ = "clientes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    direccion: Mapped[Optional[str]] = mapped_column(String)

# ARTICULO
class Articulo(BaseModel):
    titulo: str
    contenido: str
    autor: str
    fecha_publicacion: Optional[date] = None
    vistas: Optional[int] = 0

class ArticuloORM(Base):
    __tablename__ = "articulos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    contenido: Mapped[str] = mapped_column(String, nullable=False)
    autor: Mapped[str] = mapped_column(String, nullable=False)
    fecha_publicacion: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    vistas: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)