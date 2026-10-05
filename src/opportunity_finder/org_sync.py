from pathlib import Path


def write_candidate_entry(
    org_path: Path,
    title: str,
    url: str,
    subreddit: str,
    score: int,
    phrase: str,
) -> None:
    with open(org_path, "a") as org_file:
        org_file.write(f"* TODO {title}\n")
