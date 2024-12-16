# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"install allows you to install minecraft."
from ._helper import download_file, parse_rule_list, inherit_json, empty, get_user_agent, check_path_inside_minecraft_directory
from ._internal_types.shared_types import ClientJson, ClientJsonLibrary
from .natives import extract_natives_file, get_natives
from ._internal_types.install_types import AssetsJson
from concurrent.futures import ThreadPoolExecutor
from .runtime import install_jvm_runtime
from .exceptions import VersionNotFound
from .types import CallbackDict
import requests
import shutil
import json
import os

__all__ = ["install_minecraft_version"]


def install_libraries(
        id: str,
        libraries: list[ClientJsonLibrary],
        path: str, callback: CallbackDict,
        max_workers: int | None = None,) -> None:
    """
    Install all libraries
    """
    session = requests.session()
    callback.get("setStatus", empty)("Download Libraries")
    callback.get("setMax", empty)(len(libraries) - 1)

    def download_library(
            i: ClientJsonLibrary,) -> None:
        """Download the single library."""
        # Check, if the rules allow this lib for the current system
        if "rules" in i and not parse_rule_list(i["rules"], {}):
            return

        # Turn the name into a path
        current_path = os.path.join(path, "libraries")
        if "url" in i:
            if i["url"].endswith("/"):
                download_url = i["url"][:-1]
            else:
                download_url = i["url"]
        else:
            download_url = "https://libraries.minecraft.net"

        try:
            lib_path, name, version = i["name"].split(":")[0:3]
        except ValueError:
            return

        for lib_part in lib_path.split("."):
            current_path = os.path.join(current_path, lib_part)
            download_url = f"{download_url}/{lib_part}"

        try:
            version, fileend = version.split("@")
        except ValueError:
            fileend = "jar"

        jar_filename = f"{name}-{version}.{fileend}"
        download_url = f"{download_url}/{name}/{version}"
        current_path = os.path.join(current_path, name, version)
        native = get_natives(i)

        # Check if there is a native file
        if native != "":
            jar_filename_native = f"{name}-{version}-{native}.jar"
        jar_filename = f"{name}-{version}.{fileend}"
        download_url = f"{download_url}/{jar_filename}"

        # Try to download the lib
        try:
            download_file(download_url, os.path.join(current_path, jar_filename), callback=callback, session=session, minecraft_directory=path)
        except Exception:
            pass

        if "downloads" not in i:
            if "extract" in i:
                extract_natives_file(os.path.join(current_path, jar_filename_native), os.path.join(path, "versions", id, "natives"), i["extract"])
            return

        if "artifact" in i["downloads"] and i["downloads"]["artifact"]["url"] != "" and "path" in i["downloads"]["artifact"]:
            download_file(i["downloads"]["artifact"]["url"], os.path.join(path, "libraries", i["downloads"]["artifact"]["path"]), callback, sha1=i["downloads"]["artifact"]["sha1"], session=session, minecraft_directory=path)
        if native != "":
            download_file(i["downloads"]["classifiers"][native]["url"], os.path.join(current_path, jar_filename_native), callback, sha1=i["downloads"]["classifiers"][native]["sha1"], session=session, minecraft_directory=path)  # type: ignore
            extract_natives_file(os.path.join(current_path, jar_filename_native), os.path.join(path, "versions", id, "natives"), i.get("extract", {"exclude": []}))

    count = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit task for every library
        futures = [executor.submit(download_library, i) for i in libraries]
        for future in futures:
            # Wait until the task is completed
            future.result()
            count += 1
            callback.get("setProgress", empty)(count)


def install_assets(
        data: ClientJson,
        path: str,
        callback: CallbackDict,
        max_workers: int | None = None,) -> None:
    """
    Install all assets
    """
    # Old versions don't have this
    if "assetIndex" not in data:
        return

    callback.get("setStatus", empty)("Download Assets")
    session = requests.session()

    # Download all assets
    download_file(data["assetIndex"]["url"], os.path.join(path, "assets", "indexes", data["assets"] + ".json"), callback, sha1=data["assetIndex"]["sha1"], session=session)
    with open(os.path.join(path, "assets", "indexes", data["assets"] + ".json")) as f:
        assets_data: AssetsJson = json.load(f)

    # The assets has a hash. e.g. c4dbabc820f04ba685694c63359429b22e3a62b5
    # With this hash, it can be download from https://resources.download.minecraft.net/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    # And saved at assets/objects/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    assets = set(val["hash"] for val in assets_data["objects"].values())
    callback.get("setMax", empty)(len(assets) - 1)
    count = 0

    def download_asset(filehash: str) -> None:
        """Download the single asset file."""
        download_file("https://resources.download.minecraft.net/" + filehash[:2] + "/" + filehash, os.path.join(path, "assets", "objects", filehash[:2], filehash), callback, sha1=filehash, session=session, minecraft_directory=path)

    # Use a ThreadPoolExecutor to download assets concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit task for every library
        futures = [executor.submit(download_asset, filehash) for filehash in assets]
        for future in futures:
            # Wait until the task is completed
            future.result()
            count += 1
            callback.get("setProgress", empty)(count)


def do_version_install(versionid: str, path: str, callback: CallbackDict, url: str | None = None, sha1: str | None = None) -> None:
    """
    Installs the given version
    """
    # Download and read versions.json
    if url:
        download_file(url, os.path.join(path, "versions", versionid, versionid + ".json"), callback, sha1=sha1, minecraft_directory=path)

    with open(os.path.join(path, "versions", versionid, versionid + ".json"), "r", encoding="utf-8") as f:
        versiondata: ClientJson = json.load(f)

    # For Forge
    if "inheritsFrom" in versiondata:
        try:
            install_minecraft_version(versiondata["inheritsFrom"], path, callback=callback)
        except VersionNotFound:
            pass
        versiondata = inherit_json(versiondata, path)

    install_libraries(versiondata["id"], versiondata["libraries"], path, callback)
    install_assets(versiondata, path, callback)

    # Download logging config
    if "logging" in versiondata:
        if len(versiondata["logging"]) != 0:
            logger_file = os.path.join(path, "assets", "log_configs", versiondata["logging"]["client"]["file"]["id"])
            download_file(versiondata["logging"]["client"]["file"]["url"], logger_file, callback, sha1=versiondata["logging"]["client"]["file"]["sha1"], minecraft_directory=path)

    # Download minecraft.jar
    if "downloads" in versiondata:
        download_file(versiondata["downloads"]["client"]["url"], os.path.join(path, "versions", versiondata["id"], versiondata["id"] + ".jar"), callback, sha1=versiondata["downloads"]["client"]["sha1"], minecraft_directory=path)

    # Need to copy jar for old forge versions
    if not os.path.isfile(os.path.join(path, "versions", versiondata["id"], versiondata["id"] + ".jar")) and "inheritsFrom" in versiondata:
        inherits_from = versiondata["inheritsFrom"]
        inherit_path = os.path.join(path, "versions", inherits_from, f"{inherits_from}.jar")
        check_path_inside_minecraft_directory(path, inherit_path)
        shutil.copyfile(os.path.join(path, "versions", versiondata["id"], versiondata["id"] + ".jar"), inherit_path)

    # Install java runtime if needed
    if "javaVersion" in versiondata:
        callback.get("setStatus", empty)("Install java runtime")
        install_jvm_runtime(versiondata["javaVersion"]["component"], path, callback=callback)

    callback.get("setStatus", empty)("Installation complete")


def install_minecraft_version(versionid: str, minecraft_directory: str | os.PathLike, callback: CallbackDict | None = None) -> None:
    """
    Installs a minecraft version into the given path. e.g. ``install_version("1.14", "/tmp/minecraft")``. Use :func:`~minecraft_launcher_lib.utils.get_minecraft_directory` to get the default Minecraft directory.

    :param versionid: The Minecraft version
    :param minecraft_directory: The path to your Minecraft directory
    :param callback: Some functions that are called to monitor the progress (see below)
    :raises VersionNotFound: The Minecraft version was not found
    :raises FileOutsideMinecraftDirectory: A File should be placed outside the given Minecraft directory

    ``callback`` is a dict with functions that are called with arguments to get the progress. You can use it to show the progress to the user.

    .. code:: python

        callback = {
            "setStatus": some_function, # This function is called to set a text
            "setProgress" some_function, # This function is called to set the progress.
            "setMax": some_function, # This function is called to set to max progress.
        }

    Files that are already exists will not be replaced.
    """
    if isinstance(minecraft_directory, os.PathLike):
        minecraft_directory = str(minecraft_directory)
    if callback is None:
        callback = {}
    if os.path.isfile(os.path.join(minecraft_directory, "versions", versionid, f"{versionid}.json")):
        do_version_install(versionid, minecraft_directory, callback)
        return
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json", headers={"user-agent": get_user_agent()}).json()
    for i in version_list["versions"]:
        if i["id"] == versionid:
            do_version_install(versionid, minecraft_directory, callback, url=i["url"], sha1=i["sha1"])
            return
    raise VersionNotFound(versionid)
