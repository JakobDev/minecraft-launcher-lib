import minecraft_launcher_lib
import pathlib
import pytest


def test_extract_natives_invalid_version(tmp_path: pathlib.Path):
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.natives.extract_natives("InvalidVersion", str(tmp_path), {})
