# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"utils contains a few functions for helping you that doesn't fit in any other category"
from .types import MinecraftOptions, LatestMinecraftVersions, MinecraftVersionInfo
from ._internal_types.shared_types import ClientJson, VersionListManifestJson
from ._helper import get_requests_response_cache, assert_func
from datetime import datetime
import platform
import pathlib
import random
import shutil
import uuid
import json
import os


def get_minecraft_directory() -> str:
    """
    Returns the default path to the .minecraft directory

    Example:

    .. code:: python

        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        print(f"The default minecraft directory is {minecraft_directory}")
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

    Example:

    .. code:: python

        latest_version = minecraft_launcher_lib.utils.get_latest_version()
        print("Latest Release " + latest_version["release"])
        print("Latest Snapshot " + latest_version["snapshot"])
    """
    return get_requests_response_cache("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json").json()["latest"]


def get_version_list() -> list[MinecraftVersionInfo]:
    """
    Returns all versions that Mojang offers to download

    Example:

    .. code:: python

        for version in minecraft_launcher_lib.utils.get_version_list():
            print(version["id"])
    """
    vlist: VersionListManifestJson = get_requests_response_cache("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json").json()
    returnlist: list[MinecraftVersionInfo] = []
    for i in vlist["versions"]:
        returnlist.append({"id": i["id"], "type": i["type"], "releaseTime": datetime.fromisoformat(i["releaseTime"]), "complianceLevel": i["complianceLevel"]})
    return returnlist


def get_installed_versions(minecraft_directory: str | os.PathLike) -> list[MinecraftVersionInfo]:
    """
    Returns all installed versions

    Example:

    .. code:: python

        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        for version in minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory):
            print(version["id"])

    :param minecraft_directory: The path to your Minecraft directory
    """
    try:
        dir_list = os.listdir(os.path.join(minecraft_directory, "versions"))
    except FileNotFoundError:
        return []

    version_list: list[MinecraftVersionInfo] = []
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


def get_available_versions(minecraft_directory: str | os.PathLike) -> list[MinecraftVersionInfo]:
    """
    Returns all installed versions and all versions that Mojang offers to download

    Example:

    .. code:: python

        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        for version in minecraft_launcher_lib.utils.get_available_versions(minecraft_directory):
            print(version["id"])

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
    Tries the find out the path to the default java executable.
    Returns :code:`java`, if no path was found.

    Example:

    .. code:: python

        print("The path to Java is " + minecraft_launcher_lib.utils.get_java_executable())
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

    Example:

    .. code:: python

        print(f"You are using version {minecraft_launcher_lib.utils.get_library_version()} of minecraft-launcher-lib")
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
    Generates test options to launch minecraft.
    This includes a random name and a random uuid.

    .. note::
        This function is just for debugging and testing, if Minecraft works.
        The behavior of this function may change in the future.
        Do not use it in production.

    Example:

    .. code:: python

        version = "1.0"
        options = minecraft_launcher_lib.utils.generate_test_options()
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directory, options)
        subprocess.run(command)
    """
    return {
        "username": f"Player{random.randrange(100, 1000)}",
        "uuid": str(uuid.uuid4()),
        "token": ""
    }


def is_version_valid(version: str, minecraft_directory: str | os.PathLike) -> bool:
    """
    Checks if the given version exists.
    This checks if the given version is installed or offered to download by Mojang.
    Basically you can use this tho check, if the given version can be used with :func:`~minecraft_launcher_lib.install.install_minecraft_version`.

    Example:

    .. code:: python

        version = "1.0"
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        if minecraft_launcher_lib.utils.is_version_valid(version, minecraft_directory):
            print(f"{version} is a valid version")
        else:
            print(f"{version} is not a valid version")

    :param version: A Minecraft version
    :param minecraft_directory: The path to your Minecraft directory
    """
    if os.path.isdir(os.path.join(minecraft_directory, "versions", version)):
        return True
    for i in get_version_list():
        if i["id"] == version:
            return True
    return False


def is_vanilla_version(version: str) -> bool:
    """
    Checks if the given version is a vanilla version

    Example:

    .. code:: python

        version = "1.0"
        if minecraft_launcher_lib.utils.is_vanilla_version(version):
            print(f"{version} is a vanilla version")
        else:
            print(f"{version} is not a vanilla version")

    :param version: A Minecraft version
    """
    for i in get_version_list():
        if i["id"] == version:
            return True
    return False


def is_platform_supported() -> bool:
    """
    Checks if the current platform is supported

    Example:

    .. code:: python

        if not minecraft_launcher_lib.utils.is_platform_supported():
            print("Your platform is not supported", file=sys.stderr)
            sys.exit(1)
    """
    if platform.system() not in ["Windows", "Darwin", "Linux"]:
        return False
    return True


def is_minecraft_installed(minecraft_directory: str | os.PathLike) -> bool:
    """
    Checks, if there is already a existing Minecraft Installation in the given Directory

    Example:

    .. code:: python

        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        if minecraft_launcher_lib.utils.is_minecraft_installed(minecraft_directory):
            print("Minecraft is installed")
        else:
            print("Minecraft is not installed")

    :param minecraft_directory: The path to your Minecraft directory
    :return: Is a Installation is found
    """
    try:
        assert_func(os.path.isdir(os.path.join(minecraft_directory, "versions")))
        assert_func(os.path.isdir(os.path.join(minecraft_directory, "libraries")))
        assert_func(os.path.isdir(os.path.join(minecraft_directory, "assets")))
        return True
    except AssertionError:
        return False
