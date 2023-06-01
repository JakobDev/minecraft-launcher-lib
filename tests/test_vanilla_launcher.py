import minecraft_launcher_lib
import pathlib
import shutil
import pytest
import os


def _prepare_vanilla_launcher_test_env(tmp_path: pathlib.Path) -> None:
    shutil.copytree(os.path.join(os.path.dirname(__file__), "data", "vanilla_launcher"), tmp_path / ".minecraft")


def test_load_vanilla_launcher_profiles(tmp_path: pathlib.Path) -> None:
    _prepare_vanilla_launcher_test_env(tmp_path)

    profile_list = minecraft_launcher_lib.vanilla_launcher.load_vanilla_launcher_profiles(tmp_path / ".minecraft")

    assert len(profile_list) == 2

    assert profile_list[0]["name"] == "Test"
    assert profile_list[0]["version"] is None
    assert profile_list[0]["versionType"] == "latest-release"
    assert profile_list[0]["gameDirectory"] is None
    assert profile_list[0]["javaExecutable"] is None
    assert profile_list[0]["javaArguments"] == ["-Xmx2G", "-XX:+UnlockExperimentalVMOptions", "-XX:+UseG1GC", "-XX:G1NewSizePercent=20", "-XX:G1ReservePercent=20", "-XX:MaxGCPauseMillis=50", "-XX:G1HeapRegionSize=32M"]
    assert profile_list[0]["customResolution"]["height"] == 400
    assert profile_list[0]["customResolution"]["width"] == 450

    assert profile_list[1]["name"] == "Forge1.16.5"
    assert profile_list[1]["version"] == "1.16.5-forge-36.1.24"
    assert profile_list[1]["versionType"] == "custom"
    assert profile_list[1]["gameDirectory"] == "/gametest"
    assert profile_list[1]["javaExecutable"] == "/javatest"
    assert profile_list[1]["javaArguments"] is None
    assert profile_list[1]["customResolution"] is None


def test_vanilla_launcher_profile_to_minecraft_options() -> None:
    test_values = {"name": "test", "versionType": "latest-release"}
    assert len(minecraft_launcher_lib.vanilla_launcher.vanilla_launcher_profile_to_minecraft_options(test_values)) == 0
    assert minecraft_launcher_lib.vanilla_launcher.vanilla_launcher_profile_to_minecraft_options({**test_values, **{"gameDirectory": "test"}}) == {"gameDirectory": "test"}
    assert minecraft_launcher_lib.vanilla_launcher.vanilla_launcher_profile_to_minecraft_options({**test_values, **{"javaArguments": ["a", "b"]}}) == {"jvmArguments": ["a", "b"]}
    assert minecraft_launcher_lib.vanilla_launcher.vanilla_launcher_profile_to_minecraft_options({**test_values, **{"customResolution": {"height": 100, "width": 150}}}) == {
        "customResolution": True,
        "resolutionWidth": "150",
        "resolutionHeight": "100"
    }

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidVanillaLauncherProfile):
        minecraft_launcher_lib.vanilla_launcher.vanilla_launcher_profile_to_minecraft_options({})


def test_get_vanilla_launcher_profile_version() -> None:
    latest_version = minecraft_launcher_lib.utils.get_latest_version()

    assert minecraft_launcher_lib.vanilla_launcher.get_vanilla_launcher_profile_version({"name": "test", "version": "test", "versionType": "latest-release"}) == latest_version["release"]
    assert minecraft_launcher_lib.vanilla_launcher.get_vanilla_launcher_profile_version({"name": "test", "version": "test", "versionType": "latest-snapshot"}) == latest_version["snapshot"]
    assert minecraft_launcher_lib.vanilla_launcher.get_vanilla_launcher_profile_version({"name": "test", "version": "test", "versionType": "custom"}) == "test"

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidVanillaLauncherProfile):
        minecraft_launcher_lib.vanilla_launcher.get_vanilla_launcher_profile_version({"name": "test", "version": "test", "versionType": "test"})


def test_do_vanilla_launcher_profiles_exists(tmp_path: pathlib.Path) -> None:
    assert minecraft_launcher_lib.vanilla_launcher.do_vanilla_launcher_profiles_exists(tmp_path / ".minecraft") is False
    _prepare_vanilla_launcher_test_env(tmp_path)
    assert minecraft_launcher_lib.vanilla_launcher.do_vanilla_launcher_profiles_exists(tmp_path / ".minecraft") is True
