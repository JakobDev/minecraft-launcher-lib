import minecraft_launcher_lib
from typing import List
import pathlib
import pytest
import shutil
import os


def _prepare_command_test_env(tmp_path: pathlib.Path) -> None:
    shutil.copytree(os.path.join(os.path.dirname(__file__), "data", "versions"), tmp_path / "versions")


def _check_argument(command: List[str], argument: str, value: str) -> bool:
    # Checks if a argument has the given value
    try:
        index = command.index(argument)
    except Exception:
        return False
    try:
        return command[index + 1] == value
    except Exception:
        return False


def test_get_minecraft_command_executable_basic(tmp_path: pathlib.Path) -> None:
    _prepare_command_test_env(tmp_path)
    options = {}
    options["username"] = "Player"
    options["uuid"] = "Testuuid"
    options["token"] = "testtoken"
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert _check_argument(command, "--username", "Player")
    assert _check_argument(command, "--uuid", "Testuuid")
    assert _check_argument(command, "--accessToken", "testtoken")


def test_get_minecraft_command_executable_path(tmp_path: pathlib.Path):
    _prepare_command_test_env(tmp_path)
    # Test with option
    options = {"executablePath": "test"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert command[0] == "test"
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), {})
    assert command[0] == "java"


def test_get_minecraft_command_jvm_arguments(tmp_path: pathlib.Path):
    _prepare_command_test_env(tmp_path)
    options = {"jvmArguments": ["a", "b"]}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert command[1] == "a"
    assert command[2] == "b"


def test_get_minecraft_command_game_directory(tmp_path: pathlib.Path):
    _prepare_command_test_env(tmp_path)
    # Test with option
    options = {"gameDirectory": "gamedir"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert _check_argument(command, "--gameDir", "gamedir")
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), {})
    assert _check_argument(command, "--gameDir", str(tmp_path))


def test_get_minecraft_command_demo(tmp_path: pathlib.Path):
    _prepare_command_test_env(tmp_path)
    # Test with option
    options = {"demo": True}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "--demo" in command
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), {})
    assert "--demo" not in command


def test_get_minecraft_command_custom_resolution(tmp_path: pathlib.Path):
    _prepare_command_test_env(tmp_path)
    # Test default values of width and height
    options = {"customResolution": True}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert _check_argument(command, "--width", "854")
    assert _check_argument(command, "--height", "480")
    # Test custom values of width and height
    options = {}
    options["customResolution"] = True
    options["resolutionWidth"] = "1000"
    options["resolutionHeight"] = "500"
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert _check_argument(command, "--width", "1000")
    assert _check_argument(command, "--height", "500")
    # Test without options
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), {})
    assert "--width" not in command
    assert "--height" not in command


def test_get_minecraft_command_natives_directory(tmp_path: pathlib.Path):
    _prepare_command_test_env(tmp_path)
    # Test with option
    options = {"nativesDirectory": "test"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "-Djava.library.path=test" in command
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), {})
    default_natives_path = os.path.join(tmp_path, "versions", "test1", "natives")
    assert f"-Djava.library.path={default_natives_path}"


def test_get_minecraft_command_invalid_version(tmp_path: pathlib.Path):
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.command.get_minecraft_command("InvalidVersion", str(tmp_path), {})


def test_get_minecraft_command_with_path(tmp_path: pathlib.Path):
    _prepare_command_test_env(tmp_path)
    # Test if get_minecraft_command works with os.PathLike
    minecraft_launcher_lib.command.get_minecraft_command("test1", tmp_path, {})
