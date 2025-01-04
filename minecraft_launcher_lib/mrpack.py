# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"""
mrpack allows you to install Modpacks from the `Mrpack Format <https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack>`_.
You should also take a look at the :doc:`complete example </examples/Mrpack>`.
"""
from ._helper import download_file, empty, check_path_inside_minecraft_directory
from .types import MrpackInformation, MrpackInstallOptions, CallbackDict
from ._internal_types.mrpack_types import MrpackIndex, MrpackFile
from .install import install_minecraft_version
from .forge import install_forge_version
from .exceptions import VersionNotFound
from .fabric import install_fabric
from .quilt import install_quilt
import requests
import zipfile
import json
import os


def _filter_mrpack_files(file_list: list[MrpackFile], mrpack_install_options: MrpackInstallOptions) -> list[MrpackFile]:
    """
    Gets all Mrpack Files that should be installed
    """
    filtered_list: list[MrpackFile] = []
    for file in file_list:
        if "env" not in file:
            filtered_list.append(file)
            continue

        if file["env"]["client"] == "required":
            filtered_list.append(file)
        if file["env"]["client"] == "optional" and file["path"] in mrpack_install_options.get("optionalFiles", []):
            filtered_list.append(file)

    return filtered_list


def get_mrpack_information(path: str | os.PathLike) -> MrpackInformation:
    """
    Gets some Information from a .mrpack file

    Example:

    .. code:: python

        path = "/path/to/mrpack"
        information = minecraft_launcher_lib.mrpack.get_mrpack_information(path)
        print("Name: " + information["name"])
        print("Summary: " + information["summary"])

    :param path: The Path the the .mrpack file
    :type path: Union[str, os.PathLike]
    :return: The Information about the given Mrpack
    """
    with zipfile.ZipFile(path, "r") as zf:
        with zf.open("modrinth.index.json", "r") as f:
            index: MrpackIndex = json.load(f)

            information: MrpackInformation = {}  # type: ignore
            information["name"] = index["name"]
            information["summary"] = index.get("summary", "")
            information["versionId"] = index["versionId"]
            information["formatVersion"] = index["formatVersion"]
            information["minecraftVersion"] = index["dependencies"]["minecraft"]

            information["optionalFiles"] = []
            for file in index["files"]:
                if "env" not in file:
                    continue

                if file["env"]["client"] == "optional":
                    information["optionalFiles"].append(file["path"])

            return information


def install_mrpack(path: str | os.PathLike, minecraft_directory: str | os.PathLike, modpack_directory: str | os.PathLike | None = None, callback: CallbackDict | None = None, mrpack_install_options: MrpackInstallOptions | None = None) -> None:
    """
    Installs a .mrpack file

    ``mrpack_install_options`` is a dict. All Options are Optional.

    .. code:: python

        mrpack_install_options = {
            "optionalFiles": [], # List with all Optional files
            "skipDependenciesInstall": False # If you want to skip the Dependencies install. Only used for testing purposes.
        }

    Example:

    .. code:: python

        path = "/path/to/mrpack"
        minecraft_directory = minecraft_directory.utils.get_minecraft_directory()
        minecraft_launcher_lib.mrpack.install_mrpack(path, minecraft_directory)

    :param path: The Path the the .mrpack file
    :param minecraft_directory: he path to your Minecraft directory
    :param modpack_directory: If you want to install the Pack in another Directory than your Minecraft directory, set it here.
    :param callback: The same dict as for :func:`~minecraft_launcher_lib.install.install_minecraft_version`
    :param mrpack_install_options: Some Options to install the Pack (see below)
    :raises FileOutsideMinecraftDirectory: A File should be placed outside the given Minecraft directory
    """
    minecraft_directory = os.path.abspath(minecraft_directory)
    path = os.path.abspath(path)

    if modpack_directory is None:
        modpack_directory = minecraft_directory
    else:
        modpack_directory = os.path.abspath(modpack_directory)

    if callback is None:
        callback = {}

    if mrpack_install_options is None:
        mrpack_install_options = {}

    with zipfile.ZipFile(path, "r") as zf:
        with zf.open("modrinth.index.json", "r") as f:
            index: MrpackIndex = json.load(f)

        # Download the files
        callback.get("setStatus", empty)("Download mrpack files")
        file_list = _filter_mrpack_files(index["files"], mrpack_install_options)
        callback.get("setMax", empty)(len(file_list))
        for count, file in enumerate(file_list):
            full_path = os.path.abspath(os.path.join(modpack_directory, file["path"]))

            check_path_inside_minecraft_directory(modpack_directory, full_path)

            download_file(file["downloads"][0], full_path, sha1=file["hashes"]["sha1"], callback=callback)

            callback.get("setProgress", empty)(count + 1)

        # Extract the overrides
        callback.get("setStatus", empty)("Extract overrides")
        for zip_name in zf.namelist():
            # Check if the entry is in the overrides and if it is a file
            if (not zip_name.startswith("overrides/") and not zip_name.startswith("client-overrides/")) or zf.getinfo(zip_name).file_size == 0:
                continue

            # Remove the overrides at the start of the Name
            # We don't have removeprefix() in Python 3.8
            if zip_name.startswith("client-overrides/"):
                file_name = zip_name[len("client-overrides/"):]
            else:
                file_name = zip_name[len("overrides/"):]

            # Constructs the full Path
            full_path = os.path.abspath(os.path.join(modpack_directory, file_name))

            check_path_inside_minecraft_directory(modpack_directory, full_path)

            callback.get("setStatus", empty)(f"Extract {zip_name}]")

            try:
                os.makedirs(os.path.dirname(full_path))
            except FileExistsError:
                pass

            with open(full_path, "wb") as f:
                f.write(zf.read(zip_name))

        if mrpack_install_options.get("skipDependenciesInstall"):
            return

        # Install dependencies
        callback.get("setStatus", empty)("Installing Minecraft " + index["dependencies"]["minecraft"])
        install_minecraft_version(index["dependencies"]["minecraft"], minecraft_directory, callback=callback)

        if "forge" in index["dependencies"]:
            forge_version = None
            FORGE_DOWNLOAD_URL = "https://maven.minecraftforge.net/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
            for current_forge_version in (index["dependencies"]["minecraft"] + "-" + index["dependencies"]["forge"], index["dependencies"]["minecraft"] + "-" + index["dependencies"]["forge"] + "-" + index["dependencies"]["minecraft"]):
                if requests.head(FORGE_DOWNLOAD_URL.replace("{version}", current_forge_version)).status_code == 200:
                    forge_version = current_forge_version
                    break
            else:
                raise VersionNotFound(index["dependencies"]["forge"])

            callback.get("setStatus", empty)(f"Installing Forge {forge_version}")
            install_forge_version(forge_version, minecraft_directory, callback=callback)

        if "fabric-loader" in index["dependencies"]:
            callback.get("setStatus", empty)("Installing Fabric " + index["dependencies"]["fabric-loader"] + " for Minecraft " + index["dependencies"]["minecraft"])
            install_fabric(index["dependencies"]["minecraft"], minecraft_directory, loader_version=index["dependencies"]["fabric-loader"], callback=callback)

        if "quilt-loader" in index["dependencies"]:
            callback.get("setStatus", empty)("Installing Quilt " + index["dependencies"]["quilt-loader"] + " for Minecraft " + index["dependencies"]["minecraft"])
            install_quilt(index["dependencies"]["minecraft"], minecraft_directory, loader_version=index["dependencies"]["quilt-loader"], callback=callback)


def get_mrpack_launch_version(path: str | os.PathLike) -> str:
    """
    Returns that Version that needs to be used with :func:`~minecraft_launcher_lib.command.get_minecraft_command`.

    Example:

    .. code:: python

        path = "/path/to/mrpack"
        print("Launch version: " + minecraft_launcher_lib.mrpack.get_mrpack_launch_version(path))

    :param path: The Path the the .mrpack file
    :return: The version
    """
    with zipfile.ZipFile(path, "r") as zf:
        with zf.open("modrinth.index.json", "r") as f:
            index: MrpackIndex = json.load(f)

            if "forge" in index["dependencies"]:
                return index["dependencies"]["minecraft"] + "-forge-" + index["dependencies"]["forge"]
            elif "fabric-loader" in index["dependencies"]:
                return "fabric-loader-" + index["dependencies"]["fabric-loader"] + "-" + index["dependencies"]["minecraft"]
            elif "quilt-loader" in index["dependencies"]:
                return "quilt-loader-" + index["dependencies"]["quilt-loader"] + "-" + index["dependencies"]["minecraft"]
            else:
                return index["dependencies"]["minecraft"]
