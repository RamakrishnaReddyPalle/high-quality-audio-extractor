# app\api\routes\download.py

from fastapi import (
    APIRouter,
    HTTPException
)

from app.models.request_models import (
    DownloadRequest
)

from app.services.yt_dlp_service import (
    YTDLPService
)

from app.utils.validators import (
    validate_youtube_url
)

router = APIRouter()


@router.post("/")
def download_audio(
    request: DownloadRequest
):

    if not validate_youtube_url(
        request.url
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )

    try:

        result = (
            YTDLPService.download_best_audio(
                request.url
            )
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )