"""Base de datos de mentira: una lista en memoria.

Los datos son siempre los mismos. Lo que cambia entre v1 y v2 es el
"contrato": cómo se los enseñamos al cliente.
"""

USERS = [
    {"id": 1, "name": "Eva", "email": "eva@example.com"},
    {"id": 2, "name": "David", "email": "david@example.com"},
    {"id": 3, "name": "Laura", "email": "laura@example.com"},
]


def siguiente_id() -> int:
    return max(u["id"] for u in USERS) + 1
