"""Versión 1 de la API (la antigua). Está DEPRECADA: sigue funcionando,
pero avisa a los clientes de que deben migrar a la v2."""

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from .data import USERS


class UserV1(BaseModel):
    id: int
    nombre: str  # <- en la v2 este campo se llamará "fullName" (breaking change)


def avisar_deprecacion(response: Response):
    """Añade cabeceras HTTP a TODAS las respuestas de la v1."""
    response.headers["Deprecation"] = "@1790812800"  # desde el 1-oct-2026 (RFC 9745)
    response.headers["Sunset"] = "Thu, 31 Dec 2026 23:59:59 GMT"  # se apaga el 31-dic-2026
    response.headers["Link"] = '</v2/users>; rel="successor-version"'


router = APIRouter(
    prefix="/v1",
    tags=["v1 (deprecada)"],
    deprecated=True,  # Swagger la mostrará tachada
    dependencies=[Depends(avisar_deprecacion)],
)


@router.get("/users", response_model=list[UserV1], summary="Listar usuarios (v1)")
def listar_usuarios():
    return [{"id": u["id"], "nombre": u["name"]} for u in USERS]


@router.get("/users/{user_id}", response_model=UserV1, summary="Obtener un usuario (v1)")
def obtener_usuario(user_id: int):
    for u in USERS:
        if u["id"] == user_id:
            return {"id": u["id"], "nombre": u["name"]}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
