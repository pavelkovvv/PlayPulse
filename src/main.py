import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings import config_loader


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

    # === Healthcheck ===
    @app.get("/health", tags=["system"])
    async def healthcheck():
        return {"status": "ok"}

    return app


app = create_app()


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
