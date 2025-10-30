# Módulo 2: FastAPI REST + SQLAlchemy.

**Versiones:** 
- FastAPI 0.116.2
- SQLAlchemy 2.0.43

## FastAPI fundamentals
- **Introducción** al framework FastAPI
- **Instalación** y **configuración** del entorno y dependencias
- **Métodos HTTP**: GET, POST, PUT, PATCH, DELETE
- **Validación** automática con Pydantic
- **Documentación** automática con Swagger/OpenAPI

## Conceptos avanzados de FastAPI
- **Path parameters** y **query parameters**
- **Cabeceras HTTP** y **modelos de respuesta**
- Manejo centralizado de **errores** y **excepciones**
- Códigos de **estado HTTP**
- **Dependency Injection** para arquitectura limpia

## Integración con SQLAlchemy
- **Configuración** de SQLAlchemy con FastAPI
- Definición de **modelos** de base de datos
- **Esquemas Pydantic** vs **modelos SQLAlchemy**
- **DTOs** y **Mappers** para transformación de datos
- **Tipos de datos**, **validaciones** y **constraints**

## Patrones de arquitectura
- **Operaciones CRUD** básicas
- **Repository Pattern**: separación de lógica de datos
- **Service Layer**: lógica de negocio centralizada
- Consultas avanzadas con **Joins** y **filtros**
- **Asociaciones** entre modelos (relaciones)

## Gestión de base de datos
- **Migraciones** automáticas con Alembic
- **Testing** de APIs con TestClient
- **Buenas prácticas** de desarrollo


1. Clonar repositorio m2
2. Crear archivo requirements.txt
3. Crear entorno venv
4. Hola mundo en fastapi

## Entorno virtual

* 1. Crear entorno virtual:
    * Opción 1: hacerlo con visual studio code con Create Environment
    * Opción 2: python -m venv .venv

* 2. Activar el entorno
    * Windows powershell: .venv\Scripts\activate
    * Git Bash: source .venv/Scripts/activate
    
* 3. Instalar dependencias:
    * pip install -r requirements.txt