from fastapi import FastAPI
from uvicorn import run

from .utils import lifespan
from .routes import users_router, admin_router


app = FastAPI(lifespan=lifespan, docs_url="/", redoc_url=None,)
app.router.prefix = "/api/v1"
app.include_router(router=users_router)
app.include_router(router=admin_router)


if __name__ == "__main__":
    run(app=app, host="127.0.0.1", port=8000)
