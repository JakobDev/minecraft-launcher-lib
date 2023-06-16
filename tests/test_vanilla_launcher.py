import minecraft_launcher_lib
import pathlib
import shutil
import pytest
import json
import os


def _prepare_vanilla_launcher_test_env(tmp_path: pathlib.Path) -> None:
    shutil.copytree(os.path.join(os.path.dirname(__file__), "data", "vanilla_launcher"), tmp_path / ".minecraft")


def test_load_vanilla_launcher_profiles(tmp_path: pathlib.Path) -> None:
    _prepare_vanilla_launcher_test_env(tmp_path)

    profile_list = minecraft_launcher_lib.vanilla_launcher.load_vanilla_launcher_profiles(tmp_path / ".minecraft")

    assert len(profile_list) == 4

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

    assert profile_list[2]["name"] == "Latest release"
    assert profile_list[2]["version"] is None
    assert profile_list[2]["versionType"] == "latest-release"
    assert profile_list[2]["gameDirectory"] is None
    assert profile_list[2]["javaExecutable"] is None
    assert profile_list[2]["javaArguments"] is None
    assert profile_list[2]["customResolution"] is None

    assert profile_list[3]["name"] == "Latest snapshot"
    assert profile_list[3]["version"] is None
    assert profile_list[3]["versionType"] == "latest-snapshot"
    assert profile_list[3]["gameDirectory"] is None
    assert profile_list[3]["javaExecutable"] is None
    assert profile_list[3]["javaArguments"] is None
    assert profile_list[3]["customResolution"] is None


def test_vanilla_launcher_profile_to_minecraft_options() -> None:
    test_values = {"name": "test", "versionType": "latest-release"}
    assert len(minecraft_launcher_lib.vanilla_launcher.vanilla_launcher_profile_to_minecraft_options(test_values)) == 0
    assert minecraft_launcher_lib.vanilla_launcher.vanilla_launcher_profile_to_minecraft_options({**test_values, **{"gameDirectory": "test"}}) == {"gameDirectory": "test"}
    assert minecraft_launcher_lib.vanilla_launcher.vanilla_launcher_profile_to_minecraft_options({**test_values, **{"javaExecutable": "/testJava"}}) == {"executablePath": "/testJava"}
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


def _remove_none_values(none_dict: dict) -> dict:
    new_dict = {}
    for key, value in none_dict.items():
        if value is not None:
            new_dict[key] = value
    return new_dict


def _check_vanilla_profile_written(tmp_path: pathlib.Path, profile: minecraft_launcher_lib.types.VanillaLauncherProfile) -> None:
    temp_dir_count = 0
    while True:
        if not (tmp_path / str(temp_dir_count)).is_dir():
            break
        else:
            temp_dir_count += 1

    current_dir = (tmp_path / str(temp_dir_count))
    current_dir.mkdir()

    with open(os.path.join(os.path.dirname(__file__), "data", "vanilla_launcher", "launcher_profiles.json"), "r", encoding="utf-8") as f:
        json_data = json.load(f)

    json_data["profiles"] = {}

    with open(current_dir / "launcher_profiles.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False)

    minecraft_launcher_lib.vanilla_launcher.add_vanilla_launcher_profile(current_dir, profile)
    assert _remove_none_values(minecraft_launcher_lib.vanilla_launcher.load_vanilla_launcher_profiles(current_dir)[0]) == _remove_none_values(profile)


def test_add_vanilla_launcher_profile(tmp_path: pathlib.Path) -> None:
    _check_vanilla_profile_written(tmp_path, {"name": "test", "versionType": "latest-release"})
    _check_vanilla_profile_written(tmp_path, {"name": "test", "versionType": "latest-snapshot"})
    _check_vanilla_profile_written(tmp_path, {"name": "test", "versionType": "custom", "version": "test"})
    _check_vanilla_profile_written(tmp_path, {"name": "test", "versionType": "latest-release", "gameDirectory": "testGame"})
    _check_vanilla_profile_written(tmp_path, {"name": "test", "versionType": "latest-release", "javaExecutable": "testJava"})
    _check_vanilla_profile_written(tmp_path, {"name": "test", "versionType": "latest-release", "javaArguments": ["a", "b", "c"]})
    _check_vanilla_profile_written(tmp_path, {"name": "test", "versionType": "latest-release", "customResolution": {"width": 150, "height": 100}})

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidVanillaLauncherProfile):
        minecraft_launcher_lib.vanilla_launcher.add_vanilla_launcher_profile(tmp_path, {"name": "test", "versionType": "custom"})

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidVanillaLauncherProfile):
        minecraft_launcher_lib.vanilla_launcher.add_vanilla_launcher_profile(tmp_path, {"name": "test", "versionType": "latest-release", "gameDirectory": 123})

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidVanillaLauncherProfile):
        minecraft_launcher_lib.vanilla_launcher.add_vanilla_launcher_profile(tmp_path, {"name": "test", "versionType": "latest-release", "javaExecutable": 123})

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidVanillaLauncherProfile):
        minecraft_launcher_lib.vanilla_launcher.add_vanilla_launcher_profile(tmp_path, {"name": "test", "versionType": "latest-release", "javaArguments": [123]})

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidVanillaLauncherProfile):
        minecraft_launcher_lib.vanilla_launcher.add_vanilla_launcher_profile(tmp_path, {"name": "test", "versionType": "latest-release", "customResolution": {"width": "abc"}})


def test_do_vanilla_launcher_profiles_exists(tmp_path: pathlib.Path) -> None:
    assert minecraft_launcher_lib.vanilla_launcher.do_vanilla_launcher_profiles_exists(tmp_path / ".minecraft") is False
    _prepare_vanilla_launcher_test_env(tmp_path)
    assert minecraft_launcher_lib.vanilla_launcher.do_vanilla_launcher_profiles_exists(tmp_path / ".minecraft") is True
