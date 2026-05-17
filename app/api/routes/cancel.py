# app\api\routes\cancel.py

from fastapi import APIRouter

from app.core.progress_tracker import (
    progress_data
)

from app.utils.process_registry import (
    active_processes
)

router = APIRouter()


@router.post("/")
def cancel_processing():

    progress_data["cancelled"] = True

    for process in active_processes.values():

        try:
            process.kill()

        except Exception:
            pass

    active_processes.clear()

    progress_data["status"] = "cancelled"

    progress_data["message"] = (
        "Processing cancelled"
    )

    progress_data["active"] = False

    return {
        "status": "cancelled"
    }