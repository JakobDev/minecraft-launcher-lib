# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from .._helper import download_file, extract_file_from_zip, get_classpath_separator, get_library_path, get_jar_mainclass, parse_maven_metadata, empty, SUBPROCESS_STARTUP_INFO
from ..install import install_minecraft_version, install_libraries
from .._internal_types.forge_types import ForgeInstallProfile
from .._internal_types.shared_types import ClientJson
from ._base import ModLoaderBase
from ..types import CallbackDict
from typing import cast
import subprocess
import tempfile
import zipfile
import shutil
import json
import os

_MAVEN_METADATA_URL = "https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml"


class Forge(ModLoaderBase):
    "Implements the mod loader class for Forge"
    def get_id(self) -> str:
        "Implements get_id() for Forge"
        return "forge"

    def get_name(self) -> str:
        "Implements get_name() for Forge"
        return "Forge"

    def get_minecraft_versions(self, stable_only: bool) -> list[str]:
        "Implements get_minecraft_versions() for Forge"
        version_dict: dict[str, bool] = {}

        for current_version in parse_maven_metadata(_MAVEN_METADATA_URL)["versions"]:
            current_minecraft_version, _ = current_version.split("-", 1)
            version_dict[current_minecraft_version] = True

        return list(version_dict.keys())

    def get_loader_versions(self, minecraft_version: str, stable_only: bool) -> list[str]:
        "Implements get_loader_versions() for Forge"
        version_list: list[str] = []

        for current_version in parse_maven_metadata(_MAVEN_METADATA_URL)["versions"]:
            current_minecraft_version, current_forge_version = current_version.split("-", 1)
            if current_minecraft_version == minecraft_version:
                version_list.append(current_forge_version)

        return version_list

    def get_installer_url(self, minecraft_version: str, loader_version: str) -> str:
        "Implements get_installer_url() for Forge"
        forge_version = f"{minecraft_version}-{loader_version}"
        return f"https://maven.minecraftforge.net/net/minecraftforge/forge/{forge_version}/forge-{forge_version}-installer.jar"

    def get_installed_version(self, minecraft_version: str, loader_version: str) -> str:
        "Implements get_installed_version() for Forge"
        return f"{minecraft_version}-forge-{loader_version}"

    def _forge_processors(self, data: ForgeInstallProfile, minecraft_directory: str, tempdir: str, lzma_path: str, installer_path: str, callback: CallbackDict, java: str) -> None:
        """
        Run the processors of the install_profile.json
        """
        argument_vars = {"{MINECRAFT_JAR}": os.path.join(minecraft_directory, "versions", data["minecraft"], data["minecraft"] + ".jar")}
        for data_key, data_value in data["data"].items():
            if data_value["client"].startswith("[") and data_value["client"].endswith("]"):
                argument_vars["{" + data_key + "}"] = get_library_path(data_value["client"][1:-1], minecraft_directory)
            else:
                argument_vars["{" + data_key + "}"] = data_value["client"]

        root_path = os.path.join(tempdir, "root")
        os.makedirs(root_path)

        argument_vars["{INSTALLER}"] = installer_path
        argument_vars["{BINPATCH}"] = lzma_path
        argument_vars["{ROOT}"] = root_path
        argument_vars["{SIDE}"] = "client"

        classpath_seperator = get_classpath_separator()

        callback.get("setMax", empty)(len(data["processors"]))

        for count, current_processor in enumerate(data["processors"]):
            if "client" not in current_processor.get("sides", ["client"]):
                # Skip server side only processors
                continue

            callback.get("setStatus", empty)("Running processor " + current_processor["jar"])

            # Get the classpath
            classpath = ""
            for current_classpath in current_processor["classpath"]:
                classpath = classpath + get_library_path(current_classpath, minecraft_directory) + classpath_seperator

            classpath = classpath + get_library_path(current_processor["jar"], minecraft_directory)
            mainclass = get_jar_mainclass(get_library_path(current_processor["jar"], minecraft_directory))

            command = [java, "-cp", classpath, mainclass]
            for arg in current_processor["args"]:
                var = argument_vars.get(arg, arg)
                if var.startswith("[") and var.endswith("]"):
                    command.append(get_library_path(var[1:-1], minecraft_directory))
                else:
                    command.append(var)

            for argument_key, argument_value in argument_vars.items():
                for pos in range(len(command)):
                    command[pos] = command[pos].replace(argument_key, argument_value)

            subprocess.run(command, cwd=root_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=SUBPROCESS_STARTUP_INFO)

            callback.get("setProgress", empty)(count)

    def install(self, minecraft_version: str, minecraft_directory: str, callback: CallbackDict, java: str, loader_version: str) -> None:
        "Implements install() for Forge"
        forge_installer_url = self.get_installer_url(minecraft_version, loader_version)
        forge_version = f"{minecraft_version}-{loader_version}"

        forge_version_id = self.get_installed_version(minecraft_version, loader_version)

        with tempfile.TemporaryDirectory(prefix="minecraft-launcher-lib-") as tempdir:
            installer_path = os.path.join(tempdir, "installer.jar")

            download_file(forge_installer_url, installer_path, callback)

            with zipfile.ZipFile(installer_path, "r") as zf:
                # Read the install_profile.json
                with zf.open("install_profile.json", "r") as f:
                    version_content = f.read()

                version_data: ForgeInstallProfile = json.loads(version_content)
                minecraft_version = version_data["minecraft"] if "minecraft" in version_data else version_data["install"]["minecraft"]

                # Install all needed libs from install_profile.json
                if "libraries" in version_data:
                    install_libraries(minecraft_version, version_data["libraries"], str(minecraft_directory), callback)

                # Install client json
                client_json: ClientJson | None = None

                if "version.json" in zf.namelist():
                    with zf.open("version.json", "r") as f:
                        client_json = json.loads(f.read())
                elif "versionInfo" in version_data:
                    client_json = version_data["versionInfo"]

                # It should be set now
                # If not, it should just throw a error later in the code
                client_json = cast(ClientJson, client_json)

                client_json["id"] = forge_version_id

                version_dir = os.path.join(minecraft_directory, "versions", forge_version_id)

                try:
                    os.makedirs(version_dir)
                except FileExistsError:
                    pass

                with open(os.path.join(version_dir, f"{forge_version_id}.json"), "w", encoding="utf-8") as f:
                    json.dump(client_json, f, ensure_ascii=False, indent=4)

                # Extract forge libs from the installer
                forge_lib_path = os.path.join(minecraft_directory, "libraries", "net", "minecraftforge", "forge", forge_version)
                try:
                    extract_file_from_zip(
                        zf,
                        f"maven/net/minecraftforge/forge/{forge_version}/forge-{forge_version}-universal.jar",
                        os.path.join(forge_lib_path, f"forge-{forge_version}-universal.jar"),
                        minecraft_directory=minecraft_directory
                    )
                except KeyError:
                    pass

                try:
                    extract_file_from_zip(
                        zf,
                        f"forge-{forge_version}-universal.jar",
                        os.path.join(forge_lib_path, f"forge-{forge_version}.jar"),
                        minecraft_directory=minecraft_directory
                    )
                except KeyError:
                    pass

                try:
                    extract_file_from_zip(
                        zf,
                        f"maven/net/minecraftforge/forge/{forge_version}/forge-{forge_version}.jar",
                        os.path.join(forge_lib_path, f"forge-{forge_version}.jar"),
                        minecraft_directory=minecraft_directory
                    )
                except KeyError:
                    pass

                # Extract the client.lzma
                lzma_path = os.path.join(tempdir, "client.lzma")
                try:
                    extract_file_from_zip(zf, "data/client.lzma", lzma_path)
                except KeyError:
                    pass

            # Install the rest with the vanilla function
            install_minecraft_version(forge_version_id, minecraft_directory, callback=callback)

            # Run the processors
            if "processors" in version_data:
                self._forge_processors(version_data, minecraft_directory, tempdir, lzma_path, installer_path, callback, java)

        # If Forge provides no client.jar, we can just copy the client.jar from the base minecraft version
        forge_jar_path = os.path.join(minecraft_directory, "versions", forge_version_id, f"{forge_version_id}.jar")
        if not os.path.isfile(forge_jar_path):
            shutil.copyfile(os.path.join(
                minecraft_directory, "versions", minecraft_version,
                f"{minecraft_version}.jar"), forge_jar_path
            )
