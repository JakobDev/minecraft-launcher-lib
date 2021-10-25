from .exceptions import InvalidRefreshToken
from .helper import get_user_agent
from typing import List, Dict, Union
import urllib.parse
import requests


def get_login_url(client_id: str, redirect_uri: str) -> str:
    """
    Returns the url to the website on which the user logs in
    """
    return f"https://login.live.com/oauth20_authorize.srf?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope=XboxLive.signin%20offline_access&state=<optional;"


def url_contains_auth_code(url: str) -> bool:
    """
    Checks if the given url contains a authorization code
    """
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    return "code" in qs


def get_auth_code_from_url(url: str) -> str:
    """
    Get the authorization code from the url
    """
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    return qs["code"][0]


def get_authorization_token(client_id: str, client_secret: str, redirect_uri: str, auth_code: str) -> Dict[str, str]:
    """
    Get the authorization token
    """
    parameters = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": auth_code,
        "grant_type": "authorization_code",
    }
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "user-agent": get_user_agent()
    }
    r = requests.post("https://login.live.com/oauth20_token.srf", data=parameters, headers=header)
    return r.json()


def refresh_authorization_token(client_id: str, client_secret: str, redirect_uri: str, refresh_token: str,) -> Dict[str, str]:
    """
    Refresh the authorization token
    """
    parameters = {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    header = {
        "user-agent": get_user_agent()
    }
    r = requests.post("https://login.live.com/oauth20_token.srf", data=parameters, headers=header)
    return r.json()


def authenticate_with_xbl(access_token: str) -> Dict[str, Union[str, Dict[str, List[Dict[str, str]]]]]:
    """
    Authenticate with Xbox Live
    """
    parameters = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={access_token}"
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }
    header = {
        "Content-Type": "application/json",
        "user-agent": get_user_agent(),
        "Accept": "application/json"
    }
    r = requests.post("https://user.auth.xboxlive.com/user/authenticate", json=parameters, headers=header)
    return r.json()


def authenticate_with_xsts(xbl_token: str) -> Dict[str, Union[str, Dict[str, Union[str, List[str]]]]]:
    """
    Authenticate with XSTS
    """
    parameters = {
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [
                xbl_token
            ]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    }
    header = {
        "Content-Type": "application/json",
        "user-agent": get_user_agent(),
        "Accept": "application/json"
    }
    r = requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", json=parameters, headers=header)
    return r.json()


def authenticate_with_minecraft(userhash: str, xsts_token: str) -> Dict[str, Union[str, List, int]]:
    """
    Authenticate with Minecraft
    """
    parameters = {
        "identityToken": f"XBL3.0 x={userhash};{xsts_token}"
    }
    header = {
        "Content-Type": "application/json",
        "user-agent": get_user_agent(),
        "Accept": "application/json"
    }
    r = requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", json=parameters, headers=header)
    return r.json()


def get_store_information(token: str) -> Dict[str, Union[List[Dict[str, str]]]]:
    """
    Get the store information
    """
    header = {
        "Authorization": f"Bearer {token}",
        "user-agent": get_user_agent()
    }
    r = requests.get("https://api.minecraftservices.com/entitlements/mcstore", headers=header)
    return r.json()


def get_profile(token: str) -> Dict[str, Union[List[Dict[str, str]]]]:
    """
    Get the profile
    """
    header = {
        "Authorization": f"Bearer {token}",
        "user-agent": get_user_agent()
    }
    r = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=header)
    return r.json()


def complete_login(client_id: str, client_secret: str, redirect_uri: str, auth_code: str) -> Dict[str, Union[List[Dict[str, str]]]]:
    """
    Do the complete login process
    """
    token_request = get_authorization_token(client_id, client_secret, redirect_uri, auth_code)
    token = token_request["access_token"]

    xbl_request = authenticate_with_xbl(token)
    xbl_token = xbl_request["Token"]
    userhash = xbl_request["DisplayClaims"]["xui"][0]["uhs"]

    xsts_request = authenticate_with_xsts(xbl_token)
    xsts_token = xsts_request["Token"]

    account_request = authenticate_with_minecraft(userhash, xsts_token)
    access_token = account_request["access_token"]

    profile = get_profile(access_token)

    profile["access_token"] = account_request["access_token"]
    profile["refresh_token"] = token_request["refresh_token"]

    return profile


def complete_refresh(client_id: str, client_secret: str, redirect_uri: str, refresh_token: str) -> Dict[str, Union[List[Dict[str, str]]]]:
    """
    Do the complete login process with a refresh token
    """
    token_request = refresh_authorization_token(client_id, client_secret, redirect_uri, refresh_token)

    if "error" in token_request:
        raise InvalidRefreshToken()

    token = token_request["access_token"]

    xbl_request = authenticate_with_xbl(token)
    xbl_token = xbl_request["Token"]
    userhash = xbl_request["DisplayClaims"]["xui"][0]["uhs"]

    xsts_request = authenticate_with_xsts(xbl_token)
    xsts_token = xsts_request["Token"]

    account_request = authenticate_with_minecraft(userhash, xsts_token)
    access_token = account_request["access_token"]

    profile = get_profile(access_token)

    profile["access_token"] = account_request["access_token"]
    profile["refresh_token"] = token_request["refresh_token"]

    return profile
