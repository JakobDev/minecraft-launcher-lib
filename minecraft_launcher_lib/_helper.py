# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"This module contains some helper functions. It should nt be used outside minecraft_launcher_lib"
from .exceptions import FileOutsideMinecraftDirectory, InvalidChecksum, VersionNotFound
from ._internal_types.shared_types import ClientJson, ClientJsonRule, ClientJsonLibrary
from ._internal_types.helper_types import RequestsResponseCache, MavenMetadata
from .types import MinecraftOptions, CallbackDict
from typing import Literal, Any
import datetime
import requests
import platform
import hashlib
import zipfile
import shutil
import lzma
import json
import sys
import re
import os


def empty(arg: Any) -> None:
    """
    This function is just a placeholder
    """
    pass


def check_path_inside_minecraft_directory(minecraft_directory: str | os.PathLike, path: str | os.PathLike) -> None:
    """
    Raises a FileOutsideMinecraftDirectory if the Path is not in the given Directory
    """
    if not os.path.abspath(path).startswith(os.path.abspath(minecraft_directory)):
        raise FileOutsideMinecraftDirectory(os.path.abspath(path), os.path.abspath(minecraft_directory))


def download_file(url: str, path: str, callback: CallbackDict = {}, sha1: str | None = None, lzma_compressed: bool | None = False, session: requests.sessions.Session | None = None, minecraft_directory: str | os.PathLike | None = None, overwrite: bool | None = False) -> bool:
    """
    Downloads a file into the given path. Check sha1 if given.
    """
    # Check if the Path is outside the given Minecraft Directory
    if minecraft_directory is not None:
        check_path_inside_minecraft_directory(minecraft_directory, path)

    if os.path.isfile(path) and not overwrite:
        if sha1 is None:
            return False
        elif get_sha1_hash(path) == sha1:
            return False

    try:
        os.makedirs(os.path.dirname(path))
    except Exception:
        pass

    callback.get("setStatus", empty)("Download " + os.path.basename(path))

    if session is None:
        r = requests.get(url, stream=True, headers={"user-agent": get_user_agent()})
    else:
        r = session.get(url, stream=True, headers={"user-agent": get_user_agent()})

    if r.status_code != 200:
        return False

    with open(path, 'wb') as f:
        r.raw.decode_content = True
        if lzma_compressed:
            f.write(lzma.decompress(r.content))
        else:
            shutil.copyfileobj(r.raw, f)

    if sha1 is not None:
        checksum = get_sha1_hash(path)
        if checksum != sha1:
            raise InvalidChecksum(url, path, sha1, checksum)

    return True


def parse_single_rule(rule: ClientJsonRule, options: MinecraftOptions) -> bool:
    """
    Parse a single rule from the versions.json
    """
    if rule["action"] == "allow":
        returnvalue = False
    elif rule["action"] == "disallow":
        returnvalue = True

    for os_key, os_value in rule.get("os", {}).items():
        if os_key == "name":
            if os_value == "windows" and platform.system() != 'Windows':
                return returnvalue
            elif os_value == "osx" and platform.system() != 'Darwin':
                return returnvalue
            elif os_value == "linux" and platform.system() != 'Linux':
                return returnvalue
        elif os_key == "arch":
            if os_value == "x86" and platform.architecture()[0] != "32bit":
                return returnvalue
        elif os_key == "version":
            if not re.match(os_value, get_os_version()):
                return returnvalue

    for features_key in rule.get("features", {}).keys():
        if features_key == "has_custom_resolution" and not options.get("customResolution", False):
            return returnvalue
        elif features_key == "is_demo_user" and not options.get("demo", False):
            return returnvalue
        elif features_key == "has_quick_plays_support" and options.get("quickPlayPath") is None:
            return returnvalue
        elif features_key == "is_quick_play_singleplayer" and options.get("quickPlaySingleplayer") is None:
            return returnvalue
        elif features_key == "is_quick_play_multiplayer" and options.get("quickPlayMultiplayer") is None:
            return returnvalue
        elif features_key == "is_quick_play_realms" and options.get("quickPlayRealms") is None:
            return returnvalue

    return not returnvalue


def parse_rule_list(rules: list[ClientJsonRule], options: MinecraftOptions) -> bool:
    """
    Parse a list of rules
    """
    for i in rules:
        if not parse_single_rule(i, options):
            return False

    return True


def _get_lib_name_without_version(lib: ClientJsonLibrary) -> str:
    """
    Returns the library name but without the version part
    e.g. org.ow2.asm:asm:9.7.1 -> org.ow2.asm:asm
    """
    return ":".join(lib["name"].split(":")[:-1])


def inherit_json(original_data: ClientJson, path: str | os.PathLike) -> ClientJson:
    """
    Implement the inheritsFrom function
    See https://github.com/tomsik68/mclauncher-api/wiki/Version-Inheritance-&-Forge
    """
    inherit_version = original_data["inheritsFrom"]

    with open(os.path.join(path, "versions", inherit_version, inherit_version + ".json")) as f:
        new_data: ClientJson = json.load(f)

    # Inheriting the libs is a bit special
    # If the lib is already present in the client.json in a different, it can't be inherited
    # So first we need a dict which contains all libs that are already present
    original_libs: dict[str, bool] = {}
    for current_lib in original_data.get("libraries", []):
        lib_name = _get_lib_name_without_version(current_lib)
        original_libs[lib_name] = True

    # Now we can attach all libs from the inherited version that are not already existing
    lib_list = original_data.get("libraries", [])
    for current_lib in new_data["libraries"]:
        lib_name = _get_lib_name_without_version(current_lib)
        if lib_name not in original_libs:
            lib_list.append(current_lib)

    new_data["libraries"] = lib_list

    for key, value in original_data.items():
        if key == "libraries":
            # We already had inherited the libs
            continue

        if isinstance(value, list) and isinstance(new_data.get(key, None), list):
            new_data[key] = value + new_data[key]  # type: ignore
        elif isinstance(value, dict) and isinstance(new_data.get(key, None), dict):
            for a, b in value.items():
                if isinstance(b, list):
                    new_data[key][a] = new_data[key][a] + b  # type: ignore
        else:
            new_data[key] = value  # type: ignore

    return new_data


def get_library_path(name: str, path: str | os.PathLike) -> str:
    """
    Returns the path from a library name
    """
    libpath = os.path.join(path, "libraries")
    parts = name.split(":")
    base_path, libname, version = parts[0:3]
    for i in base_path.split("."):
        libpath = os.path.join(libpath, i)
    try:
        version, fileend = version.split("@")
    except ValueError:
        fileend = "jar"

    # construct a filename with the remaining parts
    filename = f"{libname}-{version}{''.join(map(lambda p: f'-{p}', parts[3:]))}.{fileend}"
    libpath = os.path.join(libpath, libname, version, filename)
    return libpath


def get_jar_mainclass(path: str) -> str:
    """
    Returns the mainclass of a given jar
    """
    zf = zipfile.ZipFile(path)
    # Parse the MANIFEST.MF
    with zf.open("META-INF/MANIFEST.MF") as f:
        lines = f.read().decode("utf-8").splitlines()
    zf.close()
    content = {}
    for i in lines:
        try:
            key, value = i.split(":")
            content[key] = value[1:]
        except Exception:
            pass
    return content["Main-Class"]


def get_sha1_hash(path: str) -> str:
    """
    Calculate the sha1 checksum of a file
    Source: https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    """
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def get_os_version() -> str:
    """
    Try to implement System.getProperty("os.version") from Java for use in rules
    This doesn't work on mac yet
    """
    if platform.system() == "Windows":
        ver = sys.getwindowsversion()  # type: ignore
        return f"{ver.major}.{ver.minor}"
    elif platform.system == "Darwin":
        return ""
    else:
        return platform.uname().release


_user_agent_cache = None


def get_user_agent() -> str:
    """
    Returns the user agent of minecraft-launcher-lib
    """
    global _user_agent_cache
    if _user_agent_cache is not None:
        return _user_agent_cache
    else:
        with open(os.path.join(os.path.dirname(__file__), "version.txt"), "r", encoding="utf-8") as f:
            _user_agent_cache = "minecraft-launcher-lib/" + f.read().strip()
            return _user_agent_cache


def get_classpath_separator() -> Literal[":", ";"]:
    """
    Returns the classpath separator for the current os
    """
    if platform.system() == "Windows":
        return ";"
    else:
        return ":"


_requests_response_cache: dict[str, RequestsResponseCache] = {}


def get_requests_response_cache(url: str) -> requests.models.Response:
    """
    Caches the result of request.get(). If a request was made to the same URL within the last hour, the cache will be used, so you don't need to make a request to a URl each timje you call a function.
    """
    global _requests_response_cache
    if url not in _requests_response_cache or (datetime.datetime.now() - _requests_response_cache[url]["datetime"]).total_seconds() / 60 / 60 >= 1:
        r = requests.get(url, headers={"user-agent": get_user_agent()})
        if r.status_code == 200:
            _requests_response_cache[url] = {
                "response": r,
                "datetime": datetime.datetime.now()
            }
        return r
    else:
        return _requests_response_cache[url]["response"]


def parse_maven_metadata(url: str) -> MavenMetadata:
    """
    Parses a maven metadata file
    """
    r = get_requests_response_cache(url)
    # The structure of the metadata file is simple. So you don't need a XML parser. It can be parsed using RegEx.
    return {
        "release": re.search("(?<=<release>).*?(?=</release>)", r.text, re.MULTILINE).group(),  # type: ignore
        "latest": re.search("(?<=<latest>).*?(?=</latest>)", r.text, re.MULTILINE).group(),  # type: ignore
        "versions": re.findall("(?<=<version>).*?(?=</version>)", r.text, re.MULTILINE)
    }


def extract_file_from_zip(handler: zipfile.ZipFile, zip_path: str, extract_path: str, minecraft_directory: str | os.PathLike | None = None) -> None:
    """
    Extract a file from a zip handler into the given path
    """
    if minecraft_directory is not None:
        check_path_inside_minecraft_directory(minecraft_directory, extract_path)

    try:
        os.makedirs(os.path.dirname(extract_path))
    except Exception:
        pass

    with handler.open(zip_path, "r") as f:
        with open(extract_path, "wb") as w:
            w.write(f.read())


def assert_func(expression: bool) -> None:
    """
    The assert keyword is not available when running Python in Optimized Mode.
    This function is a drop-in replacement.
    See https://docs.python.org/3/using/cmdline.html?highlight=pythonoptimize#cmdoption-O
    """
    if not expression:
        raise AssertionError()


def get_client_json(version: str, minecraft_directory: str | os.PathLike) -> ClientJson:
    "Load the client.json for the given version"
    local_path = os.path.join(minecraft_directory, "versions", version, f"{version}.json")
    if os.path.isfile(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "inheritsFrom" in data:
            data = inherit_json(data, minecraft_directory)

        return data

    version_list = get_requests_response_cache("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json").json()
    for i in version_list["versions"]:
        if i["id"] == version:
            return get_requests_response_cache(i["url"]).json()

    raise VersionNotFound(version)
