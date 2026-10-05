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


@pytest.mark.unit
def test_write_candidate_entry_includes_phrase_url_subreddit_and_score_as_properties(
    tmp_path,
):
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
    assert ":PHRASE: is there a tool that" in content
    assert ":URL: https://reddit.com/r/SomebodyMakeThis/comments/abc123" in content
    assert ":SUBREDDIT: SomebodyMakeThis" in content
    assert ":SCORE: 42" in content


@pytest.mark.unit
def test_write_candidate_entry_creates_org_file_with_todo_header_if_missing(tmp_path):
    org_path = tmp_path / "candidates.org"

    write_candidate_entry(
        org_path,
        title="Is there a tool that tracks my expenses?",
        url="https://reddit.com/r/SomebodyMakeThis/comments/abc123",
        subreddit="SomebodyMakeThis",
        score=42,
        phrase="is there a tool that",
    )

    content = org_path.read_text()
    assert content.startswith("#+TODO: TODO DONE\n")


@pytest.mark.unit
def test_write_candidate_entry_appends_without_altering_existing_entries(tmp_path):
    org_path = tmp_path / "candidates.org"
    existing_content = (
        "#+TODO: TODO DONE\n"
        "* TODO Does anyone know a website that tracks garden chores?\n"
        "  :PROPERTIES:\n"
        "  :PHRASE: does anyone know a website that\n"
        "  :URL: https://reddit.com/r/SideProject/comments/xyz789\n"
        "  :SUBREDDIT: SideProject\n"
        "  :SCORE: 7\n"
        "  :END:\n"
    )
    org_path.write_text(existing_content)

    write_candidate_entry(
        org_path,
        title="Is there a tool that tracks my expenses?",
        url="https://reddit.com/r/SomebodyMakeThis/comments/abc123",
        subreddit="SomebodyMakeThis",
        score=42,
        phrase="is there a tool that",
    )

    content = org_path.read_text()
    assert content.startswith(existing_content)
    assert "* TODO Is there a tool that tracks my expenses?" in content
