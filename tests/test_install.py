import minecraft_launcher_lib
import pytest


def test_install_minecraft_version_invalid_version(tmpdir):
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.install.install_minecraft_version("InvalidVersion", str(tmpdir))
