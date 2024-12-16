# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"command contains the function for creating the minecraft command"
from ._helper import parse_rule_list, inherit_json, get_classpath_separator, get_library_path
from ._internal_types.shared_types import ClientJson, ClientJsonArgumentRule
from .runtime import get_executable_path
from .exceptions import VersionNotFound
from .utils import get_library_version
from .types import MinecraftOptions
from .natives import get_natives
import json
import copy
import os

__all__ = ["get_minecraft_command"]


def get_libraries(data: ClientJson, path: str) -> str:
    """
    Returns the argument with all libs that come after -cp
    """
    classpath_seperator = get_classpath_separator()
    libstr = ""
    for i in data["libraries"]:
        if "rules" in i and not parse_rule_list(i["rules"], {}):
            continue

        libstr += get_library_path(i["name"], path) + classpath_seperator
        native = get_natives(i)
        if native != "":
            if "downloads" in i and "path" in i["downloads"]["classifiers"][native]:  # type: ignore
                libstr += os.path.join(path, "libraries", i["downloads"]["classifiers"][native]["path"]) + classpath_seperator  # type: ignore
            else:
                libstr += get_library_path(i["name"] + "-" + native, path) + classpath_seperator

    if "jar" in data:
        libstr = libstr + os.path.join(path, "versions", data["jar"], data["jar"] + ".jar")
    else:
        libstr = libstr + os.path.join(path, "versions", data["id"], data["id"] + ".jar")

    return libstr


def replace_arguments(argstr: str, versionData: ClientJson, path: str, options: MinecraftOptions, classpath: str) -> str:
    """
    Replace all placeholder in arguments with the needed value
    """
    argstr = argstr.replace("${natives_directory}", options["nativesDirectory"])
    argstr = argstr.replace("${launcher_name}", options.get("launcherName", "minecraft-launcher-lib"))
    argstr = argstr.replace("${launcher_version}", options.get("launcherVersion", get_library_version()))
    argstr = argstr.replace("${classpath}", classpath)
    argstr = argstr.replace("${auth_player_name}", options.get("username", "{username}"))
    argstr = argstr.replace("${version_name}", versionData["id"])
    argstr = argstr.replace("${game_directory}", options.get("gameDirectory", path))
    argstr = argstr.replace("${assets_root}", os.path.join(path, "assets"))
    argstr = argstr.replace("${assets_index_name}", versionData.get("assets", versionData["id"]))
    argstr = argstr.replace("${auth_uuid}", options.get("uuid", "{uuid}"))
    argstr = argstr.replace("${auth_access_token}", options.get("token", "{token}"))
    argstr = argstr.replace("${user_type}", "msa")
    argstr = argstr.replace("${version_type}", versionData["type"])
    argstr = argstr.replace("${user_properties}", "{}")
    argstr = argstr.replace("${resolution_width}", options.get("resolutionWidth", "854"))
    argstr = argstr.replace("${resolution_height}", options.get("resolutionHeight", "480"))
    argstr = argstr.replace("${game_assets}", os.path.join(path, "assets", "virtual", "legacy"))
    argstr = argstr.replace("${auth_session}", options.get("token", "{token}"))
    argstr = argstr.replace("${library_directory}", os.path.join(path, "libraries"))
    argstr = argstr.replace("${classpath_separator}", get_classpath_separator())
    argstr = argstr.replace("${quickPlayPath}", options.get("quickPlayPath") or "{quickPlayPath}")
    argstr = argstr.replace("${quickPlaySingleplayer}", options.get("quickPlaySingleplayer") or "{quickPlaySingleplayer}")
    argstr = argstr.replace("${quickPlayMultiplayer}", options.get("quickPlayMultiplayer") or "{quickPlayMultiplayer}")
    argstr = argstr.replace("${quickPlayRealms}", options.get("quickPlayRealms") or "{quickPlayRealms}")
    return argstr


def get_arguments_string(versionData: ClientJson, path: str, options: MinecraftOptions, classpath: str) -> list[str]:
    """
    Turns the argument string from the client.json into a list
    """
    arglist: list[str] = []

    for v in versionData["minecraftArguments"].split(" "):
        v = replace_arguments(v, versionData, path, options, classpath)
        arglist.append(v)

    # Custom resolution is not in the list
    if options.get("customResolution", False):
        arglist.append("--width")
        arglist.append(options.get("resolutionWidth", "854"))
        arglist.append("--height")
        arglist.append(options.get("resolutionHeight", "480"))

    if options.get("demo", False):
        arglist.append("--demo")

    return arglist


def get_arguments(data: list[str | ClientJsonArgumentRule], versionData: ClientJson, path: str, options: MinecraftOptions, classpath: str) -> list[str]:
    """
    Returns all arguments from the client.json
    """
    arglist: list[str] = []
    for i in data:
        # i could be the argument
        if isinstance(i, str):
            arglist.append(replace_arguments(i, versionData, path, options, classpath))
        else:
            # Rules might has 2 different names in different client.json
            if "compatibilityRules" in i and not parse_rule_list(i["compatibilityRules"], options):
                continue

            if "rules" in i and not parse_rule_list(i["rules"], options):
                continue

            # Sometimes  i["value"] is the argument
            if isinstance(i["value"], str):
                arglist.append(replace_arguments(i["value"], versionData, path, options, classpath))
            # Sometimes i["value"] is a list of arguments
            else:
                for v in i["value"]:
                    v = replace_arguments(v, versionData, path, options, classpath)
                    arglist.append(v)
    return arglist


def get_minecraft_command(version: str, minecraft_directory: str | os.PathLike, options: MinecraftOptions) -> list[str]:
    """
    Returns the command for running minecraft as list. The given command can be executed with subprocess. Use :func:`~minecraft_launcher_lib.utils.get_minecraft_directory` to get the default Minecraft directory.

    :param version: The Minecraft version
    :param minecraft_directory: The path to your Minecraft directory
    :param options: Some Options (see below)

    ``options`` is a dict:

    .. code:: python

        options = {
            # This is needed
            "username": The Username,
            "uuid": uuid of the user,
            "token": the accessToken,
            # This is optional
            "executablePath": "java", # The path to the java executable
            "defaultExecutablePath": "java", # The path to the java executable if the client.json has none
            "jvmArguments": [], #The jvmArguments
            "launcherName": "minecraft-launcher-lib", # The name of your launcher
            "launcherVersion": "1.0", # The version of your launcher
            "gameDirectory": "/home/user/.minecraft", # The gameDirectory (default is the path given in arguments)
            "demo": False, # Run Minecraft in demo mode
            "customResolution": False, # Enable custom resolution
            "resolutionWidth": "854", # The resolution width
            "resolutionHeight": "480", # The resolution height
            "server": "example.com", # The IP of a server where Minecraft connect to after start
            "port": "123", # The port of a server where Minecraft connect to after start
            "nativesDirectory": "minecraft_directory/versions/version/natives", # The natives directory
            "enableLoggingConfig": False, # Enable use of the log4j configuration file
            "disableMultiplayer": False, # Disables the multiplayer
            "disableChat": False, # Disables the chat
            "quickPlayPath": None, # The Quick Play Path
            "quickPlaySingleplayer": None, # The Quick Play Singleplayer
            "quickPlayMultiplayer": None, # The Quick Play Multiplayer
            "quickPlayRealms": None, # The Quick Play Realms
        }

    You can use the :doc:`microsoft_account` module to get the needed information.
    For more information about the options take a look at the :doc:`/tutorial/more_launch_options` tutorial.
    """
    path = str(minecraft_directory)

    if not os.path.isdir(os.path.join(path, "versions", version)):
        raise VersionNotFound(version)

    options = copy.deepcopy(options)

    with open(os.path.join(path, "versions", version, version + ".json"), "r", encoding="utf-8") as f:
        data: ClientJson = json.load(f)

    if "inheritsFrom" in data:
        data = inherit_json(data, path)

    options["nativesDirectory"] = options.get("nativesDirectory", os.path.join(path, "versions", data["id"], "natives"))
    classpath = get_libraries(data, path)

    command: list[str] = []
    # Add Java executable
    if "executablePath" in options:
        command.append(options["executablePath"])
    elif "javaVersion" in data:
        java_path = get_executable_path(data["javaVersion"]["component"], path)
        if java_path is None:
            command.append("java")
        else:
            command.append(java_path)
    else:
        command.append(options.get("defaultExecutablePath", "java"))

    if "jvmArguments" in options:
        command = command + options["jvmArguments"]

    # Newer Versions have jvmArguments in client.json
    if isinstance(data.get("arguments", None), dict):
        if "jvm" in data["arguments"]:
            command = command + get_arguments(data["arguments"]["jvm"], data, path, options, classpath)
        else:
            command.append("-Djava.library.path=" + options["nativesDirectory"])
            command.append("-cp")
            command.append(classpath)
    else:
        command.append("-Djava.library.path=" + options["nativesDirectory"])
        command.append("-cp")
        command.append(classpath)

    # The argument for the logger file
    if options.get("enableLoggingConfig", False):
        if "logging" in data:
            if len(data["logging"]) != 0:
                logger_file = os.path.join(path, "assets", "log_configs", data["logging"]["client"]["file"]["id"])
                command.append(data["logging"]["client"]["argument"].replace("${path}", logger_file))

    command.append(data["mainClass"])

    if "minecraftArguments" in data:
        # For older versions
        command = command + get_arguments_string(data, path, options, classpath)
    else:
        command = command + get_arguments(data["arguments"]["game"], data, path, options, classpath)

    if "server" in options:
        command.append("--server")
        command.append(options["server"])
        if "port" in options:
            command.append("--port")
            command.append(options["port"])

    if options.get("disableMultiplayer", False):
        command.append("--disableMultiplayer")

    if options.get("disableChat", False):
        command.append("--disableChat")

    return command
