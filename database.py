
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "complaints.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                complaint TEXT NOT NULL,
                category TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                priority TEXT NOT NULL,
                summary TEXT NOT NULL,
                resolution TEXT NOT NULL,
                reply TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_complaint(complaint: str, result: dict):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO complaints (
                complaint, category, sentiment, priority,
                summary, resolution, reply
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            complaint,
            result["category"],
            result["sentiment"],
            result["priority"],
            result["summary"],
            result["resolution"],
            result["reply"],
        ))


def get_complaint_history(limit: int = 100):
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT *
            FROM complaints
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]
