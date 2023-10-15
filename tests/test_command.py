from ._test_helper import prepare_test_versions
import minecraft_launcher_lib
from typing import List
import platform
import pathlib
import pytest
import os


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
    prepare_test_versions(tmp_path)
    options = {}
    options["username"] = "Player"
    options["uuid"] = "Testuuid"
    options["token"] = "testtoken"
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert _check_argument(command, "--username", "Player")
    assert _check_argument(command, "--uuid", "Testuuid")
    assert _check_argument(command, "--accessToken", "testtoken")


def test_get_minecraft_command_java(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)

    # Test with option
    options = {"executablePath": "test"}
    command = minecraft_launcher_lib.command.get_minecraft_command("java", str(tmp_path), options)
    assert command[0] == "test"

    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command("java", str(tmp_path), {})
    assert command[0] == "java"

    # Test if using the runtime path

    java_path = (tmp_path / "runtime" / "java-runtime-test" / "linux" / "java-runtime-test" / "bin" / "java")
    os.makedirs(java_path.parent)
    java_path.touch()
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    command = minecraft_launcher_lib.command.get_minecraft_command("java", str(tmp_path), {})
    assert command[0] == str(java_path)


def test_get_minecraft_command_jvm_arguments(tmp_path: pathlib.Path):
    prepare_test_versions(tmp_path)
    options = {"jvmArguments": ["a", "b"]}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert command[1] == "a"
    assert command[2] == "b"


def test_get_minecraft_command_game_directory(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)

    # Test with option
    options = {"gameDirectory": "gamedir"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert _check_argument(command, "--gameDir", "gamedir")

    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), {})
    assert _check_argument(command, "--gameDir", str(tmp_path))


def test_get_minecraft_command_demo(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)
    # Test with option
    options = {"demo": True}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "--demo" in command
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), {})
    assert "--demo" not in command


def test_get_minecraft_command_custom_resolution(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)

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


def test_get_minecraft_command_natives_directory(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)
    # Test with option
    options = {"nativesDirectory": "test"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "-Djava.library.path=test" in command
    # Test without option
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), {})
    default_natives_path = os.path.join(tmp_path, "versions", "test1", "natives")
    assert f"-Djava.library.path={default_natives_path}"


def test_get_minecraft_command_logging_config(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)

    options = {"enableLoggingConfig": True}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "-Dlog4j.configurationFile=" + str(tmp_path / "assets" / "log_configs" / "client-1.12.xml") in command


def test_get_minecraft_command_server_port(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)

    options = {"server": "example.com"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert _check_argument(command, "--server", "example.com")
    assert "--port" not in command

    options["port"] = "123"
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert _check_argument(command, "--server", "example.com")
    assert _check_argument(command, "--port", "123")


def test_get_minecraft_command_disable_multiplayer_chat(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)

    options = {"disableMultiplayer": True}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "--disableMultiplayer" in command
    assert "--disableChat" not in command

    options = {"disableChat": True}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "--disableMultiplayer" not in command
    assert "--disableChat" in command


def test_get_minecraft_command_quick_play(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)

    options = {}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "--quickPlayPath" not in command
    assert "--quickPlaySingleplayer" not in command
    assert "--quickPlayMultiplayer" not in command
    assert "--quickPlayRealms" not in command

    options = {"quickPlayPath": "testPath"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert _check_argument(command, "--quickPlayPath", "testPath")
    assert "--quickPlaySingleplayer" not in command
    assert "--quickPlayMultiplayer" not in command
    assert "--quickPlayRealms" not in command

    options = {"quickPlaySingleplayer": "testSingleplayer"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "--quickPlayPath" not in command
    assert _check_argument(command, "--quickPlaySingleplayer", "testSingleplayer")
    assert "--quickPlayMultiplayer" not in command
    assert "--quickPlayRealms" not in command

    options = {"quickPlayMultiplayer": "testMultiplayer"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "--quickPlayPath" not in command
    assert "--quickPlaySingleplayer" not in command
    assert _check_argument(command, "--quickPlayMultiplayer", "testMultiplayer")
    assert "--quickPlayRealms" not in command

    options = {"quickPlayRealms": "testRealms"}
    command = minecraft_launcher_lib.command.get_minecraft_command("test1", str(tmp_path), options)
    assert "--quickPlayPath" not in command
    assert "--quickPlaySingleplayer" not in command
    assert "--quickPlayMultiplayer" not in command
    assert _check_argument(command, "--quickPlayRealms", "testRealms")


def test_get_minecraft_command_old_arguments(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)

    options = {}
    command = minecraft_launcher_lib.command.get_minecraft_command("natives", str(tmp_path), options)
    assert "--width" not in command
    assert "--height" not in command
    assert "--demo" not in command

    options = {"customResolution": True, "resolutionWidth": "1000", "resolutionHeight": "500"}
    command = minecraft_launcher_lib.command.get_minecraft_command("natives", str(tmp_path), options)
    assert _check_argument(command, "--width", "1000")
    assert _check_argument(command, "--height", "500")
    assert "--demo" not in command

    options = {"demo": True}
    command = minecraft_launcher_lib.command.get_minecraft_command("natives", str(tmp_path), options)
    assert "--width" not in command
    assert "--height" not in command
    assert "--demo" in command


def test_get_minecraft_command_inherit(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)

    options = {}
    minecraft_launcher_lib.command.get_minecraft_command("inherit", str(tmp_path), options)


def test_get_minecraft_command_extended(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    prepare_test_versions(tmp_path)

    minecraft_launcher_lib.command.get_minecraft_command("test2", str(tmp_path), {})


def test_get_minecraft_command_invalid_version(tmp_path: pathlib.Path) -> None:
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.command.get_minecraft_command("InvalidVersion", str(tmp_path), {})


def test_get_minecraft_command_with_path(tmp_path: pathlib.Path) -> None:
    prepare_test_versions(tmp_path)
    # Test if get_minecraft_command works with os.PathLike
    minecraft_launcher_lib.command.get_minecraft_command("test1", tmp_path, {})
