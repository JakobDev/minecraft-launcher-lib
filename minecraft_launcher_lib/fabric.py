# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"fabric contains functions for dealing with the `Fabric modloader <https://fabricmc.net/>`_."
from ._helper import download_file, get_requests_response_cache, parse_maven_metadata, empty
from .exceptions import VersionNotFound, UnsupportedVersion, ExternalProgramError
from .types import FabricMinecraftVersion, FabricLoader, CallbackDict
from .install import install_minecraft_version
from .utils import is_version_valid
import subprocess
import tempfile
import os


def get_all_minecraft_versions() -> list[FabricMinecraftVersion]:
    """
    Returns all available Minecraft Versions for Fabric

    Example:

    .. code:: python

        for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions():
            print(version["version"])
    """
    FABRIC_MINECARFT_VERSIONS_URL = "https://meta.fabricmc.net/v2/versions/game"
    return get_requests_response_cache(FABRIC_MINECARFT_VERSIONS_URL).json()


def get_stable_minecraft_versions() -> list[str]:
    """
    Returns a list which only contains the stable Minecraft versions that supports Fabric

    Example:

    .. code:: python

        for version in minecraft_launcher_lib.fabric.get_stable_minecraft_versions():
            print(version)
    """
    minecraft_versions = get_all_minecraft_versions()
    stable_versions = []
    for i in minecraft_versions:
        if i["stable"] is True:
            stable_versions.append(i["version"])
    return stable_versions


def get_latest_minecraft_version() -> str:
    """
    Returns the latest unstable Minecraft versions that supports Fabric. This could be a snapshot.

    Example:

    .. code:: python

        print("Latest Minecraft version: " + minecraft_launcher_lib.fabric.get_latest_minecraft_version())
    """
    minecraft_versions = get_all_minecraft_versions()
    return minecraft_versions[0]["version"]


def get_latest_stable_minecraft_version() -> str:
    """
    Returns the latest stable Minecraft version that supports Fabric

    Example:

    .. code:: python

        print("Latest stable Minecraft version: " + minecraft_launcher_lib.fabric.get_latest_stable_minecraft_version())
    """
    stable_versions = get_stable_minecraft_versions()
    return stable_versions[0]


def is_minecraft_version_supported(version: str) -> bool:
    """
    Checks if a Minecraft version supported by Fabric

    Example:

    .. code:: python

        version = "1.20"
        if minecraft_launcher_lib.fabric.is_minecraft_version_supported(version):
            print(f"{version} is supported by fabric")
        else:
            print(f"{version} is not supported by fabric")

    :param version: A vanilla version
    """
    minecraft_versions = get_all_minecraft_versions()
    for i in minecraft_versions:
        if i["version"] == version:
            return True
    return False


def get_all_loader_versions() -> list[FabricLoader]:
    """
    Returns all loader versions

    Example:

    .. code:: python

        for version in minecraft_launcher_lib.fabric.get_all_loader_versions():
            print(version["version"])
    """
    FABRIC_LOADER_VERSIONS_URL = "https://meta.fabricmc.net/v2/versions/loader"
    return get_requests_response_cache(FABRIC_LOADER_VERSIONS_URL).json()


def get_latest_loader_version() -> str:
    """
    Get the latest loader version

    Example:

    .. code:: python

        print("Latest loader version: " + minecraft_launcher_lib.fabric.get_latest_loader_version())
    """
    loader_versions = get_all_loader_versions()
    return loader_versions[0]["version"]


def get_latest_installer_version() -> str:
    """
    Returns the latest installer version

    Example:

    .. code:: python

        print("Latest installer version: " + minecraft_launcher_lib.fabric.get_latest_installer_version())
    """
    FABRIC_INSTALLER_MAVEN_URL = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/maven-metadata.xml"
    return parse_maven_metadata(FABRIC_INSTALLER_MAVEN_URL)["latest"]


def install_fabric(minecraft_version: str, minecraft_directory: str | os.PathLike, loader_version: str | None = None, callback: CallbackDict | None = None, java: str | os.PathLike | None = None) -> None:
    """
    Installs the Fabric modloader.
    For more information take a look at the :doc:`tutorial </tutorial/install_fabric>`.

    Example:

    .. code:: python

        minecraft_version = "1.20"
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
        minecraft_launcher_lib.fabric.install_fabric(minecraft_version, minecraft_directory)

    :param minecraft_version: A vanilla version that is supported by Fabric
    :param minecraft_directory: The path to your Minecraft directory
    :param loader_version: The fabric loader version. If not given it will use the latest
    :param callback: The same dict as for :func:`~minecraft_launcher_lib.install.install_minecraft_version`
    :param java: A Path to a custom Java executable
    :raises VersionNotFound: The given Minecraft does not exists
    :raises UnsupportedVersion: The given Minecraft version is not supported by Fabric
    """
    path = str(minecraft_directory)
    if not callback:
        callback = {}

    # Check if the given version exists
    if not is_version_valid(minecraft_version, minecraft_directory):
        raise VersionNotFound(minecraft_version)

    # Check if the given Minecraft version supported
    if not is_minecraft_version_supported(minecraft_version):
        raise UnsupportedVersion(minecraft_version)

    # Get latest loader version if not given
    if not loader_version:
        loader_version = get_latest_loader_version()

    # Make sure the Minecraft version is installed
    install_minecraft_version(minecraft_version, path, callback=callback)

    # Get installer version
    installer_version = get_latest_installer_version()
    installer_download_url = f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/{installer_version}/fabric-installer-{installer_version}.jar"

    with tempfile.TemporaryDirectory(prefix="minecraft-launcher-lib-fabric-install-") as tempdir:
        installer_path = os.path.join(tempdir, "fabric-installer.jar")

        # Download the installer
        download_file(installer_download_url, installer_path, callback=callback, overwrite=True)

        # Run the installer see https://fabricmc.net/wiki/install#cli_installation
        callback.get("setStatus", empty)("Running fabric installer")
        command = ["java" if java is None else str(java), "-jar", installer_path, "client", "-dir", path, "-mcversion", minecraft_version, "-loader", loader_version, "-noprofile", "-snapshot"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise ExternalProgramError(command, result.stdout, result.stderr)

    # Install all libs of fabric
    fabric_minecraft_version = f"fabric-loader-{loader_version}-{minecraft_version}"
    install_minecraft_version(fabric_minecraft_version, path, callback=callback)
