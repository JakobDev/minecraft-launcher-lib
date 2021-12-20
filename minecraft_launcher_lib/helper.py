from typing import NoReturn, Dict, Any, Callable
from .utils import get_library_version
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


def empty(arg: Any) -> NoReturn:
    """
    This function is just a placeholder
    """
    pass


def download_file(url: str, path: str, callback: Dict[str, Callable] = {}, sha1: str = None, lzma_compressed: bool = False) -> bool:
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
    except:
        pass
    if not url.startswith("http"):
        return False
    callback.get("setStatus", empty)("Download " + os.path.basename(path))
    r = requests.get(url, stream=True, headers={"user-agent": get_user_agent()})
    if r.status_code != 200:
        return False
    with open(path, 'wb') as f:
        r.raw.decode_content = True
        if lzma_compressed:
            f.write(lzma.decompress(r.content))
        else:
            shutil.copyfileobj(r.raw, f)
    return True


def parse_single_rule(rule: Dict[str, Any], options: Dict[str, Any]) -> bool:
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


def parse_rule_list(data: Dict[str, Any], rule_string: str, options: Dict[str, Any]) -> bool:
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
    base_path, libname, version = name.split(":")
    for i in base_path.split("."):
        libpath = os.path.join(libpath, i)
    try:
        version, fileend = version.split("@")
    except:
        fileend = "jar"
    libpath = os.path.join(libpath, libname, version, libname + "-" + version + "." + fileend)
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
        except:
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


def get_user_agent() -> str:
    """
    Returns the user agent of minecraft-launcher-lib
    """
    return f"minecraft-launcher-lib/{get_library_version()}"


def get_classpath_separator() -> str:
    """
    Returns the classpath seperator for the current os
    """
    if platform.system() == "Windows":
        return ";"
    else:
        return ":"
