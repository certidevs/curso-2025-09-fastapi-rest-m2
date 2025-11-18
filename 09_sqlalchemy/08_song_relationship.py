from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy import ForeignKey, create_engine, Integer, String, Boolean, DateTime, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, Session, relationship, joinedload
from datetime import datetime


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

# modelo de la tabla artist
class Artist(Base):
    __tablename__ = "artists"
    
    # clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requerido, máximo 200 caracteres
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    # opcional
    birth_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

# modelo de la tabla song (se crea sólo un modelo, que será una tabla en nuestra base de datos)
class Song(Base):
    __tablename__ = "songs" # nombre de la tabla en bd
    
    # clave primaria, se genera automáticamente
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # requerido, máximo 200 caracteres
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    
    # relación ManyToOne con Artist unidireccional
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"), nullable=False)
    
    artist: Mapped[Artist] = relationship(Artist)
    
    # opcional
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # opcional
    explicit: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


# MODELOS PYDANTIC (schemas)
# modelos que validan los datos que llegan y salen de la api

# schema para Artist en respuestas
class ArtistResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    birth_date: datetime | None

# schema para TODAS las respuestas de la API
# lo usamos en GET, POST, PUT, PATCH
class SongResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    artist: ArtistResponse
    duration_seconds: int | None
    explicit: bool | None

# schema para CREAR una canción (POST)
# no incluimos id porque se genera automáticamente
class SongCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    artist_id: int
    duration_seconds: int | None = None
    explicit: bool | None = None
    
    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        # verificar si el valor está vacío o sólo tiene espacios
        if not v or not v.strip():
            raise ValueError("El título no puede estar vacío")

        # retorna el valor sin espacios al principio y al final (normalizar)
        return v.strip()
    
    @field_validator("duration_seconds")
    @classmethod
    def validate_duration_positive(cls, v: int | None) -> int | None:
        # valida sólo si se da un valor (no es None)
        if v is not None and v < 0:
            raise ValueError("La duración debe ser un número positivo")
        
        return v
        

# schema para ACTUALIZACIÓN COMPLETA (PUT)
# todos los campos se tienen que enviar
class SongUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    artist_id: int
    duration_seconds: int | None
    explicit: bool | None
    
    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        
        return v.strip()
    
    @field_validator("duration_seconds")
    @classmethod
    def validate_duration_positive(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("La duración debe ser un número positivo")
        
        return v

# schema para ACTUALIZACIÓN PARCIAL (PATCH)
# sólo se envían los campos que quieras actualizar
class SongPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str | None = None
    artist_id: int | None = None
    duration_seconds: int | None = None
    explicit: bool | None = None
    
    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str | None) -> str | None:
        # si no se proporcionó valor (None), no validamos
        if v is None:
            return None
        
        # si se proporcionó valor, validamos que no esté vacío
        if not v or not v.strip():
            raise ValueError("Este campo no puede estar vacío")
        
        return v.strip()
    
    @field_validator("duration_seconds")
    @classmethod
    def validate_duration_positive(cls, v: int | None) -> int | None:
        if v is None:
            return None
        
        if v < 0:
            raise ValueError("La duración debe ser un número positivo")
        
        return v
    

# INICIALIZACIÓN BASE DE DATOS

# crear todas las tablas
Base.metadata.create_all(engine)

# método inicializar con canciones por defecto
def init_db():
    """
    Inicializa la base de datos con canciones por defecto si está vacía.
    Sólo crea las canciones si no existen ya en la base de datos.
    """
    db = SessionLocal()
    try:
        existing_songs = db.execute(select(Song)).scalars().all()
        
        if existing_songs:
            return
        
        default_artists = [
            Artist(name="ABBA", birth_date=datetime(1972, 1, 1)),
            Artist(name="Amaral", birth_date=datetime(1972, 8, 4)),
            Artist(name="Ludwig van Beethoven", birth_date=None),
            Artist(name="Joan Manuel Serrat", birth_date=None),
            Artist(name="Darren Korb", birth_date=None),
            Artist(name="Michael Jackson", birth_date=None),
            Artist(name="Nirvana", birth_date=None)
        ]
        
        db.add_all(default_artists)
        db.commit()
        
        # refresca los artistas para obtener su id
        for artist in default_artists:
            db.refresh(artist)
        
        default_songs = [
            Song(title="Mamma Mia", artist_id=default_artists[0].id, duration_seconds=300, explicit=False),
            Song(title="Sin ti no soy nada", artist_id=default_artists[1].id, duration_seconds=250, explicit=False),
            Song(title="Sonata para piano nº 14", artist_id=default_artists[2].id, duration_seconds=800, explicit=False),
            Song(title="Mediterráneo", artist_id=default_artists[3].id, duration_seconds=400, explicit=False),
            Song(title="Never to Return", artist_id=default_artists[4].id, duration_seconds=300, explicit=False),
            Song(title="Billie Jean", artist_id=default_artists[5].id, duration_seconds=294, explicit=False),
            Song(title="Smells Like Teen Spirit", artist_id=default_artists[6].id, duration_seconds=301, explicit=True),
            Song(title="Dancing Queen", artist_id=default_artists[0].id, duration_seconds=250, explicit=False),
            Song(title="Lay All Your Love On Me", artist_id=default_artists[0].id, duration_seconds=250, explicit=False),
            Song(title="El Universo Sobre Mí", artist_id=default_artists[1].id, duration_seconds=150, explicit=False)
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
    # .scalars(): extrae los objetos Song
    # .all(): obtiene los resultados como lista
    return db.execute(select(Song).options(joinedload(Song.artist))).unique().scalars().all()

# GET - obtener UNA canción por id
@app.get("/api/songs/{id}", response_model=SongResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    # busca la canción con el id de la ruta
    # .scalar_one_or_none(): devuelve el objeto o None si no existe
    song = db.execute(
        select(Song).where(Song.id == id).options(joinedload(Song.artist))
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
    
    artist = db.execute(
        select(Artist).where(Artist.id == song_dto.artist_id)
    ).scalar_one_or_none()
    
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el artista con id {song_dto.artist_id}"
        )
    
    # crea objeto Song con datos validados
    song = Song(
        title=song_dto.title,
        artist_id=song_dto.artist_id,
        duration_seconds=song_dto.duration_seconds,
        explicit=song_dto.explicit
    )
    
    db.add(song) # agrega el objeto a la sesión
    db.commit() # confirma la creación en base de datos
    
    song_with_artist = db.execute(
        select(Song).where(Song.id == song.id).options(joinedload(Song.artist))
    ).scalar_one()
    
    return song_with_artist # retorna la canción creada

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
    
    artist = db.execute(
        select(Artist).where(Artist.id == song_dto.artist_id)
    ).scalar_one_or_none()
    
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se ha encontrado el artista con id {song_dto.artist_id}"
        )
        
    # guarda el diccionario sacado de song_dto
    update_data = song_dto.model_dump()
    
    # bucle para asignar el valor del diccionario a cada atributo
    for field, value in update_data.items():
        setattr(song, field, value)
    
    db.commit() # confirma los cambios
    
    song_with_artist = db.execute(
        select(Song).where(Song.id == id).options(joinedload(Song.artist))
    ).scalar_one()
    
    return song_with_artist # retorna la canción actualizada

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
    
    update_data = song_dto.model_dump(exclude_unset=True)
    
    if "artist_id" in update_data:
        artist = db.execute(
            select(Artist).where(Artist.id == update_data["artist_id"])
        ).scalar_one_or_none()
        
        if not artist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se ha encontrado el artista con id {update_data['artist_id']}"
            )
    
    for field, value in update_data.items():
        setattr(song, field, value)
    
    db.commit() # confirma los cambios en base datos
    
    song_with_artist = db.execute(
        select(Song).where(Song.id == id).options(joinedload(Song.artist))
    ).scalar_one()
    
    return song_with_artist

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