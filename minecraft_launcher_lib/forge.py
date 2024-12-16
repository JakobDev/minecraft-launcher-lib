# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"""
.. note::
    Before using this module, please read this comment from the forge developers:

    .. code:: text

        Please do not automate the download and installation of Forge.
        Our efforts are supported by ads from the download page.
        If you MUST automate this, please consider supporting the project through https://www.patreon.com/LexManos/

    It's your choice, if you want to respect that and support forge.

forge contains functions for dealing with the Forge modloader
"""
from ._helper import download_file, get_library_path, get_jar_mainclass, parse_maven_metadata, empty, extract_file_from_zip, get_classpath_separator
from .install import install_minecraft_version, install_libraries
from ._internal_types.forge_types import ForgeInstallProfile
from .exceptions import VersionNotFound
from .types import CallbackDict
import subprocess
import tempfile
import zipfile
import json
import os

__all__ = ["install_forge_version", "run_forge_installer", "list_forge_versions", "find_forge_version", "is_forge_version_valid", "supports_automatic_install", "forge_to_installed_version"]


def forge_processors(data: ForgeInstallProfile, minecraft_directory: str | os.PathLike, lzma_path: str, installer_path: str, callback: CallbackDict, java: str) -> None:
    """
    Run the processors of the install_profile.json
    """
    path = str(minecraft_directory)

    argument_vars = {"{MINECRAFT_JAR}": os.path.join(path, "versions", data["minecraft"], data["minecraft"] + ".jar")}
    for data_key, data_value in data["data"].items():
        if data_value["client"].startswith("[") and data_value["client"].endswith("]"):
            argument_vars["{" + data_key + "}"] = get_library_path(data_value["client"][1:-1], path)
        else:
            argument_vars["{" + data_key + "}"] = data_value["client"]

    with tempfile.TemporaryDirectory() as root_path:
        argument_vars["{INSTALLER}"] = installer_path
        argument_vars["{BINPATCH}"] = lzma_path
        argument_vars["{ROOT}"] = root_path
        argument_vars["{SIDE}"] = "client"

        classpath_seperator = get_classpath_separator()

        callback.get("setMax", empty)(len(data["processors"]))

        for count, i in enumerate(data["processors"]):
            if "client" not in i.get("sides", ["client"]):
                # Skip server side only processors
                continue
            callback.get("setStatus", empty)("Running processor " + i["jar"])
            # Get the classpath
            classpath = ""
            for c in i["classpath"]:
                classpath = classpath + get_library_path(c, path) + classpath_seperator
            classpath = classpath + get_library_path(i["jar"], path)
            mainclass = get_jar_mainclass(get_library_path(i["jar"], path))
            command = [java, "-cp", classpath, mainclass]
            for c in i["args"]:
                var = argument_vars.get(c, c)
                if var.startswith("[") and var.endswith("]"):
                    command.append(get_library_path(var[1:-1], path))
                else:
                    command.append(var)
            for argument_key, argument_value in argument_vars.items():
                for pos in range(len(command)):
                    command[pos] = command[pos].replace(argument_key, argument_value)
            subprocess.run(command)
            callback.get("setProgress", empty)(count)


def install_forge_version(versionid: str, path: str | os.PathLike, callback: CallbackDict | None = None, java: str | os.PathLike | None = None) -> None:
    """
    Installs the given Forge version

    :param versionid: A Forge Version. You can get a List of Forge versions using :func:`list_forge_versions`
    :param path: The path to your Minecraft directory
    :param callback: The same dict as for :func:`~minecraft_launcher_lib.install.install_minecraft_version`
    :param java: A Path to a custom Java executable

    Raises a :class:`~minecraft_launcher_lib.exceptions.VersionNotFound` exception when the given forge version is not found
    """
    if callback is None:
        callback = {}

    FORGE_DOWNLOAD_URL = "https://maven.minecraftforge.net/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"

    with tempfile.TemporaryDirectory(prefix="minecraft-launcher-lib-forge-install-") as tempdir:
        installer_path = os.path.join(tempdir, "installer.jar")

        if not download_file(FORGE_DOWNLOAD_URL.format(version=versionid), installer_path, callback):
            raise VersionNotFound(versionid)

        zf = zipfile.ZipFile(installer_path, "r")

        # Read the install_profile.json
        with zf.open("install_profile.json", "r") as f:
            version_content = f.read()

        version_data: ForgeInstallProfile = json.loads(version_content)
        forge_version_id = version_data["version"] if "version" in version_data else version_data["install"]["version"]
        minecraft_version = version_data["minecraft"] if "minecraft" in version_data else version_data["install"]["minecraft"]

        # Make sure, the base version is installed
        install_minecraft_version(minecraft_version, path, callback=callback)

        # Install all needed libs from install_profile.json
        if "libraries" in version_data:
            install_libraries(minecraft_version, version_data["libraries"], str(path), callback)

        # Extract the client.json
        version_json_path = os.path.join(path, "versions", forge_version_id, forge_version_id + ".json")
        try:
            extract_file_from_zip(zf, "version.json", version_json_path, minecraft_directory=path)
        except KeyError:
            if "versionInfo" in version_data:
                with open(version_json_path, "w", encoding="utf-8") as f:
                    json.dump(version_data["versionInfo"], f, ensure_ascii=False, indent=4)

        # Extract forge libs from the installer
        forge_lib_path = os.path.join(path, "libraries", "net", "minecraftforge", "forge", versionid)
        try:
            extract_file_from_zip(zf, "maven/net/minecraftforge/forge/{version}/forge-{version}-universal.jar".format(version=versionid), os.path.join(forge_lib_path, "forge-" + versionid + "-universal.jar"), minecraft_directory=path)
        except KeyError:
            pass

        try:
            extract_file_from_zip(zf, "forge-{version}-universal.jar".format(version=versionid), os.path.join(forge_lib_path, f"forge-{versionid}.jar"), minecraft_directory=path)
        except KeyError:
            pass

        try:
            extract_file_from_zip(zf, f"maven/net/minecraftforge/forge/{versionid}/forge-{versionid}.jar", os.path.join(forge_lib_path, f"forge-{versionid}.jar"), minecraft_directory=path)
        except KeyError:
            pass

        # Extract the client.lzma
        lzma_path = os.path.join(tempdir, "client.lzma")
        try:
            extract_file_from_zip(zf, "data/client.lzma", lzma_path)
        except KeyError:
            pass

        zf.close()

        # Install the rest with the vanilla function
        install_minecraft_version(forge_version_id, str(path), callback=callback)

        # Run the processors
        if "processors" in version_data:
            forge_processors(version_data, str(path), lzma_path, installer_path, callback, "java" if java is None else str(java))


def run_forge_installer(version: str, java: str | os.PathLike | None = None) -> None:
    """
    Run the forge installer of the given forge version

    :param version: A Forge Version. You can get a List of Forge versions using :func:`list_forge_versions`
    :param java: A Path to a custom Java executable
    """
    FORGE_DOWNLOAD_URL = "https://maven.minecraftforge.net/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"

    with tempfile.TemporaryDirectory(prefix="minecraft-launcher-lib-forge-installer-") as tempdir:
        installer_path = os.path.join(tempdir, "installer.jar")

        if not download_file(FORGE_DOWNLOAD_URL.format(version=version), installer_path, {}, overwrite=True):
            raise VersionNotFound(version)

        subprocess.run(["java" if java is None else str(java), "-jar", installer_path], check=True, cwd=tempdir)


def list_forge_versions() -> list[str]:
    """
    Returns a list of all forge versions
    """
    MAVEN_METADATA_URL = "https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml"
    return parse_maven_metadata(MAVEN_METADATA_URL)["versions"]


def find_forge_version(vanilla_version: str) -> str | None:
    """
    Find the latest forge version that is compatible to the given vanilla version

    :param vanilla_version: A vanilla Minecraft version
    """
    version_list = list_forge_versions()
    for i in version_list:
        version_split = i.split("-")
        if version_split[0] == vanilla_version:
            return i
    return None


def is_forge_version_valid(forge_version: str) -> bool:
    """
    Checks if a forge version is valid

    :param forge_version: A Forge Version
    """
    forge_version_list = list_forge_versions()
    return forge_version in forge_version_list


def supports_automatic_install(forge_version: str) -> bool:
    """
    Checks if install_forge_version() supports the given forge version

    :param forge_version: A Forge Version
    """
    try:
        vanilla_version, forge = forge_version.split("-")
        version_split = vanilla_version.split(".")
        version_number = int(version_split[1])
        if version_number >= 13:
            return True
        else:
            return False
    except Exception:
        return False


def forge_to_installed_version(forge_version: str) -> str:
    """
    Returns the Version under which Forge will be installed from the given Forge version.

    :param forge_version: A Forge Version

    Raises a ValueError if the Version is invalid.
    """
    try:
        vanilla_part, forge_part = forge_version.split("-")
        return f"{vanilla_part}-forge-{forge_part}"
    except ValueError:
        raise ValueError(f"{forge_version} is not a valid forge version") from None
