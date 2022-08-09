import minecraft_launcher_lib
import pytest


def test_get_login_url():
    login_url = minecraft_launcher_lib.microsoft_account.get_login_url("CLIENT_ID", "REDIRECT_URL")
    assert login_url is not None


def test_generate_state():
    assert isinstance(minecraft_launcher_lib.microsoft_account.generate_state(), str)


def test_get_secure_login_data():
    login_url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data("CLIENT_ID", "REDIRECT_URL")

    assert login_url is not None
    assert state is not None
    assert code_verifier is not None


def test_parse_auth_code_url():
    test_state = "123456"
    test_code = "abcxyz"

    auth_code = minecraft_launcher_lib.microsoft_account.parse_auth_code_url(f"http://127.0.0.1:3003?code={test_code}&state={test_state}", test_state)
    assert auth_code == test_code


def test_complete_refresh_invalid_token():
    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidRefreshToken):
        minecraft_launcher_lib.microsoft_account.complete_refresh("CLIENT_ID", "CLIENT_SECRET", None, "REFRESH_TOKEN")
