# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"""
This module offers a standardized way to access the functions of various mod loaders.
You should take a look at the :doc:`tutorial </tutorial/install_mod_loader>` before using this module.

.. versionadded:: 8.0
"""
from ._fabric import Fabric
from ._quilt import Quilt
from ._base import ModLoaderBase
from ..types import CallbackDict
from ..exceptions import VersionNotFound, UnsupportedVersion
from ..install import install_minecraft_version
from ._forge import Forge
from ..utils import is_version_valid
from ._neoforge import Neoforge
import os

__all__ = ["get_mod_loader", "list_mod_loader", "ModLoader"]

_MOD_LOADER_LIST: list[ModLoaderBase] = [
    Forge(),
    Neoforge(),
    Fabric(),
    Quilt(),
]


class ModLoader():
    """
    This class offers a standardized way to access the functions of various mod loaders.
    You can obtain an instance of this class by calling :func:`~minecraft_launcher_lib.mod_loader.get_mod_loader`.
    You should not create a new instance of this class on your own.
    """
    def __init__(self, base: ModLoaderBase) -> None:
        self._base = base

    def get_id(self) -> str:
        """
        Returns the ID of the mod loader

        Example:

        .. code:: python

            mod_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            print(mod_loader.get_id())
        """
        return self._base.get_id()

    def get_name(self) -> str:
        """
        Returns the name of the mod loader

        Example:

        .. code:: python

            mod_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            print(mod_loader.get_name())
        """
        return self._base.get_name()

    def get_minecraft_versions(self, stable_only: bool) -> list[str]:
        """
        Returns a list of all Minecraft versions that the mod loader supports.

        Example:

        .. code:: python

            mod_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            for version in mod_loader.get_minecraft_versions(True):
                print(version)

        :param stable_only: Only return stable versions and not snapshots. This parameter is not supported by every mod loader.
        """
        return self._base.get_minecraft_versions(stable_only)

    def is_minecraft_version_supported(self, minecraft_version: str) -> bool:
        """
        Checks if the given minecraft version is supported by the mod loader.

        Example:

        .. code:: python

            version = "1.21"
            mod_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            if mod_loader.is_minecraft_version_supported(version):
                print(f"{version} is supported")
            else:
                print(f"{version} is not supported")

        :param minecraft_version: A Minecraft version
        """
        return minecraft_version in self.get_minecraft_versions(False)

    def get_loader_versions(self, minecraft_version: str, stable_only: bool) -> list[str]:
        """
        Returns all loader versions from newest to oldest that exists for the given Minecraft version

        Example:

        .. code:: python

            version = "1.21"
            mod_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            loader_versions = mod_loader.get_loader_versions(version, True)
            for current_version in loader_versions:
                print(current_version)

        :param minecraft_version: A Minecraft version.
        :param stable_only: Only return stable loader versions. This parameter is not supported by every mod loader.
        :return: A list of all loader versions
        """
        return self._base.get_loader_versions(minecraft_version, stable_only)

    def get_latest_loader_version(self, minecraft_version: str) -> str:
        """
        Returns the latest loader version for the given Minecraft version.

        Example:

        .. code:: python

            version = "1.21"
            mod_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            latest_loader_version = mod_loader.get_latest_loader_version(version)
            print(latest_loader_version)

        :param minecraft_version: A Minecraft version.
        :param stable_only: Only return stable loader versions. This parameter is not supported by every mod loader.
        :raises ~minecraft_launcher_lib.exceptions.UnsupportedVersion: The given Minecraft version is not supported by the mod loader.
        :return: The latest loader version
        """
        version_list = self.get_loader_versions(minecraft_version, True)
        if len(version_list) != 0:
            return version_list[0]

        version_list = self.get_loader_versions(minecraft_version, False)
        if len(version_list) != 0:
            return version_list[0]

        raise UnsupportedVersion(minecraft_version)

    def get_installed_version(self, minecraft_version: str, loader_version: str) -> str:
        """
        This returns the version under which the mod loader will be installed.
        It can be used with e.g :func:`~minecraft_launcher_lib.command.get_minecraft_command`.

        Example:

        .. code:: python

            vanilla_version = "1.21"
            loader_version = "0.16.14"
            mod_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            installed_version = mod_loader.get_installed_version(vanilla_version, loader_version)
            print(installed_version)

        :param minecraft_version: The vanilla version
        :param loader_version: The loader version
        :return: The installed version
        """
        return self._base.get_installed_version(minecraft_version, loader_version)

    def install(self, minecraft_version: str, minecraft_directory: str | os.PathLike, *, loader_version: str | None = None, callback: CallbackDict | None = None, java: str | os.PathLike | None = None) -> str:
        """
        Installs the mod loader for the given vanilla version.

        Example:

        .. code:: python

            vanilla_version = "1.21"
            minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
            mod_loader = mod_loader = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
            mod_loader.install(vanilla_version, minecraft_directory)

        :param minecraft_version: The vanilla Minecraft version for which to install the mod loader. If not installed, minecraft-launcher-lib will also install the vanilla version.
        :param minecraft_directory: The path to your Minecraft directory
        :param loader_version: The version of the mod loader as returned by :func:`~minecraft_launcher_lib.mod_loader.ModLoader.get_loader_versions`.If not set the latest one will be used.
        :param callback: See :doc:`/tutorial/get_installation_progress`
        :param java: If set use this Java executable to execute programs during the installation.
        :raises ~minecraft_launcher_lib.exceptions.VersionNotFound: An invalid minecraft version was passed.
        :raises ~minecraft_launcher_lib.exceptions.UnsupportedVersion: The given Minecraft version is not supported by the mod loader.
        :raises: CalledProcessError: The execution of a program failed.
        :return: The same as :func:`~minecraft_launcher_lib.mod_loader.ModLoader.get_installed_version`.
        """
        if not is_version_valid(minecraft_version, minecraft_directory):
            raise VersionNotFound(minecraft_version)

        if not self.is_minecraft_version_supported(minecraft_version):
            raise UnsupportedVersion(minecraft_version)

        if callback is None:
            callback = {}

        if java is None:
            java = "java"

        if loader_version is None:
            loader_version = self.get_latest_loader_version(minecraft_version)

        install_minecraft_version(minecraft_version, minecraft_directory, callback=callback)

        self._base.install(minecraft_version, str(minecraft_directory), callback, str(java), loader_version)

        installed_version = self.get_installed_version(minecraft_version, loader_version)

        install_minecraft_version(installed_version, minecraft_directory, callback=callback)

        return installed_version


def get_mod_loader(mod_loader_id: str, /) -> ModLoader:
    """
    Returns the mod loader with the given ID

    Example:

    .. code:: python

        fabric = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")

    :param mod_loader_id: the mod loader id
    :raises ValueError: An invalid ID was passed
    :return: The mod loader
    """
    for current_loader in _MOD_LOADER_LIST:
        if current_loader.get_id() == mod_loader_id:
            return ModLoader(current_loader)

    raise ValueError(f"mod loader {mod_loader_id} not found")


def list_mod_loader() -> list[str]:
    """
    Returns a list of all available mod loader ids

    Example:

    .. code:: python

        id_list = minecraft_launcher_lib.mod_loader.list_mod_loader()
        for current_id in id_list:
            print(current_id)

    :return: A list of all ids
    """
    id_list: list[str] = []

    for current_loader in _MOD_LOADER_LIST:
        id_list.append(current_loader.get_id())

    return id_list
