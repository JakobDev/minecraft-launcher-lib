# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from ..vanilla_launcher import do_vanilla_launcher_profiles_exists, create_empty_vanilla_launcher_profiles_file
from .._helper import get_requests_response_cache, download_file, empty, SUBPROCESS_STARTUP_INFO
from ._base import ModLoaderBase
from ..types import CallbackDict
import subprocess
import tempfile
import re
import os


_API_URL = "https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/neoforge"
_VERSION_REG_EX = re.compile(r"^\d+\.\d+")


class Neoforge(ModLoaderBase):
    "Implements the mod loader class for NeoForge"
    def get_id(self) -> str:
        "Implements get_id() for NeoForge"
        return "neoforge"

    def get_name(self) -> str:
        "Implements get_name() for NeoForge"
        return "NeoForge"

    def _normalize_minecraft_version(self, minecraft_version: str) -> str:
        "Turns the version string into a normal minecraft version"
        minecraft_version = minecraft_version.removesuffix(".0")
        return f"1.{minecraft_version}"

    def get_minecraft_versions(self, stable_only: bool) -> list[str]:
        "Implements get_minecraft_versions() for NeoForge"
        version_dict: dict[str, bool] = {}

        for current_version in get_requests_response_cache(_API_URL).json()["versions"]:
            if not current_version.startswith("0."):
                current_minecraft_version = _VERSION_REG_EX.match(current_version).group()  # type: ignore
                version_dict[self._normalize_minecraft_version(current_minecraft_version)] = True

        return list(version_dict.keys())

    def get_loader_versions(self, minecraft_version: str, stable_only: bool) -> list[str]:
        "Implements get_loader_versions() for NeoForge"
        version_list: list[str] = []

        for current_version in get_requests_response_cache(_API_URL).json()["versions"]:
            if "beta" in current_version and stable_only:
                continue

            current_minecraft_version = _VERSION_REG_EX.match(current_version).group()  # type: ignore
            if self._normalize_minecraft_version(current_minecraft_version) == minecraft_version:
                version_list.append(current_version)

        # The versions are sorted from oldest to newest but we want newest to oldest
        version_list.reverse()

        return version_list

    def get_installer_url(self, minecraft_version: str, loader_version: str) -> str:
        "Implements get_installer_url() for NeoForge"
        return f"https://maven.neoforged.net/releases/net/neoforged/neoforge/{loader_version}/neoforge-{loader_version}-installer.jar"

    def get_installed_version(self, minecraft_version: str, loader_version: str) -> str:
        "Implements get_installed_versions() for NeoForge"
        return f"neoforge-{loader_version}"

    def install(self, minecraft_version: str, minecraft_directory: str, callback: CallbackDict, java: str, loader_version: str) -> None:
        "Implements install() for NeoForge"
        if not do_vanilla_launcher_profiles_exists(minecraft_directory):
            create_empty_vanilla_launcher_profiles_file(minecraft_directory)

        with tempfile.TemporaryDirectory(prefix="minecraft-launcher-lib-") as tempdir:
            installer_path = os.path.join(tempdir, "neoforge-installer.jar")

            download_file(self.get_installer_url(minecraft_version, loader_version), installer_path)

            callback.get("setStatus", empty)("Running installer")
            subprocess.run(
                [java, "-jar", installer_path, "--install-client", minecraft_directory],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=tempdir,
                check=True,
                startupinfo=SUBPROCESS_STARTUP_INFO
            )
