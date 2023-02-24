"""
quilt contains functions for dealing with the `Quilt modloader <https://quiltmc.org>`_.

You may have noticed, that the Functions are the same as in the :doc:`fabric` module.
That's because Quilt is a Fork of Fabric. This module behaves exactly the same as the fabric module.
"""
from ._helper import download_file, get_requests_response_cache, parse_maven_metadata, empty
from .exceptions import VersionNotFound, UnsupportedVersion, ExternalProgramError
from .types import QuiltMinecraftVersion, QuiltLoader, CallbackDict
from .install import install_minecraft_version
from typing import List, Optional, Union
from .utils import is_version_valid
import subprocess
import tempfile
import random
import os


def get_all_minecraft_versions() -> List[QuiltMinecraftVersion]:
    """
    Returns all available Minecraft Versions for Quilt
    """
    QUILT_MINECARFT_VERSIONS_URL = "https://meta.quiltmc.org/v3/versions/game"
    return get_requests_response_cache(QUILT_MINECARFT_VERSIONS_URL).json()


def get_stable_minecraft_versions() -> List[str]:
    """
    Returns a list which only contains the stable Minecraft versions that supports Quilt
    """
    minecraft_versions = get_all_minecraft_versions()
    stable_versions = []
    for i in minecraft_versions:
        if i["stable"] is True:
            stable_versions.append(i["version"])
    return stable_versions


def get_latest_minecraft_version() -> str:
    """
    Returns the latest unstable Minecraft versions that supports Quilt. This could be a snapshot.
    """
    minecraft_versions = get_all_minecraft_versions()
    return minecraft_versions[0]["version"]


def get_latest_stable_minecraft_version() -> str:
    """
    Returns the latest stable Minecraft version that supports Quilt
    """
    stable_versions = get_stable_minecraft_versions()
    return stable_versions[0]


def is_minecraft_version_supported(version: str) -> bool:
    """
    Checks if a Minecraft version supported by Quilt

    :param version: A vanilla version
    """
    minecraft_versions = get_all_minecraft_versions()
    for i in minecraft_versions:
        if i["version"] == version:
            return True
    return False


def get_all_loader_versions() -> List[QuiltLoader]:
    """
    Returns all loader versions
    """
    QUILT_LOADER_VERSIONS_URL = "https://meta.quiltmc.org/v3/versions/loader"
    return get_requests_response_cache(QUILT_LOADER_VERSIONS_URL).json()


def get_latest_loader_version() -> str:
    """
    Get the latest loader version
    """
    loader_versions = get_all_loader_versions()
    return loader_versions[0]["version"]


def get_latest_installer_version() -> str:
    """
    Returns the latest installer version
    """
    QUILT_INSTALLER_MAVEN_URL = "https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer/maven-metadata.xml"
    return parse_maven_metadata(QUILT_INSTALLER_MAVEN_URL)["latest"]


def install_quilt(minecraft_version: str, minecraft_directory: Union[str, os.PathLike], loader_version: Optional[str] = None, callback: Optional[CallbackDict] = None, java: Optional[Union[str, os.PathLike]] = None) -> None:
    """
    Installs the Quilt modloader.

    :param minecraft_version: A vanilla version that is supported by Quilt
    :param minecraft_directory: The path to your Minecraft directory
    :param loader_version: The Quilt loader version. If not given it will use the latest
    :param callback: The same dict as for :func:`~minecraft_launcher_lib.install.install_minecraft_version`
    :param java: A Path to a custom Java executable
    :raises UnsupportedVersion: The given Minecraft version is not supported by Quilt
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
    installer_download_url = f"https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer/{installer_version}/quilt-installer-{installer_version}.jar"

    # Generate a temporary path for downloading the installer
    installer_path = os.path.join(tempfile.gettempdir(), f"quilt-installer-{random.randrange(100,10000)}.tmp")

    try:
        # Download the installer
        download_file(installer_download_url, installer_path, callback=callback)

        # Run the installer
        callback.get("setStatus", empty)("Running quilt installer")
        command = ["java" if java is None else str(java), "-jar", installer_path, "install", "client", minecraft_version, loader_version, f"--install-dir={path}", "--no-profile"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise ExternalProgramError(command, result.stdout, result.stderr)
    finally:
        # Delete the installer we don't need them anymore
        try:
            os.remove(installer_path)
        except Exception:
            pass

    # Install all libs of quilt
    quilt_minecraft_version = f"quilt-loader-{loader_version}-{minecraft_version}"
    install_minecraft_version(quilt_minecraft_version, path, callback=callback)
