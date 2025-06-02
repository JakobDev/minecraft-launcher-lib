# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from .._helper import get_requests_response_cache, parse_maven_metadata
from ._base import ModLoaderBase


class FabricQuiltBase(ModLoaderBase):
    """"
    Fabric and Quilt works in many things the same.
    This class provides those shared functions
    """
    def __init__(self) -> None:
        self._maven_url = ""
        self._game_url = ""
        self._loader_url = ""
        self._loader_name = ""

    def get_minecraft_versions(self, stable_only: bool) -> list[str]:
        "Implements get_minecraft_versions() for Fabric/Quilt"
        version_list: list[str] = []

        for version in get_requests_response_cache(self._game_url).json():
            if not version["stable"] and stable_only:
                continue

            version_list.append(version["version"])

        return version_list

    def get_loader_versions(self, minecraft_version: str, stable_only: bool) -> list[str]:
        "Implements get_loader_versions() for Fabric/Quilt"
        version_list: list[str] = []

        for current_version in get_requests_response_cache(self._loader_url).json():
            version = current_version["version"]

            if (not current_version.get("stable", True) or "beta" in version) and stable_only:
                continue

            version_list.append(version)

        return version_list

    def get_installer_url(self, minecraft_version: str, loader_version: str) -> str:
        "Implements get_installer_url() for Fabric/Quilt"
        installer_version = parse_maven_metadata(f"{self._maven_url}/maven-metadata.xml")["latest"]
        return f"{self._maven_url}/{installer_version}/{self._loader_name}-installer-{installer_version}.jar"

    def get_installed_version(self, minecraft_version: str, loader_version: str) -> str:
        "Implements get_installed_version() for Fabric/Quilt"
        return f"{self._loader_name}-loader-{loader_version}-{minecraft_version}"
