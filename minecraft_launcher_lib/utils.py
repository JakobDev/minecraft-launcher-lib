import platform
import requests
import pathlib
import json
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

def get_installed_versions(path):
    dir_list = os.listdir(os.path.join(path,"versions"))
    version_list = []
    for i in dir_list:
        with open(os.path.join(path,"versions",i,i + ".json"),"r",encoding="utf-8") as f:
            version_data = json.load(f)
        version_list.append({"id":version_data["id"],"type":version_data["type"]})
    return version_list
