from typing import List
import minecraft_launcher_lib
import requests
import pytest
import shutil
import os


def check_argument(command: List[str], argument: str, value: str) -> bool:
    # Checks if a argument has the given value
    try:
        index = command.index(argument)
    except:
        return False
    try:
        return command[index + 1] == value
    except:
        return False


def download_test_version(tmpdir) -> str:
    # Download a random version for test
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json").json()
    version_id = version_list["versions"][0]["id"]
    r = requests.get(version_list["versions"][0]["url"], stream=True)
    os.makedirs(os.path.join(tmpdir, "versions", version_id))
    with open(os.path.join(tmpdir, "versions", version_id, f"{version_id}.json"), 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    return version_id


def test_get_minecraft_command_executable_basic(tmpdir):
    version_id = download_test_version(tmpdir)
    options = {}
    options["username"] = "Player"
    options["uuid"] = "Testuuid"
    options["token"] = "testtoken"
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), options)
    assert check_argument(command, "--username", "Player")
    assert check_argument(command, "--uuid", "Testuuid")
    assert check_argument(command, "--accessToken", "testtoken")


def test_get_minecraft_command_executable_path(tmpdir):
    version_id = download_test_version(tmpdir)
    # Test with option
    options = {"executablePath": "test"}
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), options)
    assert command[0] == "test"
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), {})
    assert command[0] == "java"


def test_get_minecraft_command_jvm_arguments(tmpdir):
    version_id = download_test_version(tmpdir)
    options = {"jvmArguments": ["a", "b"]}
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), options)
    assert command[1] == "a"
    assert command[2] == "b"


def test_get_minecraft_command_game_directory(tmpdir):
    version_id = download_test_version(tmpdir)
    # Test with option
    options = {"gameDirectory": "gamedir"}
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), options)
    assert check_argument(command, "--gameDir", "gamedir")
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), {})
    assert check_argument(command, "--gameDir", str(tmpdir))


def test_get_minecraft_command_demo(tmpdir):
    version_id = download_test_version(tmpdir)
    # Test with option
    options = {"demo": True}
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), options)
    assert "--demo" in command
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), {})
    assert "--demo" not in command


def test_get_minecraft_command_custom_resolution(tmpdir):
    version_id = download_test_version(tmpdir)
    # Test default values of width and height
    options = {"customResolution": True}
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), options)
    assert check_argument(command, "--width", "854")
    assert check_argument(command, "--height", "480")
    # Test custom values of width and height
    options = {}
    options["customResolution"] = True
    options["resolutionWidth"] = "1000"
    options["resolutionHeight"] = "500"
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), options)
    assert check_argument(command, "--width", "1000")
    assert check_argument(command, "--height", "500")
    # Test without options
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), {})
    assert "--width" not in command
    assert "--height" not in command


def test_get_minecraft_command_natives_directory(tmpdir):
    version_id = download_test_version(tmpdir)
    # Test with option
    options = {"nativesDirectory": "test"}
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), options)
    assert "-Djava.library.path=test" in command
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command(version_id, str(tmpdir), {})
    default_natives_path = os.path.join(tmpdir, "versions", version_id, "natives")
    assert f"-Djava.library.path={default_natives_path}"


def test_get_minecraft_command_invalid_version(tmpdir):
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.command.get_minecraft_command("InvalidVersion", str(tmpdir), {})
