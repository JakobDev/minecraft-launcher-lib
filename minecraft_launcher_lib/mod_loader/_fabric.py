# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from .._helper import download_file, empty, SUBPROCESS_STARTUP_INFO
from ._fabric_quilt_base import FabricQuiltBase
from ..types import CallbackDict
import subprocess
import tempfile
import os


class Fabric(FabricQuiltBase):
    "Implements the mod loader class for Fabric"
    def __init__(self) -> None:
        super().__init__()

        self._maven_url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer"
        self._game_url = "https://meta.fabricmc.net/v2/versions/game"
        self._loader_url = "https://meta.fabricmc.net/v2/versions/loader"
        self._loader_name = "fabric"

    def get_id(self) -> str:
        "Implements get_id() for Fabric"
        return "fabric"

    def get_name(self) -> str:
        "Implements get_name() for Fabric"
        return "Fabric"

    def install(self, minecraft_version: str, minecraft_directory: str, callback: CallbackDict, java: str, loader_version: str) -> None:
        "Implements install() for Fabric"
        installer_download_url = self.get_installer_url(minecraft_version, loader_version)

        with tempfile.TemporaryDirectory(prefix="minecraft-launcher-lib-") as tempdir:
            installer_path = os.path.join(tempdir, "fabric-installer.jar")

            # Download the installer
            download_file(installer_download_url, installer_path, callback=callback, overwrite=True)

            # Run the installer see https://fabricmc.net/wiki/install#cli_installation
            callback.get("setStatus", empty)("Running installer")
            command = [java, "-jar", installer_path, "client", "-dir", minecraft_directory, "-mcversion", minecraft_version, "-loader", loader_version, "-noprofile", "-snapshot"]
            subprocess.run(command, cwd=tempdir, check=True, startupinfo=SUBPROCESS_STARTUP_INFO)
