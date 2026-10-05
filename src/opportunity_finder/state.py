import sqlite3
from pathlib import Path


def init_db(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS seen_posts (post_id TEXT PRIMARY KEY)"
        )


def mark_post_seen(db_path: Path, post_id: str) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO seen_posts (post_id) VALUES (?)", (post_id,)
        )


def is_post_seen(db_path: Path, post_id: str) -> bool:
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT 1 FROM seen_posts WHERE post_id = ?", (post_id,)
        ).fetchone()
    return row is not None
