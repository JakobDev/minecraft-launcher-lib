# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"runtime allows to install the java runtime. This module is used by :func:`~minecraft_launcher_lib.install.install_minecraft_version`, so you don't need to use it in your code most of the time."
from ._helper import get_user_agent, download_file, empty, get_sha1_hash, check_path_inside_minecraft_directory, get_client_json
from ._internal_types.runtime_types import RuntimeListJson, PlatformManifestJson, _PlatformManifestJsonFile
from .types import CallbackDict, JvmRuntimeInformation, VersionRuntimeInformation
from .exceptions import VersionNotFound, PlatformNotSupported
from concurrent.futures import ThreadPoolExecutor
import subprocess
import datetime
import requests
import platform
import os

_JVM_MANIFEST_URL = "https://launchermeta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json"


def _get_jvm_platform_string() -> str:
    """
    Get the name that is used the identify the platform
    """
    match platform.system():
        case "Windows":
            if platform.architecture()[0] == "32bit":
                return "windows-x86"
            else:
                return "windows-x64"
        case "Linux":
            if platform.architecture()[0] == "32bit":
                return "linux-i386"
            else:
                return "linux"
        case "Darwin":
            if platform.machine() == "arm64":
                return "mac-os-arm64"
            else:
                return "mac-os"
        case _:
            return "gamecore"


def get_jvm_runtimes() -> list[str]:
    """
    Returns a list of all jvm runtimes

    Example:

    .. code:: python

        for runtime in minecraft_launcher_lib.runtime.get_jvm_runtimes():
            print(runtime)
    """
    manifest_data: RuntimeListJson = requests.get(_JVM_MANIFEST_URL, headers={"user-agent": get_user_agent()}).json()
    jvm_list = []
    for key in manifest_data[_get_jvm_platform_string()].keys():
        jvm_list.append(key)
    return jvm_list


def get_installed_jvm_runtimes(minecraft_directory: str | os.PathLike) -> list[str]:
    """
    Returns a list of all installed jvm runtimes

    Example:

    .. code:: python

        for runtime in minecraft_launcher_lib.runtime.get_installed_jvm_runtimes():
            print(runtime)

    :param minecraft_directory: The path to your Minecraft directory
    """
    try:
        return os.listdir(os.path.join(minecraft_directory, "runtime"))
    except FileNotFoundError:
        return []


def install_jvm_runtime(
        jvm_version: str,
        minecraft_directory: str | os.PathLike,
        callback: CallbackDict | None = None,
        max_workers: int | None = None) -> None:
    """
    Installs the given jvm runtime. callback is the same dict as in the install module.

    Example:

    .. code:: python

        runtime_version = "java-runtime-gamma"
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        minecraft_launcher_lib.runtime.install_jvm_runtime(runtime_version, minecraft_directory)

    :param jvm_version: The Name of the JVM version
    :param minecraft_directory: The path to your Minecraft directory
    :param callback: the same dict as for :func:`~minecraft_launcher_lib.install.install_minecraft_version`
    :param max_workers: number of workers for asynchronous downloads. If None, max_workers will be set automatically.
    :raises VersionNotFound: The given JVM Version was not found
    :raises FileOutsideMinecraftDirectory: A File should be placed outside the given Minecraft directory
    """
    if callback is None:
        callback = {}

    manifest_data: RuntimeListJson = requests.get(_JVM_MANIFEST_URL, headers={"user-agent": get_user_agent()}).json()
    platform_string = _get_jvm_platform_string()
    # Check if the jvm version exists
    if jvm_version not in manifest_data[platform_string]:
        raise VersionNotFound(jvm_version)
    # Check if there is a platform manifest
    if len(manifest_data[platform_string][jvm_version]) == 0:
        return
    platform_manifest: PlatformManifestJson = requests.get(manifest_data[platform_string][jvm_version][0]["manifest"]["url"], headers={"user-agent": get_user_agent()}).json()
    base_path = os.path.join(minecraft_directory, "runtime", jvm_version, platform_string, jvm_version)
    session = requests.session()
    file_list: list[str] = []

    def install_runtime_file(key: str, value: _PlatformManifestJsonFile) -> None:
        """Install the single runtime file."""
        current_path = os.path.join(base_path, key)
        check_path_inside_minecraft_directory(minecraft_directory, current_path)

        if value["type"] == "file":
            # Prefer downloading the compresses file
            if "lzma" in value["downloads"]:
                download_file(value["downloads"]["lzma"]["url"], current_path, sha1=value["downloads"]["raw"]["sha1"], callback=callback, lzma_compressed=True, session=session)
            else:
                download_file(value["downloads"]["raw"]["url"], current_path, sha1=value["downloads"]["raw"]["sha1"], callback=callback, session=session)

            # Make files executable on unix systems
            if value["executable"]:
                try:
                    subprocess.run(["chmod", "+x", current_path])
                except FileNotFoundError:
                    pass
            file_list.append(key)

        elif value["type"] == "directory":
            try:
                os.makedirs(current_path)
            except Exception:
                pass

        elif value["type"] == "link":
            check_path_inside_minecraft_directory(minecraft_directory, os.path.join(base_path, value["target"]))
            os.makedirs(os.path.dirname(current_path), exist_ok=True)

            try:
                os.symlink(value["target"], current_path)
            except Exception:
                pass

    # Download all files of the runtime
    callback.get("setMax", empty)(len(platform_manifest["files"]) - 1)
    count = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(install_runtime_file, key, value)
            for key, value in platform_manifest["files"].items()
        ]
        for future in futures:
            future.result()
            count += 1
            callback.get("setProgress", empty)(count)

    # Create the .version file
    version_path = os.path.join(minecraft_directory, "runtime", jvm_version, platform_string, ".version")
    check_path_inside_minecraft_directory(minecraft_directory, version_path)
    with open(version_path, "w", encoding="utf-8") as f:
        f.write(manifest_data[platform_string][jvm_version][0]["version"]["name"])

    # Writes the .sha1 file
    # It has the structure {path} /#// {sha1} {creation time in nanoseconds}
    sha1_path = os.path.join(minecraft_directory, "runtime", jvm_version, platform_string, f"{jvm_version}.sha1")
    check_path_inside_minecraft_directory(minecraft_directory, sha1_path)
    with open(sha1_path, "w", encoding="utf-8") as f:
        for current_file in file_list:
            current_path = os.path.join(base_path, current_file)
            ctime = os.stat(current_path).st_ctime_ns
            sha1 = get_sha1_hash(current_path)
            f.write(f"{current_file} /#// {sha1} {ctime}\n")


def get_executable_path(jvm_version: str, minecraft_directory: str | os.PathLike) -> str | None:
    """
    Returns the path to the executable. Returns None if none is found.

    Example:

    .. code:: python

        runtime_version = "java-runtime-gamma"
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        executable_path = minecraft_launcher_lib.runtime.get_executable_path(runtime_version, minecraft_directory)
        if executable_path is not None:
            print(f"Executable path: {executable_path}")
        else:
            print("The executable path was not found")

    :param jvm_version: The Name of the JVM version
    :param minecraft_directory: The path to your Minecraft directory
    """
    java_path = os.path.join(minecraft_directory, "runtime", jvm_version, _get_jvm_platform_string(), jvm_version, "bin", "java")
    if os.path.isfile(java_path):
        return java_path
    elif os.path.isfile(java_path + ".exe"):
        return java_path + ".exe"
    java_path = java_path.replace(os.path.join("bin", "java"), os.path.join("jre.bundle", "Contents", "Home", "bin", "java"))
    if os.path.isfile(java_path):
        return java_path
    else:
        return None


def get_jvm_runtime_information(jvm_version: str) -> JvmRuntimeInformation:
    """
    Returns some Information about a JVM Version

    Example:

    .. code:: python

        runtime_version = "java-runtime-gamma"
        information = minecraft_launcher_lib.runtime.get_jvm_runtime_information(runtime_version)
        print("Java version: " + information["name"])
        print("Release date: " + information["released"].isoformat())

    :param jvm_version: A JVM Version
    :raises VersionNotFound: The given JVM Version was not found
    :raises VersionNotFound: The given JVM Version is not available on this Platform
    :return: A Dict with Information
    """
    manifest_data: RuntimeListJson = requests.get(_JVM_MANIFEST_URL, headers={"user-agent": get_user_agent()}).json()
    platform_string = _get_jvm_platform_string()

    # Check if the jvm version exists
    if jvm_version not in manifest_data[platform_string]:
        raise VersionNotFound(jvm_version)

    if len(manifest_data[platform_string][jvm_version]) == 0:
        raise PlatformNotSupported()

    return {
        "name": manifest_data[platform_string][jvm_version][0]["version"]["name"],
        "released": datetime.datetime.fromisoformat(manifest_data[platform_string][jvm_version][0]["version"]["released"])
    }


def get_version_runtime_information(version: str, minecraft_directory: str | os.PathLike) -> VersionRuntimeInformation | None:
    """
    Returns information about the runtime used by a version

    Example:

    .. code:: python

        minecraft_version = "1.20"
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        information = minecraft_launcher_lib.runtime.get_version_runtime_information(minecraft_version, minecraft_directory)
        print("Name: " + information["name"])
        print("Java version: " + str(information["javaMajorVersion"]))

    :param minecraft_directory: The path to your Minecraft directory
    :raises VersionNotFound: The Minecraft version was not found
    :return: A Dict with Information. None if the version has no runtime information.
    """
    data = get_client_json(version, minecraft_directory)

    if "javaVersion" not in data:
        return None

    return {
        "name": data["javaVersion"]["component"],
        "javaMajorVersion": data["javaVersion"]["majorVersion"]
    }
