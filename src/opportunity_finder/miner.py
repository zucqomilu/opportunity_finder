from dataclasses import dataclass
from pathlib import Path

from opportunity_finder.state import is_post_seen


@dataclass(frozen=True)
class Match:
    phrase: str
    title: str
    url: str
    subreddit: str
    score: int


def extract_match(submission, phrase: str) -> Match:
    return Match(
        phrase=phrase,
        title=submission.title,
        url=submission.url,
        subreddit=submission.subreddit.display_name,
        score=submission.score,
    )


def search_subreddit(subreddit, phrases: list[str], db_path: Path, min_score: int):
    matches = []
    for submission in subreddit.new(limit=100):
        if is_post_seen(db_path, submission.id):
            continue
        if submission.score < min_score:
            continue
        text = f"{submission.title} {submission.selftext}".lower()
        if any(phrase.lower() in text for phrase in phrases):
            matches.append(submission)
    return matches
