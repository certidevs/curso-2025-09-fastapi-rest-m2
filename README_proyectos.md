## PROYECTO

### Equipos

#### Equipo 1

**Temática**: Clínica veterinaria: Mascota, Duenyo, Veterinario, Visita...

Repo: https://github.com/albanomp/Proyecto-Clinica-Veterinaria

- **Jorge**
- Albano
- Marcos

Tareas:

* [OK] entidades sql-alchemy
* [OK] modelos pydantic DTOs
* [OK] API REST CRUD para cada modelo
* [] carpeta templates y listados HTML
* [] unificar las api rest en una sola app FastAPI dividido en archivos:
  * models.py: sqlalchemy (clave primaria, claves foráneas)
  * schemas.py: pydantic
  * routes/pets.py (api rest de mascotas)
  * routes/appointments.py (api rest citas)
  * db.py
  * main.py (aquí se crea la app de fastapi)
  * templates/ con los htmls


#### Equipo 2

**Temática**: Gestor de videojuegos: Videojuego, Genero, Desarrolladora, Usuario...

Repo: https://github.com/Mapakitus/gestor-videojuegos

- **Paco**
- Jon
- Lueyo

* [OK] mover rama lueyo 
* [OK] resetear main:
  * Opción 1: deshacer ultimos 8 commits:
    * git reset --hard HEAD~8
    * git push --force
  * Opción 2: 
    * manualmente colocar todo a un estado deseado
* [] Entidades:
  * Videojuego (ManyToOne con Genero, ManyToOne Desarrolladora) (Paco)
  * Genero  (Jon)
  * Desarrolladora (Lueyo)
  * Usuario (id, email, nif, password, saldo) (Lueyo)
  * Review (ManyToOne Videojuego, ManyToOne Usuario)
  * Compra (ManyToOne Videojuego, ManyToOne Usuario)
* Schemas pydantic
* API REST CRUD
* HTMLs
* Opcional autenticación:
  * registro.html
  * login.html
  * lógica para detectar el usuario autenticado en los controladores
  * opción simple:
    * no hacer registro ni login, simplemente tener un usuario en base datos y vincular cada operación de Review o Compra a ese usuario


#### Equipo 3

**Temática**: Cartelera de cine: Pelicula, Sala, Genero, Proyeccion...

Repo: https://github.com/HueteDevs/Proyecto_Adecco

- Javi
- Reyes
- Kary
- Iñaki
- Manuel

* Entidades
    * Pelicula
    * Sala
    * Genero
* Schemas
* API REST CRUD
* HTMLs
* Asociaciones
* Arquitectura

* 1. crear rama "arquitectura" copia de main Javier
* 2. En main, nueva estructura minima:
  * models/ 
  * routes/
  * schemas/
  * templates/ para los htmls
  * database.py
  * main.py

#### Equipo 4

**Temática**: Biblioteca: Libro, Autor, Socio, Prestamo...

Repo: https://github.com/RaresID/biblioteca-commerce

- **Rafael**
- Deme
- Rares
- Alejandro Gómez

* [] Entidades
  * Book (ManyToOne Author, ManyToOne Editorial)
  * Author 
  * Editorial
  * User
  * Compra (id, fecha, precio, ManyToOne Book, ManyToOne User)

* [] Schemas pydantic
* [] API REST CRUD
* HTMLs templates


## AVANCE

* Reuniones
* GitHub
* main.py con api rest con sqlalchemy con sqlite
* Pensar tablas de base de datos con SQLAlchemy 
    * primero solo dos atributos: campo id y otro atributo
    * agregar atributos uno a uno, probando cada uno
    * (primero sin asociaciones)
* API REST operaciones CRUD por el API REST, probando en Swagger UI
* Asociaciones: intentar una/dos asociación Many To One


## Ejemplo de arquitectura

Hemos empezado desarrollando la aplicación en un solo archivo por simplicidad, la idea es ampliar la arquitectura conforme evoluciona la aplicación.

```
├── app/
│ ├── main.py
│ ├── models/ # Capa de Persistencia: Definiciones de Tablas (SQLAlchemy ORM)
│ │ ├── pelicula.py # Entidad Pelicula
│ │ ├── genero.py # Entidad Genero
│ │ ├── sala.py # Entidad Sala
│ │ ├── horario.py # Entidad Horario
│ │ ├── venta.py # Entidad Venta
│ │ ├── socio.py # Entidad Socio
│ │ └── login.py # Entidad Login / Usuario
│ ├── schemas/ # Capa de Serialización/Validación (Pydantic, Marshmallow, etc.)
│ │ ├── pelicula.py # Esquemas de entrada y salida para Peliculas
│ │ ├── genero.py # Esquemas de entrada y salida para Generos
│ │ ├── sala.py # Esquemas de entrada y salida para Salas
│ │ ├── horario.py # Esquemas de entrada y salida para Horarios
│ │ ├── venta.py # Esquemas de entrada y salida para Ventas
│ │ ├── socio.py # Esquemas de entrada y salida para Socios
│ │ └── auth.py # Esquemas para Login/Registro/Tokens
│ ├── services/ # Capa de Lógica de Negocio (El 'cerebro' de la aplicación)
│ │ ├── pelicula.py # Funciones CRUD y validaciones de negocio para Pelicula
│ │ ├── genero.py # Funciones CRUD y validaciones de negocio para Genero
│ │ ├── sala.py # Funciones CRUD y validaciones de negocio para Sala
│ │ ├── horario.py # Funciones CRUD y validaciones de negocio para Horario
│ │ ├── venta.py # Funciones CRUD y validaciones de negocio para Venta
│ │ ├── socio.py # Funciones CRUD y validaciones de negocio para Socio
│ │ └── auth.py # Lógica para manejo de usuarios, *hashing* de contraseñas y tokens
│ ├── routes/ # Capa de Controladores: Manejo de Peticiones HTTP
│ │ ├── peliculas.py # Rutas CRUD Peliculas (Llama a `services/pelicula.py`)
│ │ ├── generos.py # Rutas CRUD Generos
│ │ ├── salas.py # Rutas CRUD Salas
│ │ ├── horarios.py # Rutas CRUD Horarios
│ │ ├── ventas.py # Rutas CRUD Ventas
│ │ ├── socios.py # Rutas CRUD Socios
│ │ └── login.py # Rutas de autenticación / login (Llama a `services/auth.py`)
│ ├── database/
│ │ ├── db.py # Motor de conexión SQLAlchemy y sesión (dependencia inyectada)
│ │ ├── db.sql # Schema y seed de la base de datos (Script SQL)
│ │ └── db.db # Base de datos SQLite
│ ├── templates/ # Vistas (Jinja2, etc.)
│ │ ├── base.html # Layout común
│ │ ├── peliculas/ # Vistas HTML de peliculas
│ │ ├── generos/ # Vistas HTML de generos
│ │ ├── salas/ # Vistas HTML de salas
│ │ ├── horarios/ # Vistas HTML de horarios
│ │ ├── ventas/ # Vistas HTML de ventas
│ │ ├── socios/ # Vistas HTML de socios
│ │ └── login/ # Vistas HTML de login/autenticación
│ └── static/
│ ├── Bootstrap/ # Hojas de estilo y JS de Bootstrap
│ │ ├── css/ # Archivos CSS de Bootstrap (bootstrap.min.css)
│ │ └── js/ # Archivos JavaScript de Bootstrap (bootstrap.bundle.min.js)
│ ├── css/ # Hojas de estilo (CSS3/Bootstrap)
│ ├── js/ # Archivos JavaScript
│ └── img/ # Imágenes y assets
├── requirements.txt # Dependencias del proyecto (Framework, ORM, Pydantic, etc.)
├── README.html # Documentación inicial y guía de instalación
└── run.py
```