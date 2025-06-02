# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from abc import ABC, abstractmethod
from ..types import CallbackDict


class ModLoaderBase(ABC):
    """
    This is a abstract base class for a mod loader
    """
    @abstractmethod
    def get_id(self) -> str:
        "Returns the ID of the mod loader"
        raise NotImplementedError()

    @abstractmethod
    def get_name(self) -> str:
        "Returns the name of the mod loader"
        raise NotImplementedError()

    @abstractmethod
    def get_minecraft_versions(self, stable_only: bool) -> list[str]:
        "Returns a list of all Minecraft versions the loader supports"
        raise NotImplementedError()

    @abstractmethod
    def get_loader_versions(self, minecraft_version: str, stable_only: bool) -> list[str]:
        "Returns all versions of the mod loader"
        raise NotImplementedError()

    @abstractmethod
    def get_installer_url(self, minecraft_version: str, loader_version: str) -> str:
        "Returns the URL to the installer"
        raise NotImplementedError()

    @abstractmethod
    def get_installed_version(self, minecraft_version: str, loader_version: str) -> str:
        "Get the version under which the mod loader is installed"
        raise NotImplementedError()

    @abstractmethod
    def install(self, minecraft_version: str, minecraft_directory: str, callback: CallbackDict, java: str, loader_version: str) -> None:
        "Installs the mod loader"
        raise NotImplementedError()
