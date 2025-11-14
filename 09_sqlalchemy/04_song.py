from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Integer, String, Boolean, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session


# CONFIGURACIÓN BASE DE DATOS

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


# MODELO BASE DE DATOS (sqlalchemy)

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


# MODELOS PYDANTIC (schemas)
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


# INICIALIZACIÓN BASE DE DATOS

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
            Song(title="Smells Like Teen Spirit", artist="Nirvana", duration_seconds=301, explicit=True)
        ]
        
        # agregar las canciones
        db.add_all(default_songs)
        db.commit()
    finally:
        db.close()

# inicializa la base de datos con canciones por defecto
init_db()


# DEPENDENCIA DE FASTAPI

def get_db():
    db = SessionLocal()
    try:
        yield db # entrega la sesión al endpoint
    finally:
        db.close()



# APLICACIÓN FASTAPI

# crea la instancia de la aplicación FastAPI
app = FastAPI(title="Cancioncitas", version="1.0.0")

# endpoint raíz
@app.get("/")
def home():
    return {"mensaje": "Bienvenido a la app Cancioncitas"}


# ENDPOINTS CRUD

# GET - obtener TODAS las canciones
@app.get("/api/songs", response_model=list[SongResponse])
def find_all(db: Session = Depends(get_db)):
    # db.execute(): ejecuta la consulta
    # select(Song): crea consulta SELECT * FROM song
    # .scarlars(): extrae los objetos Song
    # .all(): obtiene los resultados como lista
    return db.execute(select(Song)).scalars().all()

# GET - obtener UNA canción por id
@app.get("/api/songs/{id}", response_model=SongResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    # busca a canción con el id de la ruta
    # .scalar_one_or_none(): devuelve el objeto o None si no existe
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    return song

# POST - crear una nueva canción
@app.post("/api/songs", response_model=SongResponse, status_code=status.HTTP_201_CREATED)
def create(song_dto: SongCreate, db: Session = Depends(get_db)):
    # validaciones
    if not song_dto.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El título de la canción no puede estar vacío"
        )
    
    if not song_dto.artist.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El artista de la canción no puede estar vacío"
        )
    
    if song_dto.duration_seconds is not None and song_dto.duration_seconds < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La duración debe ser un número positivo"
        )
    
    # crea objeto Song con datos validados
    song = Song(
        title=song_dto.title.strip(),
        artist=song_dto.artist.strip(),
        duration_seconds=song_dto.duration_seconds,
        explicit=song_dto.explicit
    )
    
    db.add(song) # agrega el objeto a la sesión
    db.commit() # confirma la creación en base de datos
    db.refresh(song) # refresca el objeto para obtener el id generado
    return song # retorna la canción creada

# PUT - actualizar COMPLETAMENTE una canción
@app.put("/api/songs/{id}", response_model=SongResponse)
def update_full(id: int, song_dto: SongUpdate, db: Session = Depends(get_db)):
    # busca canción por id
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    
    # validaciones (igual que en POST)
    if not song_dto.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El artista de la canción no puede estar vacío"
        )
    
    if not song_dto.artist.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El artista de la canción no puede estar vacío"
        )
    
    if song_dto.duration_seconds is not None and song_dto.duration_seconds < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La duración debe ser un número positivo"
        )
    
    song.title = song_dto.title.strip()
    song.artist = song_dto.artist.strip()
    song.duration_seconds = song_dto.duration_seconds
    song.explicit = song_dto.explicit
    
    db.commit() # confirma los cambios
    db.refresh(song) # refresca el objeto de la base de datos
    return song # retorna la canción actualizada

# PATCH - actualizar PARCIALMENTE una canción
@app.patch("/api/songs/{id}", response_model=SongResponse)
def update_partial(id: int, song_dto: SongPatch, db: Session = Depends(get_db)):
    # busca canción por id
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    
    # actualiza SÓLO los campos que se han enviado (no son None)
    if song_dto.title is not None:
        if not song_dto.title.strip():
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El título de la canción no puede estar vacío"
        )
        song.title = song_dto.title.strip()
    
    if song_dto.artist is not None:
        if not song_dto.artist.strip():
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El artista de la canción no puede estar vacío"
        )
        song.artist = song_dto.artist.strip()
    
    if song_dto.duration_seconds is not None:
        if song_dto.duration_seconds < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La duración debe ser un número positivo"
            )
        song.duration_seconds = song_dto.duration_seconds
    
    if song_dto.explicit is not None:
        song.explicit = song_dto.explicit
    
    db.commit() # confirma los cambios en base datos
    db.refresh(song) # refresca el objeto
    return song

# DELETE - eliminar una canción
@app.delete("/api/songs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    # busca la canción por id
    song = db.execute(
        select(Song).where(Song.id == id)
    ).scalar_one_or_none()
    
    # si no existe, devuelve 404
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado la canción con id {id}"
        )
    
    # elimina la canción de base de datos
    db.delete(song) # marca el objeto para eliminación
    db.commit() # confirma la eliminación en base de datos
    return None