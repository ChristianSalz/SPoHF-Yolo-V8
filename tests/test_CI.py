import os

import os
import requests
import pytest

@pytest.mark.smoke
def test_github_actions_minutes():
    """
    Smoke test for GitHub Actions workflow.
    """
    # Read token from environment
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        pytest.skip("GITHUB_TOKEN not set, skipping check")

    headers = {"Authorization": f"token {token}"}

    # Get the authenticated user's login
    user_resp = requests.get("https://api.github.com/user", headers=headers)
    assert user_resp.status_code == 200, "Failed to get authenticated user"
    username = user_resp.json()["login"]

    # Query Actions usage for the user
    url = f"https://api.github.com/users/{username}/actions/usage"
    usage_resp = requests.get(url, headers=headers)
    assert usage_resp.status_code == 200, f"Failed to query Actions usage for {username}"

    data = usage_resp.json()
    remaining_minutes = data.get("included_minutes", 0) - data.get("minutes_used", 0)

    assert remaining_minutes > 0, f"No GitHub Actions minutes left! Remaining: {remaining_minutes}"

#Check weights
def test_weights_file_exists():
    path = "Best-Model-Weights/weights-nano.zip"
    assert os.path.isfile(path), f"{path} does not exist"

#Check structure
def test_required_folders_exist():
    required = [
        "Best-Model-Weights",
        "train",
        "tests",
        "valid"
    ]
    for folder in required:
        assert os.path.isdir(folder), f"{folder} is missing"

