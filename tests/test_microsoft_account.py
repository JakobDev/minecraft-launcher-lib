import minecraft_launcher_lib
import pytest


def test_get_login_url():
    state = minecraft_launcher_lib.microsoft_account.generate_state()
    code_verifier, code_challenge, code_challenge_method = minecraft_launcher_lib.microsoft_account.generate_pkce()
    login_url = minecraft_launcher_lib.microsoft_account.get_login_url("CLIENT_ID", "REDIRECT_URL", state, code_challenge, code_challenge_method)

    assert code_verifier is not None
    assert login_url is not None


def test_url_contains_auth_code():
    assert minecraft_launcher_lib.microsoft_account.url_contains_auth_code("https://login.live.com/oauth20_desktop.srf?code=testcode&lc=test") is True
    assert minecraft_launcher_lib.microsoft_account.url_contains_auth_code("https://example.com") is False


def test_get_auth_code_from_url():
    assert minecraft_launcher_lib.microsoft_account.get_auth_code_from_url("https://login.live.com/oauth20_desktop.srf?code=testcode&lc=test") == "testcode"


def test_complete_refresh_invalid_token():
    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidRefreshToken):
        minecraft_launcher_lib.microsoft_account.complete_refresh("CLIENT_ID", "REFRESH_TOKEN")
