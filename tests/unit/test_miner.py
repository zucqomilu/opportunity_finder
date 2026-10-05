from types import SimpleNamespace

import pytest

from opportunity_finder.miner import search_subreddit
from opportunity_finder.state import init_db, mark_post_seen


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


@pytest.mark.unit
def test_search_subreddit_excludes_posts_already_marked_seen(tmp_path):
    db_path = tmp_path / "state.db"
    init_db(db_path)

    seen = _submission("1", "Is there a tool that tracks my expenses?")
    unseen = _submission("2", "Is there a tool that tracks my sleep?")
    mark_post_seen(db_path, seen.id)
    subreddit = SimpleNamespace(new=lambda limit: [seen, unseen])

    results = search_subreddit(
        subreddit, phrases=["is there a tool that"], db_path=db_path, min_score=0
    )

    assert results == [unseen]


@pytest.mark.unit
def test_search_subreddit_excludes_posts_below_minimum_score(tmp_path):
    db_path = tmp_path / "state.db"
    init_db(db_path)

    low_score = _submission(
        "1", "Is there a tool that tracks my expenses?", score=2
    )
    high_score = _submission(
        "2", "Is there a tool that tracks my sleep?", score=20
    )
    subreddit = SimpleNamespace(new=lambda limit: [low_score, high_score])

    results = search_subreddit(
        subreddit, phrases=["is there a tool that"], db_path=db_path, min_score=10
    )

    assert results == [high_score]
