import minecraft_launcher_lib
import pathlib
import pytest


def test_install_minecraft_version_invalid_version(tmp_path: pathlib.Path):
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.forge.install_forge_version("InvalidVersion", str(tmp_path))


def test_list_forge_versions():
    version_list = minecraft_launcher_lib.forge.list_forge_versions()
    assert isinstance(version_list[0], str)


def test_find_forge_version():
    assert isinstance(minecraft_launcher_lib.forge.find_forge_version("1.16.2"), str)
    assert minecraft_launcher_lib.forge.find_forge_version("Test123") is None


def test_is_forge_version_valid():
    assert minecraft_launcher_lib.forge.is_forge_version_valid("1.16.5-36.1.32") is True
    assert minecraft_launcher_lib.forge.is_forge_version_valid("Test123") is False


def test_supports_automatic_install():
    assert minecraft_launcher_lib.forge.supports_automatic_install("1.16.5-36.1.32") is True
    assert minecraft_launcher_lib.forge.supports_automatic_install("1.12-14.21.1.2443") is False


def test_forge_to_installed_version():
    assert minecraft_launcher_lib.forge.forge_to_installed_version("1.19-41.0.105") == "1.19-forge-41.0.105"


def test__forge_to_installed_version_invalid_version():
    with pytest.raises(ValueError):
        minecraft_launcher_lib.forge.forge_to_installed_version("Test123")
