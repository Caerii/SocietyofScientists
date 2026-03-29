"""Database models and session persistence."""

import json
import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from pathlib import Path

logger = logging.getLogger(__name__)


class SessionDB:
    """SQLite database for session persistence."""

    def __init__(self, db_path: str = "society_of_scientists/data/sessions.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        """Get database connection with row factory."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def _get_cursor(self):
        """Context manager for database cursor."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}", exc_info=True)
            raise
        finally:
            conn.close()

    def _init_db(self):
        """Initialize database schema."""
        with self._get_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    task TEXT NOT NULL,
                    status TEXT NOT NULL,
                    running INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    completed_at TEXT,
                    stopped_at TEXT,
                    error TEXT,
                    conversation TEXT,
                    proposal TEXT
                )
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_status ON sessions(status)
            """)

    def save_session(self, session: Dict[str, Any]) -> bool:
        """Save or update a session in the database."""
        try:
            conversation_json = json.dumps(session.get("conversation", []))

            with self._get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO sessions 
                    (id, task, status, running, created_at, completed_at, stopped_at, error, conversation, proposal)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        session["id"],
                        session["task"],
                        session.get("status", "running"),
                        1 if session.get("running") else 0,
                        session["created_at"],
                        session.get("completed_at"),
                        session.get("stopped_at"),
                        session.get("error"),
                        conversation_json,
                        session.get("proposal", ""),
                    ),
                )
            return True
        except Exception as e:
            logger.error(
                f"Failed to save session {session.get('id')}: {e}", exc_info=True
            )
            return False

    def update_session_status(
        self, session_id: str, status: str, error: Optional[str] = None
    ) -> bool:
        """Update session status and optionally error message."""
        try:
            completed_at = datetime.now().isoformat() if status == "completed" else None
            stopped_at = datetime.now().isoformat() if status == "stopped" else None

            with self._get_cursor() as cursor:
                if error:
                    cursor.execute(
                        """
                        UPDATE sessions 
                        SET status = ?, running = 0, error = ?, completed_at = ?, stopped_at = ?
                        WHERE id = ?
                    """,
                        (status, error, completed_at, stopped_at, session_id),
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE sessions 
                        SET status = ?, running = 0, completed_at = ?, stopped_at = ?
                        WHERE id = ?
                    """,
                        (status, completed_at, stopped_at, session_id),
                    )
            return True
        except Exception as e:
            logger.error(f"Failed to update session {session_id}: {e}", exc_info=True)
            return False

    def update_conversation(
        self, session_id: str, conversation: List[Dict[str, Any]]
    ) -> bool:
        """Update session conversation."""
        try:
            conversation_json = json.dumps(conversation)
            with self._get_cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE sessions 
                    SET conversation = ?
                    WHERE id = ?
                """,
                    (conversation_json, session_id),
                )
            return True
        except Exception as e:
            logger.error(
                f"Failed to update conversation for session {session_id}: {e}",
                exc_info=True,
            )
            return False

    def update_proposal(self, session_id: str, proposal: str) -> bool:
        """Update session proposal text."""
        try:
            with self._get_cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE sessions 
                    SET proposal = ?
                    WHERE id = ?
                """,
                    (proposal, session_id),
                )
            return True
        except Exception as e:
            logger.error(
                f"Failed to update proposal for session {session_id}: {e}",
                exc_info=True,
            )
            return False

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID."""
        try:
            with self._get_cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM sessions WHERE id = ?
                """,
                    (session_id,),
                )
                row = cursor.fetchone()

                if row:
                    return {
                        "id": row["id"],
                        "task": row["task"],
                        "status": row["status"],
                        "running": bool(row["running"]),
                        "created_at": row["created_at"],
                        "completed_at": row["completed_at"],
                        "stopped_at": row["stopped_at"],
                        "error": row["error"],
                        "conversation": json.loads(row["conversation"])
                        if row["conversation"]
                        else [],
                        "proposal": row["proposal"] or "",
                    }
        except Exception as e:
            logger.error(f"Failed to retrieve session {session_id}: {e}", exc_info=True)
        return None

    def list_sessions(
        self, status: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List sessions, optionally filtered by status."""
        try:
            with self._get_cursor() as cursor:
                if status:
                    cursor.execute(
                        """
                        SELECT id, task, status, running, created_at, completed_at
                        FROM sessions 
                        WHERE status = ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    """,
                        (status, limit),
                    )
                else:
                    cursor.execute(
                        """
                        SELECT id, task, status, running, created_at, completed_at
                        FROM sessions 
                        ORDER BY created_at DESC
                        LIMIT ?
                    """,
                        (limit,),
                    )

                sessions = []
                for row in cursor.fetchall():
                    sessions.append(
                        {
                            "id": row["id"],
                            "task": row["task"],
                            "status": row["status"],
                            "running": bool(row["running"]),
                            "created_at": row["created_at"],
                            "completed_at": row["completed_at"],
                        }
                    )
                return sessions
        except Exception as e:
            logger.error(f"Failed to list sessions: {e}", exc_info=True)
            return []

    def delete_session(self, session_id: str) -> bool:
        """Delete a session from the database."""
        try:
            with self._get_cursor() as cursor:
                cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {e}", exc_info=True)
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get session statistics."""
        try:
            with self._get_cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN running = 1 THEN 1 ELSE 0 END) as running,
                        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                        SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errors
                    FROM sessions
                """)
                row = cursor.fetchone()

                return {
                    "total_sessions": row["total"],
                    "active_sessions": row["running"],
                    "completed_sessions": row["completed"],
                    "error_sessions": row["errors"],
                }
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}", exc_info=True)
            return {
                "total_sessions": 0,
                "active_sessions": 0,
                "completed_sessions": 0,
                "error_sessions": 0,
            }


# Global database instance
_db_instance: Optional[SessionDB] = None


def get_session_db() -> SessionDB:
    """Get or create global database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = SessionDB()
    return _db_instance
