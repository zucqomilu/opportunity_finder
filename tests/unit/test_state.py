import sqlite3

import pytest

from opportunity_finder.state import init_db


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
