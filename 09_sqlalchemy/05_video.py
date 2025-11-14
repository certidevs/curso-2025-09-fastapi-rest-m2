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


# MODELO DE BASE DE DATOS (SQLALCHEMY)


# MODELOS PYDANTIC (SCHEMAS)


# INICIALIZACIÓN DE BASE DE DATOS


# DEPENDENCIA DE FASTPI


# APLICACIÓN FASTAPI


# ENDPOINTS CRUD (Create, Read, Update, Delete)
"""
Create: Método POST (create)
Read: Método GET (find_all y find_by_id)
Update: Método PUT (update_full) y método PATCH (update_partial)
Delete: Método DELETE (delete)
"""