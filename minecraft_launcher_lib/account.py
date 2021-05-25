# Thanks to https://github.com/Polyr/mojang-api/blob/master/mojang_api/servers/authserver.py
from .helper import get_user_agent
from typing import Dict, Any
import requests
import uuid


def login_user(username: str, password: str) -> Dict[str, Any]:
    """
    Logs a user in
    """
    payload = {
        "agent": {
            "name": "Minecraft",
            "version": 1
        },
        "username": username,
        "password": password,
        "clientToken": uuid.uuid4().hex
    }

    response = requests.post("https://authserver.mojang.com/authenticate", json=payload, headers={"user-agent": get_user_agent()})
    return response.json()


def validate_access_token(access_token: str) -> bool:
    """
    Check if a access token is valid
    """
    payload = {
        "accessToken": access_token,
    }
    response = requests.post("https://authserver.mojang.com/validate", json=payload, headers={"user-agent": get_user_agent()})
    return response.status_code == 204


def refresh_access_token(access_token: str, client_token: str) -> Dict[str, Any]:
    """
    Get a new access and client token
    """
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    response = requests.post("https://authserver.mojang.com/refresh", json=payload, headers={"user-agent": get_user_agent()})
    return response.json()


def logout_user(username: str, password: str) -> bool:
    """
    Logs a user out
    """
    payload = {
        'username': username,
        'password': password
    }
    response = requests.post("https://authserver.mojang.com/signout", json=payload, headers={"user-agent": get_user_agent()})
    return response.status_code == 204


def invalidate_access_token(access_token: str, client_token: str) -> Any:
    """
    Makes a access token invalid
    """
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }
    response = requests.post("https://authserver.mojang.com/invalidate", json=payload, headers={"user-agent": get_user_agent()})
    return response


def upload_skin(uuid: str, access_token: str, path: str, slim: bool = False) -> Any:
    """
    Upload a skin
    """
    headers = {
        "Authorization": "Bearer " + access_token,
        "user-agent": get_user_agent()
    }
    files = {
        "model": "slim" if slim else "",
        "file": open(path, "rb")
    }
    response = requests.put("https://api.mojang.com/user/profile/{uuid}/skin".format(uuid=uuid), headers=headers, files=files)
    return response


def reset_skin(uuid: str, access_token: str) -> Any:
    """
    Reset the skin to the default skin
    """
    headers = {
        "Authorization": "Bearer " + access_token,
        "user-agent": get_user_agent()
    }
    response = requests.delete("https://api.mojang.com/user/profile/{uuid}/skin".format(uuid=uuid), headers=headers)
    return response
