# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from .._helper import download_file, empty, SUBPROCESS_STARTUP_INFO
from ._fabric_quilt_base import FabricQuiltBase
from ..types import CallbackDict
import subprocess
import tempfile
import os


class Quilt(FabricQuiltBase):
    "Implements the mod loader class for Quilt"
    def __init__(self) -> None:
        super().__init__()

        self._maven_url = "https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer"
        self._game_url = "https://meta.quiltmc.org/v3/versions/game"
        self._loader_url = "https://meta.quiltmc.org/v3/versions/loader"
        self._loader_name = "quilt"

    def get_id(self) -> str:
        "Implements get_id() for Quilt"
        return "quilt"

    def get_name(self) -> str:
        "Implements get_name() for Quilt"
        return "Quilt"

    def install(self, minecraft_version: str, minecraft_directory: str, callback: CallbackDict, java: str, loader_version: str) -> None:
        "Implements install() for Quilt"
        installer_download_url = self.get_installer_url(minecraft_version, loader_version)

        with tempfile.TemporaryDirectory(prefix="minecraft-launcher-lib-") as tempdir:
            installer_path = os.path.join(tempdir, "quilt-installer.jar")

            # Download the installer
            download_file(installer_download_url, installer_path, callback=callback, overwrite=True)

            # Run the installer see
            callback.get("setStatus", empty)("Running installer")
            command = [java, "-jar", installer_path, "install", "client", minecraft_version, loader_version, f"--install-dir={minecraft_directory}", "--no-profile"]
            subprocess.run(command, cwd=tempdir, check=True, startupinfo=SUBPROCESS_STARTUP_INFO)
