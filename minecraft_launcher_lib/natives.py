from typing import NoReturn, Dict, Any, Union
from .exceptions import VersionNotFound
from .helper import parse_rule_list
import platform
import zipfile
import json
import os


def get_natives(data: Dict[str, Any]) -> str:
    """
    Returns the native part from the json data
    """
    if platform.architecture()[0] == "32bit":
        arch_type = "32"
    else:
        arch_type = "64"
    if "natives" in data:
        if platform.system() == 'Windows':
            if "windows" in data["natives"]:
                return data["natives"]["windows"].replace("${arch}", arch_type)
            else:
                return ""
        elif platform.system() == 'Darwin':
            if "osx" in data["natives"]:
                return data["natives"]["osx"].replace("${arch}", arch_type)
            else:
                return ""
        else:
            if "linux" in data["natives"]:
                return data["natives"]["linux"].replace("${arch}", arch_type)
            else:
                return ""
    else:
        return ""


def extract_natives_file(filename: str, extract_path: str, extract_data: Dict[str, Any]) -> NoReturn:
    """
    Unpack natives
    """
    try:
        os.mkdir(extract_path)
    except:
        pass
    zf = zipfile.ZipFile(filename, "r")
    for i in zf.namelist():
        for e in extract_data["exclude"]:
            if i.startswith(e):
                continue
        zf.extract(i, extract_path)


def extract_natives(versionid: str, path: Union[str, os.PathLike], extract_path: str) -> NoReturn:
    """
    Extract natives into the givrn path. For more information look at the documentation.
    """
    if not os.path.isfile(os.path.join(path, "versions", versionid, versionid + ".json")):
        raise VersionNotFound(versionid)
    with open(os.path.join(path, "versions", versionid, versionid + ".json")) as f:
        data = json.load(f)
    for count, i in enumerate(data["libraries"]):
        # Check, if the rules allow this lib for the current system
        if not parse_rule_list(i, "rules", {}):
            continue
        current_path = os.path.join(path, "libraries")
        lib_path, name, version = i["name"].split(":")
        for lib_part in lib_path.split("."):
            current_path = os.path.join(current_path, lib_part)
        current_path = os.path.join(current_path, name, version)
        native = get_natives(i)
        if native == "":
            continue
        jar_filename_native = name + "-" + version + "-" + native + ".jar"
        if "extract" in i:
            extract_natives_file(os.path.join(current_path, jar_filename_native), extract_path, i["extract"])
