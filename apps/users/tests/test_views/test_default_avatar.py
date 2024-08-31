from http import HTTPStatus

import requests


def test_leaderboard_view() -> None:
    """Ensure that path for default avatar exists."""
    avatar_url = (
        "https://avatar.iran.liara.run/username?username=test"
        "&background=800000&color=FFFFFF&length=1"
    )
    response = requests.get(avatar_url, timeout=10)
    assert response.status_code == HTTPStatus.OK
    assert "image" in response.headers.get("Content-Type", "")
