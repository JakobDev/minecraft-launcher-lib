import minecraft_launcher_lib
import pathlib
import pytest


def test_install_minecraft_version_invalid_version(tmp_path: pathlib.Path):
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.install.install_minecraft_version("InvalidVersion", str(tmp_path))
