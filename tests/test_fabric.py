from ._test_helper import prepare_test_versions, get_test_callbacks, prepare_requests_mock
import minecraft_launcher_lib
import pytest_subtests
import requests_mock
import subprocess
import platform
import pathlib
import pytest
import shutil


def test_fabric_get_all_minecraft_versions() -> None:
    version_list = minecraft_launcher_lib.fabric.get_all_minecraft_versions()
    assert isinstance(version_list[0]["version"], str)
    assert isinstance(version_list[0]["stable"], bool)


def test_fabric_get_stable_minecraft_versions() -> None:
    version_list = minecraft_launcher_lib.fabric.get_stable_minecraft_versions()
    assert isinstance(version_list[0], str)


def test_fabric_get_latest_minecraft_version() -> None:
    assert isinstance(minecraft_launcher_lib.fabric.get_latest_minecraft_version(), str)


def test_fabric_get_latest_stable_minecraft_version() -> None:
    assert isinstance(minecraft_launcher_lib.fabric.get_latest_stable_minecraft_version(), str)


def test_fabric_is_minecraft_version_supported() -> None:
    assert minecraft_launcher_lib.fabric.is_minecraft_version_supported("1.16") is True
    assert minecraft_launcher_lib.fabric.is_minecraft_version_supported("1.0") is False


def test_fabric_get_all_loader_versions() -> None:
    version_list = minecraft_launcher_lib.fabric.get_all_loader_versions()
    assert isinstance(version_list[0]["separator"], str)
    assert isinstance(version_list[0]["build"], int)
    assert isinstance(version_list[0]["maven"], str)
    assert isinstance(version_list[0]["version"], str)
    assert isinstance(version_list[0]["stable"], bool)


def test_fabric_get_latest_loader_version() -> None:
    assert isinstance(minecraft_launcher_lib.fabric.get_latest_loader_version(), str)


def test_fabric_get_latest_installer_version() -> None:
    assert isinstance(minecraft_launcher_lib.fabric.get_latest_installer_version(), str)


def test_install_fabric(monkeypatch: pytest.MonkeyPatch, subtests: pytest_subtests.SubTests, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(minecraft_launcher_lib.fabric, "is_minecraft_version_supported", lambda version: True if version == "test1" else False)
    monkeypatch.setattr(minecraft_launcher_lib.fabric, "get_latest_installer_version", lambda: "testinstaller")
    monkeypatch.setattr(minecraft_launcher_lib.fabric, "get_latest_loader_version", lambda: "testloader")
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kwargs: subprocess.CompletedProcess([], 0))
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    requests_mock.get("https://maven.fabricmc.net/net/fabricmc/fabric-installer/testinstaller/fabric-installer-testinstaller.jar")
    requests_mock.real_http = True

    prepare_test_versions(tmp_path)
    prepare_requests_mock(requests_mock)

    shutil.copytree(tmp_path / "versions" / "test1", tmp_path / "versions" / "fabric-loader-testloader-test1")
    (tmp_path / "versions" / "fabric-loader-testloader-test1" / "test1.json").rename(tmp_path / "versions" / "fabric-loader-testloader-test1" / "fabric-loader-testloader-test1.json")

    with subtests.test("Install"):
        minecraft_launcher_lib.fabric.install_fabric("test1", tmp_path, callback=get_test_callbacks())

    with subtests.test("ExternalProgramError"):
        monkeypatch.setattr(subprocess, "run", lambda cmd, **kwargs: subprocess.CompletedProcess([], 1))

        with pytest.raises(minecraft_launcher_lib.exceptions.ExternalProgramError):
            minecraft_launcher_lib.fabric.install_fabric("test1", tmp_path)

    with subtests.test("UnsupportedVersion"):
        with pytest.raises(minecraft_launcher_lib.exceptions.UnsupportedVersion):
            minecraft_launcher_lib.fabric.install_fabric("natives", tmp_path)

    with subtests.test("VersionNotFound"):
        with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
            minecraft_launcher_lib.fabric.install_fabric("invalid", tmp_path)
