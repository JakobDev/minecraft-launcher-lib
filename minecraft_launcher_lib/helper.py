from typing import List, Dict, Union, Optional, Any
from .types import MinecraftOptions, CallbackDict
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


def download_file(url: str, path: str, callback: CallbackDict = {}, sha1: Optional[str] = None, lzma_compressed: Optional[bool] = False, session: Optional[requests.sessions.Session] = None) -> bool:
    """
    Downloads a file into the given path. Check sha1 if given.
    """
    if os.path.isfile(path):
        if sha1 is None:
            return False
        elif get_sha1_hash(path) == sha1:
            return False
    try:
        os.makedirs(os.path.dirname(path))
    except Exception:
        pass
    if not url.startswith("http"):
        return False
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
    return True


def parse_single_rule(rule: Dict[str, Any], options: MinecraftOptions) -> bool:
    """
    Parse a single rule from the versions.json
    """
    if rule["action"] == "allow":
        returnvalue = False
    elif rule["action"] == "disallow":
        returnvalue = True
    if "os" in rule:
        for key, value in rule["os"].items():
            if key == "name":
                if value == "windows" and platform.system() != 'Windows':
                    return returnvalue
                elif value == "osx" and platform.system() != 'Darwin':
                    return returnvalue
                elif value == "linux" and platform.system() != 'Linux':
                    return returnvalue
            elif key == "arch":
                if value == "x86" and platform.architecture()[0] != "32bit":
                    return returnvalue
            elif key == "version":
                if not re.match(value, get_os_version()):
                    return returnvalue
    if "features" in rule:
        for key, value in rule["features"].items():
            if key == "has_custom_resolution" and not options.get("customResolution", False):
                return returnvalue
            elif key == "is_demo_user" and not options.get("demo", False):
                return returnvalue
    return not returnvalue


def parse_rule_list(data: Dict[str, Any], rule_string: str, options: MinecraftOptions) -> bool:
    """
    Parse a list of rules
    """
    if rule_string not in data:
        return True
    for i in data[rule_string]:
        if not parse_single_rule(i, options):
            return False
    return True


def inherit_json(original_data: Dict[str, Any], path: str) -> Dict[str, Any]:
    """
    Implement the inheritsFrom function
    See https://github.com/tomsik68/mclauncher-api/wiki/Version-Inheritance-&-Forge
    """
    inherit_version = original_data["inheritsFrom"]
    with open(os.path.join(path, "versions", inherit_version, inherit_version + ".json")) as f:
        new_data = json.load(f)
    for key, value in original_data.items():
        if isinstance(value, list) and isinstance(new_data.get(key, None), list):
            new_data[key] = value + new_data[key]
        elif isinstance(value, dict) and isinstance(new_data.get(key, None), dict):
            for a, b in value.items():
                if isinstance(b, list):
                    new_data[key][a] = new_data[key][a] + b
        else:
            new_data[key] = value
    return new_data


def get_library_path(name: str, path: str) -> str:
    """
    Returns the path from a libname
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
        ver = sys.getwindowsversion()
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


def get_classpath_separator() -> str:
    """
    Returns the classpath seperator for the current os
    """
    if platform.system() == "Windows":
        return ";"
    else:
        return ":"


_requests_response_cache = {}


def get_requests_response_cache(url: str) -> requests.models.Response:
    """
    Caches the result of request.get(). If a request was made to the same URL within the last hour, the cache will be used, so you don't need to make a request to a URl each timje you call a function.
    """
    global _requests_response_cache
    if url not in _requests_response_cache or (datetime.datetime.now() - _requests_response_cache[url]["datetime"]).total_seconds() / 60 / 60 >= 1:
        r = requests.get(url, headers={"user-agent": get_user_agent()})
        if r.status_code == 200:
            _requests_response_cache[url] = {}
            _requests_response_cache[url]["response"] = r
            _requests_response_cache[url]["datetime"] = datetime.datetime.now()
        return r
    else:
        return _requests_response_cache[url]["response"]


def parse_maven_metadata(url: str) -> Dict[str, Union[str, List[str]]]:
    """
    Parses a maven metadata file
    """
    r = get_requests_response_cache(url)
    data = {}
    # The structure of the metadata file is simple. So you don't need a XML parser. It can be parsed using RegEx.
    data["release"] = re.search("(?<=<release>).*?(?=</release>)", r.text, re.MULTILINE).group()
    data["latest"] = re.search("(?<=<latest>).*?(?=</latest>)", r.text, re.MULTILINE).group()
    data["versions"] = re.findall("(?<=<version>).*?(?=</version>)", r.text, re.MULTILINE)
    return data
