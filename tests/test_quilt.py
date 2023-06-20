from ._test_helper import prepare_test_versions, get_test_callbacks
import minecraft_launcher_lib
import requests_mock
import subprocess
import platform
import pathlib
import pytest
import shutil


def test_quilt_get_all_minecraft_versions() -> None:
    version_list = minecraft_launcher_lib.quilt.get_all_minecraft_versions()
    for i in version_list:
        assert isinstance(i["version"], str)
        assert isinstance(i["stable"], bool)


def test_quilt_get_stable_minecraft_versions() -> None:
    version_list = minecraft_launcher_lib.quilt.get_stable_minecraft_versions()
    assert isinstance(version_list[0], str)


def test_quilt_get_latest_minecraft_version() -> None:
    assert isinstance(minecraft_launcher_lib.quilt.get_latest_minecraft_version(), str)


def test_quilt_get_latest_stable_minecraft_version() -> None:
    assert isinstance(minecraft_launcher_lib.quilt.get_latest_stable_minecraft_version(), str)


def test_quilt_is_minecraft_version_supported() -> None:
    assert minecraft_launcher_lib.quilt.is_minecraft_version_supported("1.16") is True
    assert minecraft_launcher_lib.quilt.is_minecraft_version_supported("1.0") is False


def test_quilt_get_all_loader_versions() -> None:
    version_list = minecraft_launcher_lib.quilt.get_all_loader_versions()
    for i in version_list:
        assert isinstance(i["separator"], str)
        assert isinstance(i["build"], int)
        assert isinstance(i["maven"], str)
        assert isinstance(i["version"], str)


def test_quilt_get_latest_loader_version() -> None:
    assert isinstance(minecraft_launcher_lib.quilt.get_latest_loader_version(), str)


def test_quilt_get_latest_installer_version() -> None:
    assert isinstance(minecraft_launcher_lib.quilt.get_latest_installer_version(), str)


def test_install_quilt(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(minecraft_launcher_lib.quilt, "is_minecraft_version_supported", lambda version: True if version == "test1" else False)
    monkeypatch.setattr(minecraft_launcher_lib.quilt, "get_latest_installer_version", lambda: "testinstaller")
    monkeypatch.setattr(minecraft_launcher_lib.quilt, "get_latest_loader_version", lambda: "testloader")
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kwargs: subprocess.CompletedProcess([], 0))
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    requests_mock.get("https://maven.quiltmc.org/repository/release/org/quiltmc/quilt-installer/testinstaller/quilt-installer-testinstaller.jar")
    requests_mock.real_http = True

    prepare_test_versions(tmp_path)

    shutil.copytree(tmp_path / "versions" / "test1", tmp_path / "versions" / "quilt-loader-testloader-test1")
    (tmp_path / "versions" / "quilt-loader-testloader-test1" / "test1.json").rename(tmp_path / "versions" / "quilt-loader-testloader-test1" / "quilt-loader-testloader-test1.json")

    minecraft_launcher_lib.quilt.install_quilt("test1", tmp_path, callback=get_test_callbacks())

    monkeypatch.setattr(subprocess, "run", lambda cmd, **kwargs: subprocess.CompletedProcess([], 1))

    with pytest.raises(minecraft_launcher_lib.exceptions.ExternalProgramError):
        minecraft_launcher_lib.quilt.install_quilt("test1", tmp_path)

    with pytest.raises(minecraft_launcher_lib.exceptions.UnsupportedVersion):
        minecraft_launcher_lib.quilt.install_quilt("natives", tmp_path)

    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.quilt.install_quilt("invalid", tmp_path)
