"""Versión 2 de la API (la actual).

Cambios respecto a la v1:
  - "nombre" pasa a llamarse "fullName"  -> BREAKING CHANGE (por eso hay v2)
  - se añade el campo "email"            -> NO es breaking (solo suma)
  - se puede crear usuarios con POST     -> endpoint nuevo
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .data import USERS, siguiente_id


class UserV2(BaseModel):
    id: int
    fullName: str
    email: str


class UserCreate(BaseModel):
    fullName: str
    email: str


router = APIRouter(prefix="/v2", tags=["v2 (actual)"])


def a_v2(u: dict) -> dict:
    return {"id": u["id"], "fullName": u["name"], "email": u["email"]}


@router.get("/users", response_model=list[UserV2], summary="Listar usuarios (v2)")
def listar_usuarios():
    return [a_v2(u) for u in USERS]


@router.get("/users/{user_id}", response_model=UserV2, summary="Obtener un usuario (v2)")
def obtener_usuario(user_id: int):
    for u in USERS:
        if u["id"] == user_id:
            return a_v2(u)
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@router.post("/users", response_model=UserV2, status_code=201, summary="Crear un usuario (v2)")
def crear_usuario(datos: UserCreate):
    nuevo = {"id": siguiente_id(), "name": datos.fullName, "email": datos.email}
    USERS.append(nuevo)
    return a_v2(nuevo)
