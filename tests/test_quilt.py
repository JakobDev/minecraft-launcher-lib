import minecraft_launcher_lib
import pathlib
import pytest


def test_get_all_minecraft_versions():
    version_list = minecraft_launcher_lib.quilt.get_all_minecraft_versions()
    for i in version_list:
        assert isinstance(i["version"], str)
        assert isinstance(i["stable"], bool)


def test_get_stable_minecraft_versions():
    version_list = minecraft_launcher_lib.quilt.get_stable_minecraft_versions()
    assert isinstance(version_list[0], str)


def test_get_latest_minecraft_version():
    assert isinstance(minecraft_launcher_lib.quilt.get_latest_minecraft_version(), str)


def test_get_latest_stable_minecraft_version():
    assert isinstance(minecraft_launcher_lib.quilt.get_latest_stable_minecraft_version(), str)


def test_is_minecraft_version_supported():
    assert minecraft_launcher_lib.quilt.is_minecraft_version_supported("1.16") is True
    assert minecraft_launcher_lib.quilt.is_minecraft_version_supported("1.0") is False


def test_get_all_loader_versions():
    version_list = minecraft_launcher_lib.quilt.get_all_loader_versions()
    for i in version_list:
        assert isinstance(i["separator"], str)
        assert isinstance(i["build"], int)
        assert isinstance(i["maven"], str)
        assert isinstance(i["version"], str)


def test_get_latest_loader_version():
    assert isinstance(minecraft_launcher_lib.quilt.get_latest_loader_version(), str)


def test_get_latest_installer_version():
    assert isinstance(minecraft_launcher_lib.quilt.get_latest_installer_version(), str)


def test_install_quilt_exceptions(tmp_path: pathlib.Path):
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.quilt.install_quilt("InvalidVersion", tmp_path)
    with pytest.raises(minecraft_launcher_lib.exceptions.UnsupportedVersion):
        minecraft_launcher_lib.quilt.install_quilt("1.0", tmp_path)
