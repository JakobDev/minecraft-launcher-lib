# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"vanilla_launcher contains some functions for interacting with the Vanilla Minecraft Launcher"
from ._internal_types.vanilla_launcher_types import VanillaLauncherProfilesJson, VanillaLauncherProfilesJsonProfile
from .types import VanillaLauncherProfile, MinecraftOptions
from .exceptions import InvalidVanillaLauncherProfile
from .utils import get_latest_version
from ._helper import assert_func
import datetime
import json
import uuid
import os

__all__ = [
    "load_vanilla_launcher_profiles",
    "vanilla_launcher_profile_to_minecraft_options",
    "get_vanilla_launcher_profile_version",
    "add_vanilla_launcher_profile",
    "do_vanilla_launcher_profiles_exists"
]


def _is_vanilla_launcher_profile_valid(vanilla_profile: VanillaLauncherProfile) -> bool:
    "Checks if the given profile is valid"
    if not isinstance(vanilla_profile.get("name"), str):
        return False

    if vanilla_profile.get("versionType") not in ("latest-release", "latest-snapshot", "custom"):
        return False

    if vanilla_profile["versionType"] == "custom" and vanilla_profile.get("version") is None:
        return False

    if vanilla_profile.get("gameDirectory") is not None and not isinstance(vanilla_profile.get("gameDirectory"), str):
        return False

    if vanilla_profile.get("javaExecutable") is not None and not isinstance(vanilla_profile.get("javaExecutable"), str):
        return False

    if (java_arguments := vanilla_profile.get("javaArguments")) is not None:
        try:
            for i in java_arguments:
                assert_func(isinstance(i, str))
        except Exception:
            return False

    if (custom_resolution := vanilla_profile.get("customResolution")) is not None:
        try:
            assert_func(len(custom_resolution) == 2)
            assert_func(isinstance(custom_resolution["height"], int))
            assert_func(isinstance(custom_resolution["width"], int))
        except Exception:
            return False

    return True


def load_vanilla_launcher_profiles(minecraft_directory: str | os.PathLike) -> list[VanillaLauncherProfile]:
    """
    Loads the profiles of the Vanilla Launcher from the given Minecraft directory

    :param minecraft_directory: The Minecraft directory
    :return: A List with the Profiles
    """
    with open(os.path.join(minecraft_directory, "launcher_profiles.json"), "r", encoding="utf-8") as f:
        data: VanillaLauncherProfilesJson = json.load(f)

    profile_list: list[VanillaLauncherProfile] = []
    for value in data["profiles"].values():
        vanilla_profile: VanillaLauncherProfile = {}

        match value["type"]:
            case "latest-release":
                vanilla_profile["name"] = "Latest release"
            case "latest-snapshot":
                vanilla_profile["name"] = "Latest snapshot"
            case _:
                vanilla_profile["name"] = value["name"]

        match value["lastVersionId"]:
            case "latest-release":
                vanilla_profile["versionType"] = "latest-release"
                vanilla_profile["version"] = None
            case "latest-snapshot":
                vanilla_profile["versionType"] = "latest-snapshot"
                vanilla_profile["version"] = None
            case _:
                vanilla_profile["versionType"] = "custom"
                vanilla_profile["version"] = value["lastVersionId"]

        vanilla_profile["gameDirectory"] = value.get("gameDir")
        vanilla_profile["javaExecutable"] = value.get("javaDir")

        if "javaArgs" in value:
            vanilla_profile["javaArguments"] = value["javaArgs"].split(" ")
        else:
            vanilla_profile["javaArguments"] = None

        if "resolution" in value:
            vanilla_profile["customResolution"] = {
                "height": value["resolution"]["height"],
                "width": value["resolution"]["width"]
            }
        else:
            vanilla_profile["customResolution"] = None

        profile_list.append(vanilla_profile)

    return profile_list


def vanilla_launcher_profile_to_minecraft_options(vanilla_profile: VanillaLauncherProfile) -> MinecraftOptions:
    """
    Converts a VanillaLauncherProfile into a Options dict, that can be used by :func:`~minecraft_launcher_lib.command.get_minecraft_command`.
    You still need to add the Login Data to the Options before you can use it.

    :param vanilla_profile: The profile as returned by :func:`load_vanilla_launcher_profiles`
    :raises InvalidVanillaLauncherProfile: The given Profile is invalid
    :return: The Options Dict
    """
    if not _is_vanilla_launcher_profile_valid(vanilla_profile):
        raise InvalidVanillaLauncherProfile(vanilla_profile)

    options: MinecraftOptions = {}

    if (game_directory := vanilla_profile.get("gameDirectory")) is not None:
        options["gameDirectory"] = game_directory

    if (java_executable := vanilla_profile.get("javaExecutable")) is not None:
        options["executablePath"] = java_executable

    if (java_arguments := vanilla_profile.get("javaArguments")) is not None:
        options["jvmArguments"] = java_arguments

    if (custom_resolution := vanilla_profile.get("customResolution")) is not None:
        options["customResolution"] = True
        options["resolutionWidth"] = str(custom_resolution["width"])
        options["resolutionHeight"] = str(custom_resolution["height"])

    return options


def get_vanilla_launcher_profile_version(vanilla_profile: VanillaLauncherProfile) -> str:
    """
    Returns the Minecraft version of the VanillaProfile. Handles ``latest-release`` and ``latest-snapshot``.

    :param vanilla_profile: The Profile
    :type vanilla_profile: VanillaLauncherProfile
    :raises InvalidVanillaLauncherProfile: The given Profile is invalid
    :return: The Minecraft version
    """
    if not _is_vanilla_launcher_profile_valid(vanilla_profile):
        raise InvalidVanillaLauncherProfile(vanilla_profile)

    if vanilla_profile["versionType"] == "latest-release":
        return get_latest_version()["release"]
    elif vanilla_profile["versionType"] == "latest-snapshot":
        return get_latest_version()["snapshot"]
    elif vanilla_profile["versionType"] == "custom":
        return vanilla_profile["version"]  # type: ignore


def add_vanilla_launcher_profile(minecraft_directory: str | os.PathLike, vanilla_profile: VanillaLauncherProfile) -> None:
    """
    Adds a new Profile to the Vanilla Launcher

    :param minecraft_directory: The Minecraft directory
    :param vanilla_profile: The new Profile
    :raises InvalidVanillaLauncherProfile: The given Profile is invalid
    """
    if not _is_vanilla_launcher_profile_valid(vanilla_profile):
        raise InvalidVanillaLauncherProfile(vanilla_profile)

    with open(os.path.join(minecraft_directory, "launcher_profiles.json"), "r", encoding="utf-8") as f:
        data: VanillaLauncherProfilesJson = json.load(f)

    new_profile: VanillaLauncherProfilesJsonProfile = {}
    new_profile["name"] = vanilla_profile["name"]

    if vanilla_profile["versionType"] == "latest-release":
        new_profile["lastVersionId"] = "latest-release"
    elif vanilla_profile["versionType"] == "latest-snapshot":
        new_profile["lastVersionId"] = "latest-snapshot"
    elif vanilla_profile["versionType"] == "custom":
        # _is_vanilla_launcher_profile_valid() ensures that version is not None, when versionType is set to custom, so we can ignore the mypy error here
        new_profile["lastVersionId"] = vanilla_profile["version"]  # type: ignore

    if (game_directory := vanilla_profile.get("gameDirectory")) is not None:
        new_profile["gameDir"] = game_directory

    if (java_executable := vanilla_profile.get("javaExecutable")) is not None:
        new_profile["javaDir"] = java_executable

    if (java_arguments := vanilla_profile.get("javaArguments")) is not None:
        new_profile["javaArgs"] = " ".join(java_arguments)

    if (custom_resolution := vanilla_profile.get("customResolution")) is not None:
        new_profile["resolution"] = {
            "height": custom_resolution["height"],
            "width": custom_resolution["width"]
        }

    new_profile["created"] = datetime.datetime.now().isoformat()
    new_profile["lastUsed"] = datetime.datetime.now().isoformat()
    new_profile["type"] = "custom"

    # Generate a Key for the Profile
    while True:
        key = str(uuid.uuid4())
        if key not in data["profiles"]:
            break

    data["profiles"][key] = new_profile

    with open(os.path.join(minecraft_directory, "launcher_profiles.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def do_vanilla_launcher_profiles_exists(minecraft_directory: str | os.PathLike) -> bool:
    """
    Checks if profiles from the vanilla launcher can be found

    :param minecraft_directory: The Minecraft directory
    :return: If profiles exists
    """
    return os.path.isfile(os.path.join(minecraft_directory, "launcher_profiles.json"))
