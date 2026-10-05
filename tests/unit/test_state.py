import sqlite3

import pytest

from opportunity_finder.state import init_db, is_post_seen, mark_post_seen


@pytest.mark.unit
def test_init_db_creates_expected_tables_on_fresh_database_file(tmp_path):
    db_path = tmp_path / "state.db"

    init_db(db_path)

    with sqlite3.connect(db_path) as conn:
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }

    assert "seen_posts" in tables


@pytest.mark.unit
def test_mark_post_seen_then_is_post_seen_returns_true(tmp_path):
    db_path = tmp_path / "state.db"
    init_db(db_path)

    mark_post_seen(db_path, "abc123")

    assert is_post_seen(db_path, "abc123") is True


@pytest.mark.unit
def test_is_post_seen_returns_false_for_an_unseen_post_id(tmp_path):
    db_path = tmp_path / "state.db"
    init_db(db_path)

    assert is_post_seen(db_path, "never-marked") is False
