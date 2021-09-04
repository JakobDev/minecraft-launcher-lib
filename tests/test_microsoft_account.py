import minecraft_launcher_lib


def test_get_login_url():
    assert minecraft_launcher_lib.microsoft_account.get_login_url("client", "uri") == "https://login.live.com/oauth20_authorize.srf?client_id=client&response_type=code&redirect_uri=uri&scope=XboxLive.signin%20offline_access&state=<optional;"


def test_url_contains_auth_code():
    assert minecraft_launcher_lib.microsoft_account.url_contains_auth_code("https://login.live.com/oauth20_desktop.srf?code=testcode&lc=test") is True
    assert minecraft_launcher_lib.microsoft_account.url_contains_auth_code("https://example.com") is False


def test_get_auth_code_from_url():
    assert minecraft_launcher_lib.microsoft_account.get_auth_code_from_url("https://login.live.com/oauth20_desktop.srf?code=testcode&lc=test") == "testcode"
