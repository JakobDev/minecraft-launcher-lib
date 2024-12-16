# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"""
microsoft_account contains functions for login with a Microsoft Account. Before using this module you need to `create a Azure application <https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app>`_.
Many thanks to wiki.vg for it's `documentation of the login process <https://wiki.vg/Microsoft_Authentication_Scheme>`_.
You may want to read the :doc:`/tutorial/microsoft_login` tutorial before using this module.
For a list of all types see :doc:`microsoft_types`.
"""
from .microsoft_types import AuthorizationTokenResponse, XBLResponse, XSTSResponse, MinecraftAuthenticateResponse, MinecraftStoreResponse, MinecraftProfileResponse, CompleteLoginResponse
from .exceptions import InvalidRefreshToken, AzureAppNotPermitted, AccountNotOwnMinecraft
from ._helper import get_user_agent, assert_func
from base64 import urlsafe_b64encode
from typing import Literal, cast
from hashlib import sha256
import urllib.parse
import requests
import secrets

__AUTH_URL__ = "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
__TOKEN_URL__ = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
__SCOPE__ = "XboxLive.signin offline_access"


def get_login_url(client_id: str, redirect_uri: str) -> str:
    """
    Generate a login url.\\
    For a more secure alternative, use :func:`get_secure_login_data`

    :param client_id: The Client ID of your Azure App
    :param redirect_uri: The Redirect URI of your Azure App
    :return: The url to the website on which the user logs in
    """
    parameters = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "response_mode": "query",
        "scope": __SCOPE__,
    }

    url = urllib.parse.urlparse(__AUTH_URL__)._replace(query=urllib.parse.urlencode(parameters)).geturl()
    return url


def _generate_pkce_data() -> tuple[str, str, Literal["plain", "S256"]]:
    """
    Generates the PKCE code challenge and code verifier

    :return: A tuple containing the code_verifier, the code_challenge and the code_challenge_method.
    """
    code_verifier = secrets.token_urlsafe(128)[:128]
    code_challenge = urlsafe_b64encode(sha256(code_verifier.encode("ascii")).digest()).decode("ascii")[:-1]
    code_challenge_method = "S256"
    return code_verifier, code_challenge, cast(Literal["plain", "S256"], code_challenge_method)


def generate_state() -> str:
    """
    Generates a random state
    """
    return secrets.token_urlsafe(16)


def get_secure_login_data(client_id: str, redirect_uri: str, state: str | None = None) -> tuple[str, str, str]:
    """
    Generates the login data for a secure login with pkce and state.\\
    Prevents Cross-Site Request Forgery attacks and authorization code injection attacks.

    :param client_id: The Client ID of your Azure App
    :param redirect_uri: The Redirect URI of your Azure App
    :param state: You can use a existing state. If not set, a state will be generated using :func:`generate_state`.
    """
    code_verifier, code_challenge, code_challenge_method = _generate_pkce_data()

    if state is None:
        state = generate_state()

    parameters = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "response_mode": "query",
        "scope": __SCOPE__,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": code_challenge_method
    }

    url = urllib.parse.urlparse(__AUTH_URL__)._replace(query=urllib.parse.urlencode(parameters)).geturl()

    return url, state, code_verifier


def url_contains_auth_code(url: str) -> bool:
    """
    Checks if the given url contains a authorization code

    :param url: The URL to check
    """
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    return "code" in qs


def get_auth_code_from_url(url: str) -> str | None:
    """
    Get the authorization code from the url.\\
    If you want to check the state, use :func:`parse_auth_code_url`, which throws errors instead of returning an optional value.

    :param url: The URL to parse
    :return: The auth code or None if the the code is nonexistent
    """
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    try:
        return qs["code"][0]
    except KeyError:
        return None


def parse_auth_code_url(url: str, state: str | None) -> str:
    """
    Parse the authorization code url and checks the state.

    :param url: The URL to parse
    :param state: If set, the function raises a AssertionError, if the state do no match the state in the URL
    :return: The auth code
    """
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)

    if state is not None:
        assert_func(state == qs["state"][0])

    return qs["code"][0]


def get_authorization_token(client_id: str, client_secret: str | None, redirect_uri: str, auth_code: str, code_verifier: str | None = None) -> AuthorizationTokenResponse:
    """
    Get the authorization token. This function is called during :func:`complete_login`, so you need to use this function ony if :func:`complete_login` doesn't work for you.

    :param client_id: The Client ID of your Azure App
    :param client_secret: The Client Secret of your Azure App. This is deprecated and should not been used anymore.
    :param redirect_uri: The Redirect URI of your Azure App
    :param auth_code: The Code you get from :func:`parse_auth_code_url`
    :param code_verifier: The 3rd entry in the Tuple you get from :func:`get_secure_login_data`
    """
    parameters = {
        "client_id": client_id,
        "scope": __SCOPE__,
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    if client_secret is not None:
        parameters["client_secret"] = client_secret

    if code_verifier is not None:
        parameters["code_verifier"] = code_verifier

    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "user-agent": get_user_agent()
    }
    r = requests.post(__TOKEN_URL__, data=parameters, headers=header)
    return r.json()


def refresh_authorization_token(client_id: str, client_secret: str | None, redirect_uri: str | None, refresh_token: str) -> AuthorizationTokenResponse:
    """
    Refresh the authorization token. This function is called during :func:`complete_refresh`, so you need to use this function ony if :func:`complete_refresh` doesn't work for you.

    :param client_id: The Client ID of your Azure App
    :param client_secret: The Client Secret of your Azure App. This is deprecated and should not been used anymore.
    :param redirect_uri: The Redirect URI of Azure App. This Parameter only exists for backwards compatibility and is not used anymore.
    :param refresh_token: Your refresh token
    """
    parameters = {
        "client_id": client_id,
        "scope": __SCOPE__,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    if client_secret is not None:
        parameters["client_secret"] = client_secret

    # redirect_uri was used in a previous version of this library
    # we keep it for backwards compatibility, but it is not required anymore
    _ = redirect_uri

    header = {
        "user-agent": get_user_agent()
    }
    r = requests.post("https://login.live.com/oauth20_token.srf", data=parameters, headers=header)
    return r.json()


def authenticate_with_xbl(access_token: str) -> XBLResponse:
    """
    Authenticate with Xbox Live. This function is called during :func:`complete_login`, so you need to use this function ony if :func:`complete_login` doesn't work for you.

    :param access_token: The Token you get from :func:`get_authorization_token`
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


def authenticate_with_xsts(xbl_token: str) -> XSTSResponse:
    """
    Authenticate with XSTS. This function is called during :func:`complete_login`, so you need to use this function ony if :func:`complete_login` doesn't work for you.

    :param xbl_token: The Token you get from :func:`authenticate_with_xbl`
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


def authenticate_with_minecraft(userhash: str, xsts_token: str) -> MinecraftAuthenticateResponse:
    """
    Authenticate with Minecraft. This function is called during :func:`complete_login`, so you need to use this function ony if :func:`complete_login` doesn't work for you.

    :param userhash: The Hash you get from :func:`authenticate_with_xbl`
    :param xsts_token: The Token you get from :func:`authenticate_with_xsts`
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


def get_store_information(access_token: str) -> MinecraftStoreResponse:
    """
    Get the store information.

    :param access_token: The Token you get from :func:`authenticate_with_minecraft`
    """
    header = {
        "Authorization": f"Bearer {access_token}",
        "user-agent": get_user_agent()
    }
    r = requests.get("https://api.minecraftservices.com/entitlements/mcstore", headers=header)
    return r.json()


def get_profile(access_token: str) -> MinecraftProfileResponse:
    """
    Get the profile. This function is called during :func:`complete_login`, so you need to use this function ony if :func:`complete_login` doesn't work for you.

    :param access_token: The Token you get from :func:`authenticate_with_minecraft`
    """
    header = {
        "Authorization": f"Bearer {access_token}",
        "user-agent": get_user_agent()
    }
    r = requests.get("https://api.minecraftservices.com/minecraft/profile", headers=header)
    return r.json()


def complete_login(client_id: str, client_secret: str | None, redirect_uri: str, auth_code: str, code_verifier: str | None = None) -> CompleteLoginResponse:
    """
    Do the complete login process.

    :param client_id: The Client ID of your Azure App
    :param client_secret: The Client Secret of your Azure App. This is deprecated and should not been used anymore.
    :param redirect_uri: The Redirect URI of your Azure App
    :param auth_code: The Code you get from :func:`parse_auth_code_url`
    :param code_verifier: The 3rd entry in the Tuple you get from :func:`get_secure_login_data`
    :raises AzureAppNotPermitted: Your Azure App don't have the Permission to use the Minecraft API
    :raises AccountNotOwnMinecraft: The Account does not own Minecraft

    It returns the following:

    .. code:: json

        {
            "id" : "The uuid",
            "name" : "The username",
            "access_token": "The acces token",
            "refresh_token": "The refresh token",
            "skins" : [{
                "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
                "state" : "ACTIVE",
                "url" : "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
                "variant" : "CLASSIC",
                "alias" : "STEVE"
            } ],
            "capes" : []
        }
    """
    token_request = get_authorization_token(client_id, client_secret, redirect_uri, auth_code, code_verifier)
    token = token_request["access_token"]

    xbl_request = authenticate_with_xbl(token)
    xbl_token = xbl_request["Token"]
    userhash = xbl_request["DisplayClaims"]["xui"][0]["uhs"]

    xsts_request = authenticate_with_xsts(xbl_token)
    xsts_token = xsts_request["Token"]

    account_request = authenticate_with_minecraft(userhash, xsts_token)

    if "access_token" not in account_request:
        raise AzureAppNotPermitted()

    access_token = account_request["access_token"]

    profile = get_profile(access_token)

    if "error" in profile and profile["error"] == "NOT_FOUND":
        raise AccountNotOwnMinecraft()

    profile = cast(CompleteLoginResponse, profile)

    profile["access_token"] = account_request["access_token"]
    profile["refresh_token"] = token_request["refresh_token"]

    return profile


def complete_refresh(client_id: str, client_secret: str | None, redirect_uri: str | None, refresh_token: str) -> CompleteLoginResponse:
    """
    Do the complete login process with a refresh token. It returns the same as :func:`complete_login`.

    :param client_id: The Client ID of your Azure App
    :param client_secret: The Client Secret of your Azure App. This is deprecated and should not been used anymore.
    :param redirect_uri: The Redirect URI of Azure App. This Parameter only exists for backwards compatibility and is not used anymore.
    :param refresh_token: Your refresh token
    :raises InvalidRefreshToken: Your refresh token is not valid
    :raises AccountNotOwnMinecraft: The Account does not own Minecraft
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

    if "error" in profile and profile["error"] == "NOT_FOUND":
        raise AccountNotOwnMinecraft()

    profile = cast(CompleteLoginResponse, profile)

    profile["access_token"] = account_request["access_token"]
    profile["refresh_token"] = token_request["refresh_token"]

    return profile
