import minecraft_launcher_lib
import pytest


def test_extract_natives_invalid_version(tmpdir):
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.natives.extract_natives("InvalidVersion", str(tmpdir), {})
