import distutils.spawn
import platform
import requests
import pathlib
import json
import os

def get_minecraft_directory():
    if platform.system() == "Windows":
        return os.path.join(os.getenv('APPDATA'), ".minecraft")
    elif platform.system() == "Darwin":
        return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "minecraft")
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
        if not os.path.isdir(os.path.join(path,"versions",i)):
            continue
        with open(os.path.join(path,"versions",i,i + ".json"),"r",encoding="utf-8") as f:
            version_data = json.load(f)
        version_list.append({"id":version_data["id"],"type":version_data["type"]})
    return version_list

def get_available_versions(path):
    version_list = []
    version_check = []
    for i in get_version_list():
        version_list.append({"id":i["id"],"type":i["type"]})
        version_check.append(i["id"])
    for i in get_installed_versions(path):
        if not i["id"] in version_check:
            version_list.append(i)
    return version_list

def get_java_executable():
    if platform.system() == "Windows":
        if os.getenv("JAVA_HOME"):
            return os.path.join(os.getenv("JAVA_HOME"),"bin","java.exe")
        elif os.path.isfile("C:\Program Files (x86)\Common Files\Oracle\Java\javapath\java.exe"):
            return "C:\Program Files (x86)\Common Files\Oracle\Java\javapath\java.exe"
        else:
            return distutils.spawn.find_executable("java") or "java"
    elif os.getenv("JAVA_HOME"):
            return os.path.join(os.getenv("JAVA_HOME"),"bin","java")
    elif platform.system() == "Darwin":
        return distutils.spawn.find_executable("java") or "java"
    else:
        try:
            return os.readlink("/etc/alternatives/java")
        except:
            return distutils.spawn.find_executable("java") or "java"

def get_library_version():
    return "2.1"
