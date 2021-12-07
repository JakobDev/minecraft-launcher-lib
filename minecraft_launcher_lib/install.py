from .helper import download_file, parse_rule_list, inherit_json, empty, get_user_agent
from typing import NoReturn, Any, Callable, Dict, Union
from .natives import extract_natives_file, get_natives
from .exceptions import VersionNotFound
from .runtime import install_jvm_runtime
import requests
import shutil
import json
import os

__all__ = ["install_minecraft_version"]


def install_libraries(data: Dict[str, Any], path: str, callback: Dict[str, Callable]) -> NoReturn:
    """
    Install all libraries
    """
    callback.get("setStatus", empty)("Download Libraries")
    callback.get("setMax", empty)(len(data["libraries"]))
    for count, i in enumerate(data["libraries"]):
        # Check, if the rules allow this lib for the current system
        if not parse_rule_list(i, "rules", {}):
            continue
        # Turn the name into a path
        currentPath = os.path.join(path, "libraries")
        if "url" in i:
            if i["url"].endswith("/"):
                downloadUrl = i["url"][:-1]
            else:
                downloadUrl = i["url"]
        else:
            downloadUrl = "https://libraries.minecraft.net"
        try:
            libPath, name, version = i["name"].split(":")
        except:
            continue
        for libPart in libPath.split("."):
            currentPath = os.path.join(currentPath, libPart)
            downloadUrl = downloadUrl + "/" + libPart
        try:
            version, fileend = version.split("@")
        except:
            fileend = "jar"
        jarFilename = name + "-" + version + "." + fileend
        downloadUrl = downloadUrl + "/" + name + "/" + version
        currentPath = os.path.join(currentPath, name, version)
        native = get_natives(i)
        # Check if there is a native file
        if native != "":
            jarFilenameNative = name + "-" + version + "-" + native + ".jar"
        jarFilename = name + "-" + version + "." + fileend
        downloadUrl = downloadUrl + "/" + jarFilename
        # Try to download the lib
        try:
            download_file(downloadUrl, os.path.join(currentPath, jarFilename), callback)
        except:
            pass
        if "downloads" not in i:
            if "extract" in i:
                extract_natives_file(os.path.join(currentPath, jarFilenameNative), os.path.join(path, "versions", data["id"], "natives"), i["extract"])
            continue
        if "artifact" in i["downloads"]:
            download_file(i["downloads"]["artifact"]["url"], os.path.join(currentPath, jarFilename), callback, sha1=i["downloads"]["artifact"]["sha1"])
        if native != "":
            download_file(i["downloads"]["classifiers"][native]["url"], os.path.join(currentPath, jarFilenameNative), callback, sha1=i["downloads"]["classifiers"][native]["sha1"])
            if "extract" in i:
                extract_natives_file(os.path.join(currentPath, jarFilenameNative), os.path.join(path, "versions", data["id"], "natives"), i["extract"])
        callback.get("setProgress", empty)(count)


def install_assets(data: Dict[str, Any], path: str, callback: Dict[str, Callable]) -> NoReturn:
    """
    Install all assets
    """
    # Old versions dosen't have this
    if "assetIndex" not in data:
        return
    callback.get("setStatus", empty)("Download Assets")
    # Download all assets
    download_file(data["assetIndex"]["url"], os.path.join(path, "assets", "indexes", data["assets"] + ".json"), callback, sha1=data["assetIndex"]["sha1"])
    with open(os.path.join(path, "assets", "indexes", data["assets"] + ".json")) as f:
        assets_data = json.load(f)
    # The assets has a hash. e.g. c4dbabc820f04ba685694c63359429b22e3a62b5
    # With this hash, it can be download from https://resources.download.minecraft.net/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    # And saved at assets/objects/c4/c4dbabc820f04ba685694c63359429b22e3a62b5
    callback.get("setMax", empty)(len(assets_data["objects"]))
    count = 0
    for key, value in assets_data["objects"].items():
        download_file("https://resources.download.minecraft.net/" + value["hash"][:2] + "/" + value["hash"], os.path.join(path, "assets", "objects", value["hash"][:2], value["hash"]), callback, sha1=value["hash"])
        count += 1
        callback.get("setProgress", empty)(count)


def do_version_install(versionid: str, path: str, callback: Dict[str, Callable], url: str = None) -> NoReturn:
    """
    Install the given version
    """
    # Download and read versions.json
    if url:
        download_file(url, os.path.join(path, "versions", versionid, versionid + ".json"), callback)
    with open(os.path.join(path, "versions", versionid, versionid + ".json")) as f:
        versiondata = json.load(f)
    # For Forge
    if "inheritsFrom" in versiondata:
        versiondata = inherit_json(versiondata, path)
    install_libraries(versiondata, path, callback)
    install_assets(versiondata, path, callback)
    # Download logging config
    if "logging" in versiondata:
        if len(versiondata["logging"]) != 0:
            logger_file = os.path.join(path, "assets", "log_configs", versiondata["logging"]["client"]["file"]["id"])
            download_file(versiondata["logging"]["client"]["file"]["url"], logger_file, callback, sha1=versiondata["logging"]["client"]["file"]["sha1"])
    # Download minecraft.jar
    if "downloads" in versiondata:
        download_file(versiondata["downloads"]["client"]["url"], os.path.join(path, "versions", versiondata["id"], versiondata["id"] + ".jar"), callback, sha1=versiondata["downloads"]["client"]["sha1"])
    # Need to copy jar for old forge versions
    if not os.path.isfile(os.path.join(path, "versions", versiondata["id"], versiondata["id"] + ".jar")) and "inheritsFrom" in versiondata:
        inheritsFrom = versiondata["inheritsFrom"]
        shutil.copyfile(os.path.join(path, "versions", versiondata["id"], versiondata["id"] + ".jar"), os.path.join(path, "versions", inheritsFrom, inheritsFrom + ".jar"))
    # Install java runtime if needed
    if "javaVersion" in versiondata:
        callback.get("setStatus", empty)("Install java runtime")
        install_jvm_runtime(versiondata["javaVersion"]["component"], path, callback=callback)
    callback.get("setStatus", empty)("Installation complete")


def install_minecraft_version(versionid: str, minecraft_directory: Union[str, os.PathLike], callback: Dict[str, Callable] = None) -> NoReturn:
    """
    Install a Minecraft Version. Fore more Information take a look at the documentation"
    """
    if isinstance(minecraft_directory, os.PathLike):
        minecraft_directory = str(minecraft_directory)
    if callback is None:
        callback = {}
    if os.path.isfile(os.path.join(minecraft_directory, "versions", versionid, f"{versionid}.json")):
        do_version_install(versionid, minecraft_directory, callback)
        return
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", headers={"user-agent": get_user_agent()}).json()
    for i in version_list["versions"]:
        if i["id"] == versionid:
            do_version_install(versionid, minecraft_directory, callback, url=i["url"])
            return
    raise VersionNotFound(versionid)
