from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Integer, String, Boolean, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session

"""
VIDEO
- id: int
- title: string (obligatorio)
- channel: string (obligatorio)
- views: entero (opcional)
- has_subtitles: booleano (opcional)
"""

# CONFIGURACIÓN DE BASE DE DATOS
# motor de conexión
engine = create_engine(
    "sqlite:///09_sqlalchemy/videos.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# crear fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)


# MODELO DE BASE DE DATOS (SQLALCHEMY)
# clase base
class Base(DeclarativeBase):
    pass

# modelo de tabla videos
class Video(Base):
    __tablename__ = "videos"
    
    # id, clave primaria
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # obligatorio, 200 caracteres como máximo
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    # obligatorio, 200 caracteres como máximo
    channel: Mapped[str] = mapped_column(String(200), nullable=False)
    # optional
    views: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # optional
    has_subtitles: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


# MODELOS PYDANTIC (SCHEMAS)
class VideoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    channel: str
    views: int | None
    has_subtitles: bool | None

class VideoCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    channel: str
    views: int | None = None
    has_subtitles: bool | None = None

class VideoUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    channel: str
    views: int | None
    has_subtitles: bool | None

class VideoPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str | None = None
    channel: str | None = None
    views: int | None = None
    has_subtitles: bool | None = None


# INICIALIZACIÓN DE BASE DE DATOS
# crear las tablas de la base de datos
Base.metadata.create_all(engine)

# poblar tablas
def init_db():
    db = SessionLocal()
    try:
        existing_videos = db.execute(select(Video)).scalars().all()
        
        if existing_videos:
            return
        
        default_videos = [
            Video(title="Grajillas cantanto", channel="La Grajilla", views=9999999, has_subtitles=True),
            Video(title="Curso de FastAPI", channel="Gente muy pro", views=5000, has_subtitles=False),
            Video(title="Cómo instalar Linux", channel="Linux el mejor", views=25000, has_subtitles=True),
            Video(title="Música ASMR para dormir", channel="ASMR para todos", views=400, has_subtitles=False),
            Video(title="Cómo atraer aves a tu jardín", channel="Avibérico", views=8080, has_subtitles=True)
        ]
        
        db.add_all(default_videos)
        db.commit()
    finally:
        db.close()

# DEPENDENCIA DE FASTPI
# método para dar sesión de base de datos al endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# APLICACIÓN FASTAPI


# ENDPOINTS CRUD (Create, Read, Update, Delete)
"""
Create: Método POST (create)
Read: Método GET (find_all y find_by_id)
Update: Método PUT (update_full) y método PATCH (update_partial)
Delete: Método DELETE (delete)
"""