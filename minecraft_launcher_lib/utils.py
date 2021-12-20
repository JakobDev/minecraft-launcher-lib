from typing import Dict, List, Union
import platform
import requests
import random
import pathlib
import shutil
import uuid
import json
import os

__version__ = "4.2"


def get_minecraft_directory() -> str:
    """
    Returns the default path to the .minecraft directory
    """
    if platform.system() == "Windows":
        return os.path.join(os.getenv('APPDATA'), ".minecraft")
    elif platform.system() == "Darwin":
        return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "minecraft")
    else:
        return os.path.join(str(pathlib.Path.home()), ".minecraft")


def get_latest_version() -> Dict[str, str]:
    """
    Returns the latest version of Minecraft
    """
    return requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", headers={"user-agent": f"minecraft-launcher-lib/{get_library_version()}"}).json()["latest"]


def get_version_list() -> List[Dict[str, str]]:
    """
    Returns all versions that Mojang offers to download
    """
    vlist = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", headers={"user-agent": f"minecraft-launcher-lib/{get_library_version()}"}).json()
    returnlist = []
    for i in vlist["versions"]:
        returnlist.append({"id": i["id"], "type": i["type"]})
    return returnlist


def get_installed_versions(minecraft_directory: Union[str, os.PathLike]) -> List[Dict[str, str]]:
    """
    Returns all installed versions
    """
    dir_list = os.listdir(os.path.join(minecraft_directory, "versions"))
    version_list = []
    for i in dir_list:
        if not os.path.isfile(os.path.join(minecraft_directory, "versions", i, i + ".json")):
            continue
        with open(os.path.join(minecraft_directory, "versions", i, i + ".json"), "r", encoding="utf-8") as f:
            version_data = json.load(f)
        version_list.append({"id": version_data["id"], "type": version_data["type"]})
    return version_list


def get_available_versions(minecraft_directory: Union[str, os.PathLike]) -> List[Dict[str, str]]:
    """
    Returns all installed versions and all versions that Mojang offers to download
    """
    version_list = []
    version_check = []
    for i in get_version_list():
        version_list.append({"id": i["id"], "type": i["type"]})
        version_check.append(i["id"])
    for i in get_installed_versions(minecraft_directory):
        if not i["id"] in version_check:
            version_list.append(i)
    return version_list


def get_java_executable() -> str:
    """
    Tries the find out the path to the default java executable
    """
    if platform.system() == "Windows":
        if os.getenv("JAVA_HOME"):
            return os.path.join(os.getenv("JAVA_HOME"), "bin", "java.exe")
        elif os.path.isfile(r"C:\Program Files (x86)\Common Files\Oracle\Java\javapath\java.exe"):
            return r"C:\Program Files (x86)\Common Files\Oracle\Java\javapath\java.exe"
        else:
            return shutil.which("java") or "java"
    elif os.getenv("JAVA_HOME"):
        return os.path.join(os.getenv("JAVA_HOME"), "bin", "java")
    elif platform.system() == "Darwin":
        return shutil.which("java") or "java"
    else:
        if os.path.islink("/etc/alternatives/java"):
            return os.readlink("/etc/alternatives/java")
        elif os.path.islink("/usr/lib/jvm/default-runtime"):
            return os.path.join("/usr", "lib", "jvm", os.readlink("/usr/lib/jvm/default-runtime"), "bin", "java")
        else:
            return shutil.which("java") or "java"


def get_library_version() -> str:
    """
    Returns the version of minecraft-launcher-lib
    """
    return __version__


def generate_test_options() -> Dict[str, str]:
    """
    Generates options to launch minecraft. Useful for testing. Do not use in production.
    """
    return {
        "username": f"Player{random.randrange(100,1000)}",
        "uuid": str(uuid.uuid4()),
        "token": ""
    }


def is_version_valid(version: str, minecraft_directory: Union[str, os.PathLike]) -> bool:
    """
    Checks if the given version exists
    """
    if os.path.isdir(os.path.join(minecraft_directory, "versions", version)):
        return True
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", headers={"user-agent": f"minecraft-launcher-lib/{get_library_version()}"}).json()
    for i in version_list["versions"]:
        if i["id"] == version:
            return True
    return False


def get_minecraft_news(page_size: int = 20) -> Dict:
    """
    Get the news from minecraft.net
    """
    parameters = {
        "pageSize": page_size
    }
    header = {
        "user-agent": f"minecraft-launcher-lib/{get_library_version()}"
    }
    return requests.get("https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid", params=parameters, headers=header).json()
