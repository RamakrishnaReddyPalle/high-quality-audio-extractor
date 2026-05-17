# app/api/routes/playlist.py

from fastapi import APIRouter

from app.services.yt_dlp_service import YTDLPService

router = APIRouter()


@router.get("/")
def get_playlist_entries(url: str):

    entries = (
        YTDLPService.fetch_playlist_entries(url)
    )

    return {
        "count": len(entries),
        "entries": entries
    }