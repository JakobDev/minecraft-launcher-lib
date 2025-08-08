# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from ._test_helper import prepare_test_versions, prepare_requests_mock
import minecraft_launcher_lib
import pytest_subprocess
import requests_mock
import pathlib
import pytest


def test_mod_loader_neoforge_get_id() -> None:
    neoforge = minecraft_launcher_lib.mod_loader.get_mod_loader("neoforge")
    assert neoforge.get_id() == "neoforge"


def test_mod_loader_neoforge_get_name() -> None:
    neoforge = minecraft_launcher_lib.mod_loader.get_mod_loader("neoforge")
    assert neoforge.get_name() == "NeoForge"


def test_mod_loader_neoforge_get_minecraft_version(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get("https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/neoforge", json={
        "versions": ["20.0.neoforge-beta", "20.0.neoforge"]
    })

    neoforge = minecraft_launcher_lib.mod_loader.get_mod_loader("neoforge")
    version_list = neoforge.get_minecraft_versions(True)

    assert len(version_list) == 1
    assert version_list[0] == "1.20"


def test_mod_loader_neoforge_get_loader_versions(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get("https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/neoforge", json={
        "versions": ["20.0.neoforge-beta", "20.0.neoforge"]
    })

    neoforge = minecraft_launcher_lib.mod_loader.get_mod_loader("neoforge")

    stable_versions = neoforge.get_loader_versions("1.20", True)
    assert len(stable_versions) == 1
    assert stable_versions[0] == "20.0.neoforge"

    all_versions = neoforge.get_loader_versions("1.20", False)
    assert len(all_versions) == 2
    assert all_versions[0] == "20.0.neoforge-beta"
    assert all_versions[1] == "20.0.neoforge"


def test_mod_loader_neoforge_get_installer_url() -> None:
    neoforge = minecraft_launcher_lib.mod_loader.get_mod_loader("neoforge")
    installer_url = neoforge._base.get_installer_url("minecraft-version", "loader-version")
    assert installer_url == "https://maven.neoforged.net/releases/net/neoforged/neoforge/loader-version/neoforge-loader-version-installer.jar"


def test_mod_loader_neoforge_get_installed_version() -> None:
    neoforge = minecraft_launcher_lib.mod_loader.get_mod_loader("neoforge")
    neoforge.get_installed_version("minecraft-version", "loader-version") == "neoforge-loader-version"


def test_mod_loader_neoforge_install(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path, fp: pytest_subprocess.fake_process.FakeProcess) -> None:
    neoforge = minecraft_launcher_lib.mod_loader.get_mod_loader("neoforge")

    requests_mock.get("minecraft-launcher-lib://neoforge.jar")

    monkeypatch.setattr(neoforge._base, "get_installer_url", lambda minecraft_version, loader_version: "minecraft-launcher-lib://neoforge.jar")
    monkeypatch.setattr(neoforge, "get_installed_version", lambda minecraft_version, loader_version: "test1")
    monkeypatch.setattr(neoforge, "is_minecraft_version_supported", lambda minecraft_version: True)
    monkeypatch.setattr(neoforge, "get_latest_loader_version", lambda minecraft_version: "1.0")

    fp.register(["java", fp.any()])
    fp.allow_unregistered(True)

    prepare_test_versions(tmp_path)
    prepare_requests_mock(requests_mock)

    neoforge.install("test1", tmp_path)

    assert fp.call_count(["java", fp.any()]) == 1
