#Thanks to https://github.com/Polyr/mojang-api/blob/master/mojang_api/servers/authserver.py
import requests
import uuid

def login_user(username, password):
    payload = {
        "agent": {
            "name": "Minecraft",
            "version": 1
        },
        "username": username,
        "password": password,
        "clientToken": uuid.uuid4().hex
    }

    response = requests.post("https://authserver.mojang.com/authenticate", json=payload)
    return response.json()

def validate_access_token(access_token):
    payload = {
        "accessToken": access_token,
    }
    response = requests.post("https://authserver.mojang.com/validate", json=payload)
    return response.status_code == 204

def refresh_access_token(access_token, client_token):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }

    response = requests.post("https://authserver.mojang.com/refresh", json=payload)
    return response.json()

def logout_user(username, password):
    payload = {
        'username': username,
        'password': password
    }
    response = requests.post("https://authserver.mojang.com/signout", json=payload)
    return  response.status_code == 204

def invalidate_access_token(access_token, client_token):
    payload = {
        'accessToken': access_token,
        'clientToken': client_token
    }
    response = requests.post("https://authserver.mojang.com/invalidate", json=payload)
    return response
