import orgparse
import pytest

from opportunity_finder.org_sync import write_candidate_entry


@pytest.mark.integration
def test_write_candidate_entry_end_to_end_produces_valid_org_syntax(tmp_path):
    org_path = tmp_path / "candidates.org"

    write_candidate_entry(
        org_path,
        title="Is there a tool that tracks my expenses?",
        url="https://reddit.com/r/SomebodyMakeThis/comments/abc123",
        subreddit="SomebodyMakeThis",
        score=42,
        phrase="is there a tool that",
    )

    root = orgparse.load(str(org_path))
    children = root.children

    assert len(children) == 1
    entry = children[0]
    assert entry.todo == "TODO"
    assert entry.heading == "Is there a tool that tracks my expenses?"
    assert entry.properties["PHRASE"] == "is there a tool that"
    assert (
        entry.properties["URL"]
        == "https://reddit.com/r/SomebodyMakeThis/comments/abc123"
    )
    assert entry.properties["SUBREDDIT"] == "SomebodyMakeThis"
    assert entry.properties["SCORE"] == "42"
