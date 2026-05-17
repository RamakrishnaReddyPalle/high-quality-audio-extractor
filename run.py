# run.py

import uvicorn

from app.utils.session_manager import (
    SessionManager
)

from app.core.config import TEMP_DIR

SessionManager.cleanup_stale_sessions(
    temp_dir=str(TEMP_DIR),
    max_age_hours=2
)

if __name__ == "__main__":

    uvicorn.run(
        "app.api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )