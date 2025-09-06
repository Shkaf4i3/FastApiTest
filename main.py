from fastapi import FastAPI
from uvicorn import run

from api_v1.lifespan import lifespan
from api_v1.users.views import router


app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    run("main:app", reload=True)
