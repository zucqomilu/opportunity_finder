import pytest
from pydantic import ValidationError

from opportunity_finder.config import load_settings


@pytest.mark.unit
def test_load_settings_raises_on_missing_reddit_credentials(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text("")

    config_path = tmp_path / "config.toml"
    config_path.write_text(
        'target_subreddits = ["SomebodyMakeThis"]\n'
        'pain_point_phrases = ["is there a tool that"]\n'
    )

    with pytest.raises(ValidationError, match="reddit_client_id"):
        load_settings(env_path=env_path, config_path=config_path)


@pytest.mark.unit
def test_load_settings_loads_subreddits_and_phrases_from_config_file(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text(
        "REDDIT_CLIENT_ID=abc123\n"
        "REDDIT_CLIENT_SECRET=secret\n"
        "REDDIT_USER_AGENT=opportunity-finder/0.1\n"
    )

    config_path = tmp_path / "config.toml"
    config_path.write_text(
        'target_subreddits = ["SomebodyMakeThis", "InternetIsBeautiful"]\n'
        'pain_point_phrases = ["is there a tool that", "I wish there was an app for"]\n'
    )

    settings = load_settings(env_path=env_path, config_path=config_path)

    assert settings.target_subreddits == ["SomebodyMakeThis", "InternetIsBeautiful"]
    assert settings.pain_point_phrases == [
        "is there a tool that",
        "I wish there was an app for",
    ]
