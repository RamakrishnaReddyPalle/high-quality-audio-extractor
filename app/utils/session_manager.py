# app\utils\session_manager.py

import threading
import time

from pathlib import Path

from app.utils.cleanup import (
    cleanup_directory
)


class SessionManager:

    @staticmethod
    def cleanup_session_after_delay(
        session_dir: str,
        delay: int = 300
    ):

        def delayed_cleanup():

            time.sleep(delay)

            cleanup_directory(
                session_dir
            )

            print(
                f"Cleaned session: "
                f"{session_dir}"
            )

        thread = threading.Thread(
            target=delayed_cleanup,
            daemon=True
        )

        thread.start()

    @staticmethod
    def cleanup_stale_sessions(
        temp_dir: str,
        max_age_hours: int = 2
    ):

        now = time.time()

        temp_path = Path(temp_dir)

        if not temp_path.exists():
            return

        for session_dir in temp_path.iterdir():

            if not session_dir.is_dir():
                continue

            age_seconds = (
                now
                - session_dir.stat().st_mtime
            )

            if (
                age_seconds
                > max_age_hours * 3600
            ):

                cleanup_directory(
                    str(session_dir)
                )

                print(
                    f"Removed stale session: "
                    f"{session_dir}"
                )