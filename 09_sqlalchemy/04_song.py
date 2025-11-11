from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Integer, String, Boolean, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

# configurar base de datos

# crear motor de conexión a base de datos
engine = create_engine(
    "sqlite:///09_sqlalchemy/cancioncitas.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# crear fábrica de sesiones de base de datos
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

# modelo base de datos (sqlalchemy)

# clase base para modelos sqlalchemy
class Base(DeclarativeBase):
    pass

# modelo de la tabla song (se crea sólo un modelo, que será una tabla en nuestra base de datos)
class Song(Base):
    __tablename__ = "songs" # nombre de la tabla en bd
    
    # clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requerido, máximo 200 caracteres
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    # requerido, máximo 200 caracteres
    artist: Mapped[str] = mapped_column(String(200), nullable=False)
    # opcional
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # optional
    explicit: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

# modelos pydantic (schemas)
# modelos que validan los datos que llegan y salen de la api

# schema para TODAS las respuestas de la API
# lo usamos en GET, POST, PUT, PATCH
class SongResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    artist: str
    duration_seconds: int | None
    explicit: bool | None

# schema para CREAR una canción (POST)
# no incluimos id porque se genera automáticamente
class SongCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    artist: str
    duration_seconds: int | None = None
    explicit: bool | None = None

# schema para ACTUALIZACIÓN COMPLETA (PUT)
# todos los campos se tienen que enviar
class SongUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    artist: str
    duration_seconds: int | None
    explicit: bool | None

# schema para ACTUALIZACIÓN PARCIAL (PATCH)
# sólo se envían los campos que quieras actualizar
class SongPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str | None = None
    artist: str | None = None
    duration_seconds: int | None = None
    explicit: bool | None = None

# inicialización base de datos

# crear todas las tablas
Base.metadata.create_all(engine)

# método inicializar con canciones por defecto
def init_db():
    """
    Inializa la base de datos con canciones por defecto si está vacía.
    Sólo crea las canciones si no existen ya en la base de datos.
    """
    db = SessionLocal()
    try:
        existing_songs = db.execute(select(Song)).scalars().all()
        
        if existing_songs:
            return
        
        default_songs = [
            Song(title="Mamma Mia", artist="ABBA", duration_seconds=300, explicit=False),
            Song(title="Sin ti no soy nada", artist="Amaral", duration_seconds=250, explicit=False),
            Song(title="Sonata para piano nº 14", artist="Ludwing van Beethoven", duration_seconds=800, explicit=False),
            Song(title="Mediterráneo", artist="Joan Manuel Serrat", duration_seconds=400, explicit=False),
            Song(title="Never to Return", artist="Darren Korb", duration_seconds=300, explicit=False),
            Song(title="Billie Jean", artist="Michael Jackson", duration_seconds=294, explicit=False),
            Song(title="Smells Like Teen Spirit", artist="Nirvana", duration_seconds=301, explicit=True),
            Song(title="It's my life", artist="Bon Jovi", duration_seconds=400 , explicit=False),
            Song(title="Ni idea ahora mismo", artist="Inventado", duration_seconds=300, explicit=False),
            Song(title="Viva la vida", artist="Cold Play", duration_seconds=314, explicit=False),
            Song(title = "Neckhurts", artist= "Chadolf", duration_seconds = 300, explicit=True),
            Song(title="La Rosa de Los Vientos", artist="Mägo de Oz", duration_seconds=258, explicit=False),
            Song(title="Paranoid Android", artist="Radiohead", duration_seconds=386, explicit=True),
            Song(title="No me creas", artist= "Alberto plaza", duration_seconds=260, explicit=False)
        ]
        
        # agregar las canciones
        db.add_all(default_songs)
        db.commit()
    finally:
        db.close()

init_db()