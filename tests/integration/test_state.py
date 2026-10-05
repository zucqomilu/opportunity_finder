import subprocess
import sys

import pytest


@pytest.mark.integration
def test_state_persists_across_process_restarts(tmp_path):
    db_path_repr = repr(str(tmp_path / "state.db"))

    subprocess.run(
        [
            sys.executable,
            "-c",
            "from opportunity_finder.state import init_db, mark_post_seen; "
            f"init_db({db_path_repr}); mark_post_seen({db_path_repr}, 'persisted-post')",
        ],
        check=True,
    )

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from opportunity_finder.state import is_post_seen; "
            f"print(is_post_seen({db_path_repr}, 'persisted-post'))",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == "True"
