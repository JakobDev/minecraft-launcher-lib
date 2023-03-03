"utils contains a few functions for helping you that doesn't fit in any other category"
from .types import Articles, MinecraftOptions, LatestMinecraftVersions, MinecraftVersionInfo
from ._internal_types.shared_types import ClientJson, VersionListManifestJson
from ._helper import get_requests_response_cache
from typing import List, Union
from datetime import datetime
import platform
import requests
import random
import pathlib
import shutil
import uuid
import json
import os


def get_minecraft_directory() -> str:
    """
    Returns the default path to the .minecraft directory
    """
    if platform.system() == "Windows":
        return os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".minecraft")
    elif platform.system() == "Darwin":
        return os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "minecraft")
    else:
        return os.path.join(str(pathlib.Path.home()), ".minecraft")


def get_latest_version() -> LatestMinecraftVersions:
    """
    Returns the latest version of Minecraft
    """
    return get_requests_response_cache("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json").json()["latest"]


def get_version_list() -> List[MinecraftVersionInfo]:
    """
    Returns all versions that Mojang offers to download
    """
    vlist: VersionListManifestJson = get_requests_response_cache("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json").json()
    returnlist: List[MinecraftVersionInfo] = []
    for i in vlist["versions"]:
        returnlist.append({"id": i["id"], "type": i["type"], "releaseTime": datetime.fromisoformat(i["releaseTime"]), "complianceLevel": i["complianceLevel"]})
    return returnlist


def get_installed_versions(minecraft_directory: Union[str, os.PathLike]) -> List[MinecraftVersionInfo]:
    """
    Returns all installed versions

    :param minecraft_directory: The path to your Minecraft directory
    """
    try:
        dir_list = os.listdir(os.path.join(minecraft_directory, "versions"))
    except FileNotFoundError:
        return []

    version_list: List[MinecraftVersionInfo] = []
    for i in dir_list:
        if not os.path.isfile(os.path.join(minecraft_directory, "versions", i, i + ".json")):
            continue

        with open(os.path.join(minecraft_directory, "versions", i, i + ".json"), "r", encoding="utf-8") as f:
            version_data: ClientJson = json.load(f)

        try:
            release_time = datetime.fromisoformat(version_data["releaseTime"])
        except ValueError:
            # In case some custom client has a invalid time
            release_time = datetime.fromtimestamp(0)

        version_list.append({"id": version_data["id"], "type": version_data["type"], "releaseTime": release_time, "complianceLevel": version_data.get("complianceLevel", 0)})
    return version_list


def get_available_versions(minecraft_directory: Union[str, os.PathLike]) -> List[MinecraftVersionInfo]:
    """
    Returns all installed versions and all versions that Mojang offers to download

    :param minecraft_directory: The path to your Minecraft directory
    """
    version_list = []
    version_check = []

    for i in get_version_list():
        version_list.append(i)
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
        if (java_home := os.getenv("JAVA_HOME")) is not None:
            return os.path.join(java_home, "bin", "javaw.exe")
        elif os.path.isfile(r"C:\Program Files (x86)\Common Files\Oracle\Java\javapath\javaw.exe"):
            return r"C:\Program Files (x86)\Common Files\Oracle\Java\javapath\javaw.exe"
        else:
            return shutil.which("javaw") or "javaw"
    elif (java_home := os.getenv("JAVA_HOME")) is not None:
        return os.path.join(java_home, "bin", "java")
    elif platform.system() == "Darwin":
        return shutil.which("java") or "java"
    else:
        if os.path.islink("/etc/alternatives/java"):
            return os.readlink("/etc/alternatives/java")
        elif os.path.islink("/usr/lib/jvm/default-runtime"):
            return os.path.join("/usr", "lib", "jvm", os.readlink("/usr/lib/jvm/default-runtime"), "bin", "java")
        else:
            return shutil.which("java") or "java"


_version_cache = None


def get_library_version() -> str:
    """
    Returns the version of minecraft-launcher-lib
    """
    global _version_cache
    if _version_cache is not None:
        return _version_cache
    else:
        with open(os.path.join(os.path.dirname(__file__), "version.txt"), "r", encoding="utf-8") as f:
            _version_cache = f.read().strip()
            return _version_cache


def generate_test_options() -> MinecraftOptions:
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

    :param version: A Minecraft version
    :param minecraft_directory: The path to your Minecraft directory
    """
    if os.path.isdir(os.path.join(minecraft_directory, "versions", version)):
        return True
    for i in get_version_list():
        if i["id"] == version:
            return True
    return False


def get_minecraft_news(page_size: int = 20) -> Articles:
    """
    Get the news from minecraft.net

    :param page_size: The Page Size (default 20)
    """
    parameters = {
        "pageSize": page_size
    }
    header = {
        "user-agent": f"minecraft-launcher-lib/{get_library_version()}"
    }
    return requests.get("https://www.minecraft.net/content/minecraft-net/_jcr_content.articles.grid", params=parameters, headers=header).json()


def is_vanilla_version(version: str) -> bool:
    """
    Checks if the given version is a vanilla version

    :param version: A Minecraft version
    """
    for i in get_version_list():
        if i["id"] == version:
            return True
    return False


def is_platform_supported() -> bool:
    """
    Checks if the current platform is supported
    """
    if platform.system() not in ["Windows", "Darwin", "Linux"]:
        return False
    return True
