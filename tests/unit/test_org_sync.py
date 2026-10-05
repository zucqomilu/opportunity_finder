import pytest

from opportunity_finder.org_sync import write_candidate_entry


@pytest.mark.unit
def test_write_candidate_entry_appends_new_todo_heading_with_post_title(tmp_path):
    org_path = tmp_path / "candidates.org"
    org_path.write_text("#+TODO: TODO DONE\n")

    write_candidate_entry(
        org_path,
        title="Is there a tool that tracks my expenses?",
        url="https://reddit.com/r/SomebodyMakeThis/comments/abc123",
        subreddit="SomebodyMakeThis",
        score=42,
        phrase="is there a tool that",
    )

    content = org_path.read_text()
    assert "* TODO Is there a tool that tracks my expenses?" in content
