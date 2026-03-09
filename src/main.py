import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings import config_loader
from dotenv import load_dotenv
from src.routers import user


def create_app() -> FastAPI:
    app = FastAPI(
        title="PlayPulse",
        version="0.0.1",
    )

    # === Middleware ===
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # === Роутеры ===
    app.include_router(user.router)

    return app


app = create_app()
load_dotenv()


def run() -> None:
    host = config_loader("FASTAPI_HOST")
    port = int(config_loader("FASTAPI_PORT"))
    reload = str(config_loader("FASTAPI_RELOAD")).lower() == "true"

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    run()
