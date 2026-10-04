import tomllib
from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseModel


class Settings(BaseModel):
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    target_subreddits: list[str]
    pain_point_phrases: list[str]
    min_score: int = 1


def load_settings(env_path: Path, config_path: Path) -> Settings:
    env_values = {k.lower(): v for k, v in dotenv_values(env_path).items()}
    with open(config_path, "rb") as config_file:
        config_values = tomllib.load(config_file)
    return Settings(**env_values, **config_values)
