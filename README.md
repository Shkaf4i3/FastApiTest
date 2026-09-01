# FastAPI CRUD Template

REST API for user CRUD with JWT cookie auth for an admin. Learning template: layered services, SQLAlchemy, pytest.

**Stack:** Python 3.13, FastAPI, SQLAlchemy 2 (asyncpg), Pydantic, PyJWT, bcrypt, pytest, Docker, uv.

## Local run

1. Create a PostgreSQL database (and a separate DB for tests).
2. Copy `.env.example` to `.env`.
3. Run:

```bash
uv sync
uv run fastapi dev ./src/main.py
```

Schema and the bootstrap admin are created on startup (`src/utils/lifespan.py`).

## Docker

```bash
cp .env.example .env
docker compose up
```

Compose starts `app` (`8000`) and PostgreSQL. Override `dsn` inside the compose network as needed.

## Configuration

| Variable | Description |
|---|---|
| `dsn` | App DSN: `postgresql+asyncpg://...` |
| `test_dsn` | Test DSN (pytest / CI) |
| `admin_login` | Admin username (seeded on first start) |
| `admin_password` | Admin password (stored hashed) |
| `jwt_key` | JWT signing secret |
| `jwt_algorithm` | JWT algorithm (e.g. `HS256`) |

`.env` is gitignored.

## Architecture

- FastAPI app, prefix `/api/v1`.
- PostgreSQL: `Users`, `Admin`.
- Auth: `POST /api/v1/admin/auth/token` (OAuth2 form) → HttpOnly `access_token` cookie (`secure`, `samesite=lax`, 1h).
- User routes require a valid admin JWT.

Layout: `src/` (routes, service, repo, dto, model, deps, core), `tests/`, `Dockerfile`, `docker-compose.yaml`, `.github/workflows/ci.yml`.

## Features

- CRUD: create / get by email / list / delete / patch status (`user` \| `support`).
- Pydantic DTOs (`EmailStr`), HTTP error mapping.
- Admin password hashing (bcrypt).
- pytest + pytest-asyncio against `test_dsn`.
- CI: GitHub Actions on `main` — `uv sync` + `uv run pytest ./tests/crud_tests.py` with a Postgres service.

## Tests

```bash
uv run pytest ./tests/crud_tests.py
```

## Links

- Swagger UI: `http://localhost:8000/` (`docs_url="/"`).
- Auth: `POST /api/v1/admin/auth/token`.
- Users: `/api/v1/users/...`.
