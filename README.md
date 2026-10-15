# Demo: versionado de APIs con FastAPI

Proyecto pequeño para la píldora **"Versionado de APIs y gestión de endpoints"**.
Una misma lista de usuarios se sirve en **dos versiones a la vez** (`/v1` y `/v2`), y la v1 está marcada como **deprecada**.

| Versión | Estado | Campos | Qué se puede hacer |
|---|---|---|---|
| `v1` | deprecada | `id`, `nombre` | solo leer (GET) |
| `v2` | actual | `id`, `fullName`, `email` | leer (GET) y crear (POST) |

> Cambiar `nombre` por `fullName` es un **breaking change**: por eso existe la v2.
> Añadir `email` **no** rompe nada: solo suma.

---

## 1. Requisitos

- Python 3.10 o superior (`python --version`)
- (Opcional) [Postman](https://www.postman.com/downloads/)

## 2. Instalación

```bash
# desde la carpeta del proyecto
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## 3. Arrancar la API

```bash
uvicorn app.main:app --reload
```

Verás algo como `Uvicorn running on http://127.0.0.1:8000`. Déjalo abierto en esa terminal.

## 4. Probarla

### Con Swagger (lo más fácil, sin instalar nada más)

1. Abre <http://127.0.0.1:8000/docs>
2. Despliega un endpoint → **Try it out** → **Execute**
3. Fíjate en que los endpoints de la **v1 salen tachados** (deprecated) y los de la **v2** no.

### Con Postman

1. **Import** → selecciona `postman/api-versioning.postman_collection.json`
2. Ejecuta las peticiones 1 a 7 (botón **Send**), o todas de golpe con clic derecho en la colección → **Run collection**.
3. En la respuesta de la petición 1, abre la pestaña **Headers**: verás `Deprecation`, `Sunset` y `Link`.
4. Las pestañas **Test Results** muestran si cada comprobación pasa.

### Con curl

```bash
curl -i http://127.0.0.1:8000/v1/users      # -i muestra las cabeceras
curl    http://127.0.0.1:8000/v2/users
curl -X POST http://127.0.0.1:8000/v2/users \
     -H "Content-Type: application/json" \
     -d '{"fullName": "Marie", "email": "marie@example.com"}'
```

## 5. Endpoints

| Método | Ruta | Respuesta |
|---|---|---|
| GET | `/v1/users` | `200` lista con `nombre` (+ cabeceras de deprecación) |
| GET | `/v1/users/{id}` | `200` usuario / `404` si no existe |
| GET | `/v2/users` | `200` lista con `fullName` y `email` |
| GET | `/v2/users/{id}` | `200` usuario / `404` si no existe |
| POST | `/v2/users` | `201` usuario creado |

## 6. Tests

```bash
pytest
```

Deberían pasar los 7 tests (`7 passed`).

## 7. Estructura

```
app/
  main.py   # crea la app y registra las dos versiones
  v1.py     # versión 1 (deprecada, con cabeceras de aviso)
  v2.py     # versión 2 (actual)
  data.py   # "base de datos" de mentira (una lista)
tests/test_api.py
postman/api-versioning.postman_collection.json
```

## 8. Para practicar

1. **Fácil:** añade un usuario más en `app/data.py` y comprueba que aparece en v1 y en v2.
2. **Fácil:** cambia la fecha de `Sunset` en `app/v1.py` y mira la cabecera en Postman.
3. **Medio:** añade `GET /v2/users/{id}/email` que devuelva solo el email.
4. **Medio:** crea una `v3` donde `fullName` se separe en `firstName` y `lastName`. ¿Es un breaking change? ¿Qué pasa con v1 y v2?
5. **Reto:** en vez de versionar por URL, versiona por cabecera (`X-API-Version: 2`) en un solo endpoint `/users`.

## 9. Subirlo a GitHub

```bash
git init
git add .
git commit -m "Demo de versionado de APIs con FastAPI"
git branch -M main
git remote add origin https://github.com/TU_USUARIO//Versionado-de-APIs-y-gestion-de-endpoints.git
git push -u origin main
```
