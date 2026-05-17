# app\api\routes\metadata.py

from fastapi import APIRouter, HTTPException

from app.services.yt_dlp_service import YTDLPService
from app.utils.validators import validate_youtube_url

router = APIRouter()


@router.get("/")
def get_metadata(url: str):

    if not validate_youtube_url(url):
        raise HTTPException(
            status_code=400,
            detail="Invalid YouTube URL"
        )

    try:
        info = YTDLPService.fetch_metadata(url)

        formats = []

        for fmt in info.get("formats", []):

            if fmt.get("vcodec") == "none":

                formats.append({
                    "format_id": fmt.get("format_id"),
                    "ext": fmt.get("ext"),
                    "acodec": fmt.get("acodec"),
                    "abr": fmt.get("abr")
                })

        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "thumbnail": info.get("thumbnail"),
            "formats": formats
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )