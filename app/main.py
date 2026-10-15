from fastapi import FastAPI

from . import v1, v2

app = FastAPI(
    title="Demo: versionado de APIs",
    description=(
        "Misma lista de usuarios servida en dos versiones.\n\n"
        "- **v1** (deprecada): campo `nombre`.\n"
        "- **v2** (actual): campo `fullName` + `email`, y permite crear usuarios."
    ),
    version="2.0.0",
)

# Cada versión es un "router" con su prefijo (/v1, /v2). Conviven en la misma app.
app.include_router(v1.router)
app.include_router(v2.router)


@app.get("/", tags=["inicio"], summary="Página de bienvenida")
def inicio():
    return {
        "mensaje": "API de demo. Abre /docs para ver Swagger.",
        "versiones": ["/v1/users (deprecada)", "/v2/users (actual)"],
    }
