# app\api\routes\serve.py

from pathlib import Path

from fastapi import (
    APIRouter,
    HTTPException
)

from fastapi.responses import (
    FileResponse
)

from app.utils.session_manager import (
    SessionManager
)

from app.core.logger import logger

router = APIRouter()


@router.get("/")
def serve_file(path: str):

    file_path = Path(path)

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    session_dir = str(
        file_path.parent
    )

    logger.info(
        f"Serving file: "
        f"{file_path.name}"
    )

    # =====================================
    # AGGRESSIVE FREE-TIER CLEANUP
    # =====================================

    SessionManager.cleanup_session_after_delay(
        session_dir=session_dir,
        delay=90
    )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream"
    )