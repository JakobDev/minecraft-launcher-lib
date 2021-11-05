from .helper import get_user_agent, download_file, empty
from typing import NoReturn, List, Dict, Callable, Union
from .exceptions import VersionNotFound
import subprocess
import requests
import platform
import os

_JVM_MANIFEST_URL = "https://launchermeta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json"


def _get_jvm_platform_string() -> str:
    """
    Get the name that is used the identify the platform
    """
    if platform.system() == "Windows":
        if platform.architecture()[0] == "32bit":
            return "windows-x86"
        else:
            return "windows-x64"
    elif platform.system() == "Linux":
        if platform.architecture()[0] == "32bit":
            return "linux-i386"
        else:
            return "linux"
    elif platform.system() == "Darwin":
        return "mac-os"


def get_jvm_runtimes() -> List[str]:
    """
    Returns a list of all jvm runtimes
    """
    manifest_data = requests.get(_JVM_MANIFEST_URL, headers={"user-agent": get_user_agent()}).json()
    jvm_list = []
    for key, value in manifest_data[_get_jvm_platform_string()].items():
        jvm_list.append(key)
    return jvm_list


def install_jvm_runtime(jvm_version: str, minecraft_directory: Union[str, os.PathLike], callback: Dict[str, Callable] = None) -> NoReturn:
    """
    Installs the given jvm runtime. callback is the same dict as in the install module.
    """
    if callback is None:
        callback = {}
    manifest_data = requests.get(_JVM_MANIFEST_URL, headers={"user-agent": get_user_agent()}).json()
    platform_string = _get_jvm_platform_string()
    # Check if the jvm version exists
    if jvm_version not in manifest_data[platform_string]:
        raise VersionNotFound(jvm_version)
    # Check if there is a platform manifest
    if len(manifest_data[platform_string][jvm_version]) == 0:
        return
    platform_manifest = requests.get(manifest_data[platform_string][jvm_version][0]["manifest"]["url"], headers={"user-agent": get_user_agent()}).json()
    base_path = os.path.join(minecraft_directory, "runtime", jvm_version, platform_string, jvm_version)
    # Download all files of the runtime
    callback.get("setMax", empty)(len(platform_manifest["files"]))
    count = 0
    for key, value in platform_manifest["files"].items():
        current_path = os.path.join(base_path, key)
        if value["type"] == "file":
            # Prefer downloading the compresses file
            if "lzma" in value["downloads"]:
                download_file(value["downloads"]["lzma"]["url"], current_path, sha1=value["downloads"]["raw"]["sha1"], callback=callback, lzma_compressed=True)
            else:
                download_file(value["downloads"]["raw"]["url"], current_path, sha1=value["downloads"]["raw"]["sha1"], callback=callback)
            # Make files executable on unix systems
            if value["executable"]:
                try:
                    subprocess.run(["chmod", "+x", current_path])
                except FileNotFoundError:
                    pass
        elif value["type"] == "directory":
            try:
                os.makedirs(current_path)
            except:
                pass
        callback.get("setProgress", empty)(count)
        count += 1
    # Create the .version file
    with open(os.path.join(minecraft_directory, "runtime", jvm_version, platform_string, ".version"), "w", encoding="utf-8") as f:
        f.write(manifest_data[platform_string][jvm_version][0]["version"]["name"])
