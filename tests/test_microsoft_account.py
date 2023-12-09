import minecraft_launcher_lib
from typing import Any
import requests
import pytest


class MicrosoftRequestsResponseMock:
    def __init__(self, code, data: Any) -> None:
        self._data = data
        self.code = code

    def json(self) -> Any:
        return self._data


class MicrosoftRequestsMock:
    def __init__(self, mode: str) -> None:
        self._mode = mode

    def get(self, url: str, **kwargs: dict) -> MicrosoftRequestsResponseMock:
        if url == "https://api.minecraftservices.com/minecraft/profile":
            if kwargs["headers"]["Authorization"] != "Bearer minecraft_access_token":
                return MicrosoftRequestsResponseMock(500, {})

            if self._mode == "not_own_minecraft":
                return MicrosoftRequestsResponseMock(400, {"error": "NOT_FOUND", "errorMessage": "Not Found"})

            return MicrosoftRequestsResponseMock(200, {"id": "minecraft_uuid", "name": "minecraft_name", "skins": [], "capes": []})

        elif url == "https://api.minecraftservices.com/entitlements/mcstore":
            if kwargs["headers"]["Authorization"] != "Bearer minecraft_access_token":
                return MicrosoftRequestsResponseMock(500, {})

            return MicrosoftRequestsResponseMock(200, {"items": [], "signature": "jwt sig", "keyId": "1"})
        else:
            raise ValueError(f"Invalid GET URL {url}")

    def post(self, url: str, **kwargs: dict) -> MicrosoftRequestsResponseMock:
        if url == "https://login.microsoftonline.com/consumers/oauth2/v2.0/token":
            return MicrosoftRequestsResponseMock(200, {"access_token": "test_access_token", "token_type": "Bearer", "expires_in": 0, "scope": "", "refresh_token": "refresh_token"})

        elif url == "https://login.live.com/oauth20_token.srf":
            if kwargs["data"]["refresh_token"] != "refresh_token":
                return MicrosoftRequestsResponseMock(403, {"error": ""})

            return MicrosoftRequestsResponseMock(200, {"access_token": "test_access_token", "token_type": "Bearer", "expires_in": 0, "scope": "", "refresh_token": "refresh_token"})

        elif url == "https://user.auth.xboxlive.com/user/authenticate":
            if kwargs["json"]["Properties"]["RpsTicket"] != "d=test_access_token":
                return MicrosoftRequestsResponseMock(500, {})

            return MicrosoftRequestsResponseMock(200, {"IssueInstant": "", "NotAfter": "", "Token": "xbl_token", "DisplayClaims": {"xui": [{"uhs": "userhash"}]}})

        elif url == "https://xsts.auth.xboxlive.com/xsts/authorize":
            if kwargs["json"]["Properties"]["UserTokens"][0] != "xbl_token":
                return MicrosoftRequestsResponseMock(500, {})

            return MicrosoftRequestsResponseMock(200, {"IssueInstant": "", "NotAfter": "", "Token": "xsts_token", "DisplayClaims": {"xui": [{"uhs": "userhash"}]}})

        elif url == "https://api.minecraftservices.com/authentication/login_with_xbox":
            if kwargs["json"]["identityToken"] != "XBL3.0 x=userhash;xsts_token":
                return MicrosoftRequestsResponseMock(500, {})

            if self._mode == "not_permitted_app":
                return MicrosoftRequestsResponseMock(403, {"error": "FORBIDDEN", "path": "/authentication/login_with_xbox"})

            return MicrosoftRequestsResponseMock(200, {"username": "", "roles": [], "access_token": "minecraft_access_token", "token_type": "Bearer", "expires_in": 0})

        else:
            raise ValueError(f"Invalid POST URL {url}")


def test_get_login_url() -> None:
    login_url = minecraft_launcher_lib.microsoft_account.get_login_url("CLIENT_ID", "REDIRECT_URL")
    assert login_url is not None


def test_generate_state() -> None:
    assert isinstance(minecraft_launcher_lib.microsoft_account.generate_state(), str)


def test_get_secure_login_data() -> None:
    login_url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data("CLIENT_ID", "REDIRECT_URL")

    assert login_url is not None
    assert state is not None
    assert code_verifier is not None


def test_url_contains_auth_code() -> None:
    assert minecraft_launcher_lib.microsoft_account.url_contains_auth_code("https://login.live.com/oauth20_desktop.srf?code=testcode&lc=test") is True
    assert minecraft_launcher_lib.microsoft_account.url_contains_auth_code("https://example.com") is False


def test_get_auth_code_from_url() -> None:
    assert minecraft_launcher_lib.microsoft_account.get_auth_code_from_url("https://login.live.com/oauth20_desktop.srf?code=testcode&lc=test") == "testcode"
    assert minecraft_launcher_lib.microsoft_account.get_auth_code_from_url("https://login.live.com/oauth20_desktop.srf") is None


def test_parse_auth_code_url() -> None:
    test_state = "123456"
    test_code = "abcxyz"

    auth_code = minecraft_launcher_lib.microsoft_account.parse_auth_code_url(f"http://127.0.0.1:3003?code={test_code}&state={test_state}", test_state)
    assert auth_code == test_code


def test_get_authorization_token(monkeypatch: pytest.MonkeyPatch) -> None:
    requests_mock = MicrosoftRequestsMock("default")

    monkeypatch.setattr(requests, "get", requests_mock.get)
    monkeypatch.setattr(requests, "post", requests_mock.post)

    assert minecraft_launcher_lib.microsoft_account.get_authorization_token("client_id", "secret", "redirect_url", "auth_code", "code-verifier")["access_token"] == "test_access_token"


def test_get_store_information(monkeypatch: pytest.MonkeyPatch) -> None:
    requests_mock = MicrosoftRequestsMock("default")

    monkeypatch.setattr(requests, "get", requests_mock.get)
    monkeypatch.setattr(requests, "post", requests_mock.post)

    store = minecraft_launcher_lib.microsoft_account.get_store_information("minecraft_access_token")

    assert store["signature"] == "jwt sig"
    assert store["keyId"] == "1"


def test_complete_login(monkeypatch: pytest.MonkeyPatch) -> None:
    requests_mock = MicrosoftRequestsMock("default")

    monkeypatch.setattr(requests, "get", requests_mock.get)
    monkeypatch.setattr(requests, "post", requests_mock.post)

    login_data = minecraft_launcher_lib.microsoft_account.complete_login("client_id", None, "redirect_url", "auth_code")

    assert login_data["id"] == "minecraft_uuid"
    assert login_data["name"] == "minecraft_name"
    assert login_data["access_token"] == "minecraft_access_token"
    assert login_data["refresh_token"] == "refresh_token"


def test_complete_login_not_own_minecraft(monkeypatch: pytest.MonkeyPatch) -> None:
    requests_mock = MicrosoftRequestsMock("not_own_minecraft")

    monkeypatch.setattr(requests, "get", requests_mock.get)
    monkeypatch.setattr(requests, "post", requests_mock.post)

    with pytest.raises(minecraft_launcher_lib.exceptions.AccountNotOwnMinecraft):
        minecraft_launcher_lib.microsoft_account.complete_login("client_id", None, "redirect_url", "auth_code")


def test_complete_login_not_permitted_azure_app(monkeypatch: pytest.MonkeyPatch) -> None:
    requests_mock = MicrosoftRequestsMock("not_permitted_app")

    monkeypatch.setattr(requests, "get", requests_mock.get)
    monkeypatch.setattr(requests, "post", requests_mock.post)

    with pytest.raises(minecraft_launcher_lib.exceptions.AzureAppNotPermitted):
        minecraft_launcher_lib.microsoft_account.complete_login("client_id", None, "redirect_url", "auth_code")


def test_complete_refresh(monkeypatch: pytest.MonkeyPatch) -> None:
    requests_mock = MicrosoftRequestsMock("default")

    monkeypatch.setattr(requests, "get", requests_mock.get)
    monkeypatch.setattr(requests, "post", requests_mock.post)

    login_data = minecraft_launcher_lib.microsoft_account.complete_refresh("client_id", "client_secret", None, "refresh_token")

    assert login_data["id"] == "minecraft_uuid"
    assert login_data["name"] == "minecraft_name"
    assert login_data["access_token"] == "minecraft_access_token"
    assert login_data["refresh_token"] == "refresh_token"


def test_complete_refresh_not_own_minecraft(monkeypatch: pytest.MonkeyPatch) -> None:
    requests_mock = MicrosoftRequestsMock("not_own_minecraft")

    monkeypatch.setattr(requests, "get", requests_mock.get)
    monkeypatch.setattr(requests, "post", requests_mock.post)

    with pytest.raises(minecraft_launcher_lib.exceptions.AccountNotOwnMinecraft):
        minecraft_launcher_lib.microsoft_account.complete_refresh("client_id", "client_secret", None, "refresh_token")


def test_complete_refresh_invalid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    requests_mock = MicrosoftRequestsMock("default")

    monkeypatch.setattr(requests, "get", requests_mock.get)
    monkeypatch.setattr(requests, "post", requests_mock.post)

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidRefreshToken):
        minecraft_launcher_lib.microsoft_account.complete_refresh("client_id", "client_secret", None, "invalid_token")
