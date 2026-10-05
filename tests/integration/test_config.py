import pytest

from opportunity_finder.config import load_settings


@pytest.mark.integration
def test_load_settings_end_to_end_from_sample_env_and_config_files(tmp_path):
    env_path = tmp_path / ".env"
    env_path.write_text(
        "REDDIT_CLIENT_ID=sample-client-id\n"
        "REDDIT_CLIENT_SECRET=sample-client-secret\n"
        "REDDIT_USER_AGENT=opportunity-finder/0.1 by u/sample\n"
    )

    config_path = tmp_path / "config.toml"
    config_path.write_text(
        'target_subreddits = ["SomebodyMakeThis", "InternetIsBeautiful", "SideProject"]\n'
        'pain_point_phrases = [\n'
        '    "is there a tool that",\n'
        '    "I wish there was an app for",\n'
        '    "does anyone know a website that",\n'
        ']\n'
        "min_score = 10\n"
    )

    settings = load_settings(env_path=env_path, config_path=config_path)

    assert settings.reddit_client_id == "sample-client-id"
    assert settings.reddit_client_secret == "sample-client-secret"
    assert settings.reddit_user_agent == "opportunity-finder/0.1 by u/sample"
    assert settings.target_subreddits == [
        "SomebodyMakeThis",
        "InternetIsBeautiful",
        "SideProject",
    ]
    assert settings.pain_point_phrases == [
        "is there a tool that",
        "I wish there was an app for",
        "does anyone know a website that",
    ]
    assert settings.min_score == 10
