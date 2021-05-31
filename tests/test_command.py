import minecraft_launcher_lib
import requests
import pytest
import shutil
import os


def test_get_minecraft_command(tmpdir):
    # Download a random version for test
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    version_id = version_list["versions"][0]["id"]
    r = requests.get(version_list["versions"][0]["url"], stream=True)
    os.makedirs(os.path.join(tmpdir, "versions", version_id))
    with open(os.path.join(tmpdir, "versions", version_id, f"{version_id}.json"), 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    # Get the command
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), {})
    for i in command:
        assert isinstance(i, str)


def test_get_minecraft_command_invalid_version(tmpdir):
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.command.get_minecraft_command("InvalidVersion", str(tmpdir), {})
