import minecraft_launcher_lib
import pytest


def test_vanilla_launcher_profile_to_minecraft_options():
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


def test_get_vanilla_launcher_profile_version():
    latest_version = minecraft_launcher_lib.utils.get_latest_version()

    assert minecraft_launcher_lib.vanilla_launcher.get_vanilla_launcher_profile_version({"name": "test", "version": "test", "versionType": "latest-release"}) == latest_version["release"]
    assert minecraft_launcher_lib.vanilla_launcher.get_vanilla_launcher_profile_version({"name": "test", "version": "test", "versionType": "latest-snapshot"}) == latest_version["snapshot"]
    assert minecraft_launcher_lib.vanilla_launcher.get_vanilla_launcher_profile_version({"name": "test", "version": "test", "versionType": "custom"}) == "test"

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidVanillaLauncherProfile):
        minecraft_launcher_lib.vanilla_launcher.get_vanilla_launcher_profile_version({"name": "test", "version": "test", "versionType": "test"})
