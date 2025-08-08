# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from ._test_helper import prepare_test_versions, prepare_requests_mock, get_test_callbacks, create_bytes_zip
import minecraft_launcher_lib
import requests_mock
import subprocess
import platform
import pathlib
import pytest


def test_mod_loader_forge_get_id() -> None:
    forge = minecraft_launcher_lib.mod_loader.get_mod_loader("forge")
    assert forge.get_id() == "forge"


def test_mod_loader_forge_get_name() -> None:
    forge = minecraft_launcher_lib.mod_loader.get_mod_loader("forge")
    assert forge.get_name() == "Forge"


def test_mod_loader_forge_get_minecraft_versions(requests_mock: requests_mock.Mocker) -> None:
    prepare_requests_mock(requests_mock)

    forge = minecraft_launcher_lib.mod_loader.get_mod_loader("forge")
    version_list = forge.get_minecraft_versions(True)

    assert len(version_list) == 1
    assert version_list[0] == "test1"


def test_mod_loader_forge_get_loader_versions(requests_mock: requests_mock.Mocker) -> None:
    prepare_requests_mock(requests_mock)

    forge = minecraft_launcher_lib.mod_loader.get_mod_loader("forge")
    version_list = forge.get_loader_versions("test1", True)

    assert len(version_list) == 1
    assert version_list[0] == "1.0"


def test_mod_loader_forge_get_installer_url() -> None:
    forge = minecraft_launcher_lib.mod_loader.get_mod_loader("forge")
    installer_url = forge._base.get_installer_url("test1", "1.0")
    assert installer_url == "https://maven.minecraftforge.net/net/minecraftforge/forge/test1-1.0/forge-test1-1.0-installer.jar"


def test_mod_loader_forge_get_installed_version() -> None:
    forge = minecraft_launcher_lib.mod_loader.get_mod_loader("forge")
    forge.get_installed_version("minecraft-version", "loader-version") == "minecraft-version-forge-loader-version"


def test_mod_loader_forge_install(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    forge = minecraft_launcher_lib.mod_loader.get_mod_loader("forge")

    requests_mock.get("minecraft-launcher-lib://forge/forgetest1.jar", content=create_bytes_zip(pathlib.Path(__file__).parent / "data" / "forge" / "forgetest1"))
    requests_mock.get("minecraft-launcher-lib://forge/forgetest2.jar", content=create_bytes_zip(pathlib.Path(__file__).parent / "data" / "forge" / "forgetest2"))

    monkeypatch.setattr(forge._base, "get_installer_url", lambda minecraft_version, loader_version: f"minecraft-launcher-lib://forge/{loader_version}.jar")
    monkeypatch.setattr(forge, "is_minecraft_version_supported", lambda minecraft_version: True)
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "architecture", lambda: ("64bit", "ELF"))
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kwargs: None)

    prepare_test_versions(tmp_path)
    prepare_requests_mock(requests_mock)

    forge.install("test1", tmp_path, callback=get_test_callbacks(), loader_version="forgetest1")
    forge.install("test1", tmp_path, callback=get_test_callbacks(), loader_version="forgetest2")
