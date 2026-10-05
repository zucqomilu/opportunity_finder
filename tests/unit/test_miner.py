from types import SimpleNamespace

import pytest

from opportunity_finder.miner import search_subreddit
from opportunity_finder.state import init_db


def _submission(id, title, selftext="", score=10):
    return SimpleNamespace(id=id, title=title, selftext=selftext, score=score)


@pytest.mark.unit
def test_search_subreddit_returns_matching_posts_for_a_configured_phrase(tmp_path):
    db_path = tmp_path / "state.db"
    init_db(db_path)

    matching = _submission("1", "Is there a tool that tracks my expenses?")
    non_matching = _submission("2", "What's your favorite recipe?")
    subreddit = SimpleNamespace(new=lambda limit: [matching, non_matching])

    results = search_subreddit(
        subreddit, phrases=["is there a tool that"], db_path=db_path, min_score=0
    )

    assert results == [matching]
