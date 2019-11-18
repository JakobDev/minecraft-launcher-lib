import platform
import requests
import pathlib
import os

def get_minecraft_directory():
    if platform.system() == "Windows":
        return os.path.join(os.getenv('APPDATA'), ".minecraft")
    elif platform.system() == "Darwin":
        return os.path.join(str(pathlib.Path.home()), "Library",
                            "Application Support", "minecraft")
    else:
        return os.path.join(str(pathlib.Path.home()), ".minecraft")

def get_latest_version():
    return requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()["latest"]

def get_version_list():
    vlist = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    returnlist = []
    for i in vlist["versions"]:
        returnlist.append({"id":i["id"],"type":i["type"]})
    return returnlist
