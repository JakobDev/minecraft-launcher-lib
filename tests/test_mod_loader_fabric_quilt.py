# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from ._test_helper import prepare_test_versions, prepare_requests_mock, get_test_callbacks
import minecraft_launcher_lib
import pytest_subprocess
import pytest_subtests
import requests_mock
import platform
import pathlib
import pytest
import shutil


def test_mod_loader_fabric_get_id() -> None:
    fabric = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
    assert fabric.get_id() == "fabric"


def test_mod_loader_quilt_get_id() -> None:
    quilt = minecraft_launcher_lib.mod_loader.get_mod_loader("quilt")
    assert quilt.get_id() == "quilt"


def test_mod_loader_fabric_get_name() -> None:
    fabric = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
    assert fabric.get_name() == "Fabric"


def test_mod_loader_quilt_get_name() -> None:
    quilt = minecraft_launcher_lib.mod_loader.get_mod_loader("quilt")
    assert quilt.get_name() == "Quilt"


@pytest.mark.parametrize("loader_id", ["fabric", "quilt"])
def test_mod_loader_fabric_quilt_get_minecraft_versions(loader_id: str, requests_mock: requests_mock.Mocker) -> None:
    prepare_requests_mock(requests_mock)

    loader = minecraft_launcher_lib.mod_loader.get_mod_loader(loader_id)

    stable_versions = loader.get_minecraft_versions(True)
    assert len(stable_versions) == 1
    assert stable_versions[0] == "test2"

    unstable_versions = loader.get_minecraft_versions(False)
    assert len(unstable_versions) == 2
    assert unstable_versions[0] == "unstable"
    assert unstable_versions[1] == "test2"


def test_mod_loader_fabric_get_loader_versions(requests_mock: requests_mock.Mocker) -> None:
    prepare_requests_mock(requests_mock)

    fabric = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
    stable_versions = fabric.get_loader_versions("1.0", True)
    assert len(stable_versions) == 1
    assert stable_versions[0] == "0.2"

    unstable_versions = fabric.get_loader_versions("1.0", False)
    assert len(unstable_versions) == 2
    assert unstable_versions[0] == "0.1"
    assert unstable_versions[1] == "0.2"


def test_mod_loader_quilt_get_loader_versions(requests_mock: requests_mock.Mocker) -> None:
    prepare_requests_mock(requests_mock)

    quilt = minecraft_launcher_lib.mod_loader.get_mod_loader("quilt")
    stable_versions = quilt.get_loader_versions("1.0", True)
    assert len(stable_versions) == 1
    assert stable_versions[0] == "0.2"

    unstable_versions = quilt.get_loader_versions("1.0", False)
    assert len(unstable_versions) == 2
    assert unstable_versions[0] == "0.1-beta"
    assert unstable_versions[1] == "0.2"


def test_mod_loader_fabric_quilt_get_installer_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("minecraft_launcher_lib.mod_loader._fabric_quilt_base.parse_maven_metadata", lambda url: {"latest": "latest-version"})

    fabric = minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")
    fabric_installer = fabric._base.get_installer_url("minecraft-version", "loader-version")
    assert fabric_installer == "https://maven.fabricmc.net/net/fabricmc/fabric-installer/latest-version/fabric-installer-latest-version.jar"

    quilt = minecraft_launcher_lib.mod_loader.get_mod_loader("quilt")
    quilt_installer = quilt._base.get_installer_url("minecraft-version", "loader-version")
    assert quilt_installer == "https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer/latest-version/quilt-installer-latest-version.jar"


@pytest.mark.parametrize("loader_id", ["fabric", "quilt"])
def test_mod_loader_fabric_quilt_get_installed_version(loader_id: str) -> None:
    loader = minecraft_launcher_lib.mod_loader.get_mod_loader(loader_id)
    assert loader.get_installed_version("minecraft-version", "loader-version") == f"{loader_id}-loader-loader-version-minecraft-version"


@pytest.mark.parametrize("loader_id", ["fabric", "quilt"])
def test_mod_loader_fabric_quilt_install(loader_id: str, monkeypatch: pytest.MonkeyPatch, subtests: pytest_subtests.SubTests, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path, fp: pytest_subprocess.fake_process.FakeProcess) -> None:
    fabric = minecraft_launcher_lib.mod_loader.get_mod_loader(loader_id)

    requests_mock.get("minecraft-launcher-lib://testinstaller")

    monkeypatch.setattr(fabric, "is_minecraft_version_supported", lambda version: True if version == "test1" else False)
    monkeypatch.setattr(fabric._base, "get_installer_url", lambda minecraft_version, loader_version: "minecraft-launcher-lib://testinstaller")
    monkeypatch.setattr(fabric, "get_latest_loader_version", lambda stable_only: "testloader")
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    fp.allow_unregistered(True)

    prepare_test_versions(tmp_path)
    prepare_requests_mock(requests_mock)

    shutil.copytree(tmp_path / "versions" / "test1", tmp_path / "versions" / f"{loader_id}-loader-testloader-test1")
    (tmp_path / "versions" / f"{loader_id}-loader-testloader-test1" / "test1.json").rename(
        tmp_path / "versions" / f"{loader_id}-loader-testloader-test1" / f"{loader_id}-loader-testloader-test1.json")

    with subtests.test("Install"):
        fp.register(["java", fp.any()])
        fabric.install("test1", tmp_path, callback=get_test_callbacks())
        assert fp.call_count(["java", fp.any()]) == 1

    with subtests.test("VersionNotFound"):
        with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
            fabric.install("invalid", tmp_path)

    with subtests.test("UnsupportedVersion"):
        with pytest.raises(minecraft_launcher_lib.exceptions.UnsupportedVersion):
            fabric.install("natives", tmp_path)
