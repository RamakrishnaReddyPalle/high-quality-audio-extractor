# app/api/routes/progress.py

from fastapi import APIRouter

from app.core.progress_tracker import progress_data

router = APIRouter()


@router.get("/")
def get_progress():

    return progress_data