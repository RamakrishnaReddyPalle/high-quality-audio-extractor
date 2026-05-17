# app\api\main.py

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.metadata import router as metadata_router
from app.api.routes.download import router as download_router
from app.api.routes.conversion import router as conversion_router
from app.api.routes.progress import router as progress_router
from app.api.routes.playlist import router as playlist_router

from app.api.routes.serve import (
    router as serve_router
)

from app.api.routes.cancel import (
    router as cancel_router
)


app = FastAPI(
    title="High Quality Audio Extractor"
)

app.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)

app.include_router(
    metadata_router,
    prefix="/metadata",
    tags=["Metadata"]
)

app.include_router(
    download_router,
    prefix="/download",
    tags=["Download"]
)

app.include_router(
    conversion_router,
    prefix="/convert",
    tags=["Conversion"]
)

app.include_router(
    progress_router,
    prefix="/progress",
    tags=["Progress"]
)

app.include_router(
    playlist_router,
    prefix="/playlist",
    tags=["Playlist"]
)

app.include_router(
    serve_router,
    prefix="/serve",
    tags=["Serve"]
)

app.include_router(
    cancel_router,
    prefix="/cancel",
    tags=["Cancel"]
)