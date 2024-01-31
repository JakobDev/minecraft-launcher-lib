from ._test_helper import prepare_test_versions, get_test_callbacks, prepare_requests_mock, create_bytes_zip
import minecraft_launcher_lib
import requests_mock
import subprocess
import platform
import pathlib
import pytest


def test_install_forge_version(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    requests_mock.get("https://maven.minecraftforge.net/net/minecraftforge/forge/forgetest1/forge-forgetest1-installer.jar", content=create_bytes_zip(pathlib.Path(__file__).parent / "data" / "forge" / "forgetest1"))
    requests_mock.get("https://maven.minecraftforge.net/net/minecraftforge/forge/forgetest2/forge-forgetest2-installer.jar", content=create_bytes_zip(pathlib.Path(__file__).parent / "data" / "forge" / "forgetest2"))

    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(platform, "architecture", lambda: ("64bit", "ELF"))
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kwargs: None)

    prepare_test_versions(tmp_path)
    prepare_requests_mock(requests_mock)

    minecraft_launcher_lib.forge.install_forge_version("forgetest1", tmp_path, callback=get_test_callbacks())
    minecraft_launcher_lib.forge.install_forge_version("forgetest2", tmp_path, callback=get_test_callbacks())

    assert (tmp_path / "libraries" / "net" / "minecraftforge" / "forge" / "forgetest1" / "forge-forgetest1.jar").is_file()


def test_install_forge_version_invalid_version(requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    requests_mock.get("https://maven.minecraftforge.net/net/minecraftforge/forge/invalid/forge-invalid-installer.jar", status_code=404)

    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound) as ex:
        minecraft_launcher_lib.forge.install_forge_version("invalid", str(tmp_path))

    assert ex.value.version == "invalid"


def test_run_forge_installer(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get("https://maven.minecraftforge.net/net/minecraftforge/forge/test/forge-test-installer.jar", text="Hello")
    requests_mock.get("https://maven.minecraftforge.net/net/minecraftforge/forge/invalid/forge-invalid-installer.jar", text="World", status_code=404)
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kwargs: exec("raise subprocess.CalledProcessError(1, [])") if cmd[0] != "java" else None)

    minecraft_launcher_lib.forge.run_forge_installer("test")

    with pytest.raises(subprocess.CalledProcessError):
        minecraft_launcher_lib.forge.run_forge_installer("test", java="test")

    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.forge.run_forge_installer("invalid")


def test_list_forge_versions() -> None:
    version_list = minecraft_launcher_lib.forge.list_forge_versions()
    assert isinstance(version_list[0], str)


def test_find_forge_version() -> None:
    assert isinstance(minecraft_launcher_lib.forge.find_forge_version("1.16.2"), str)
    assert minecraft_launcher_lib.forge.find_forge_version("Test123") is None


def test_is_forge_version_valid() -> None:
    assert minecraft_launcher_lib.forge.is_forge_version_valid("1.16.5-36.1.32") is True
    assert minecraft_launcher_lib.forge.is_forge_version_valid("Test123") is False


def test_supports_automatic_install() -> None:
    assert minecraft_launcher_lib.forge.supports_automatic_install("1.16.5-36.1.32") is True
    assert minecraft_launcher_lib.forge.supports_automatic_install("1.12-14.21.1.2443") is False
    assert minecraft_launcher_lib.forge.supports_automatic_install("invalid") is False


def test_forge_to_installed_version() -> None:
    assert minecraft_launcher_lib.forge.forge_to_installed_version("1.19-41.0.105") == "1.19-forge-41.0.105"

    with pytest.raises(ValueError):
        minecraft_launcher_lib.forge.forge_to_installed_version("Test123")
