from pathlib import Path


def write_candidate_entry(
    org_path: Path,
    title: str,
    url: str,
    subreddit: str,
    score: int,
    phrase: str,
) -> None:
    if not org_path.exists():
        org_path.write_text("#+TODO: TODO DONE\n")

    with open(org_path, "a") as org_file:
        org_file.write(
            f"* TODO {title}\n"
            "  :PROPERTIES:\n"
            f"  :PHRASE: {phrase}\n"
            f"  :URL: {url}\n"
            f"  :SUBREDDIT: {subreddit}\n"
            f"  :SCORE: {score}\n"
            "  :END:\n"
        )
