"mrpack allows you to install Modpacks from the `Mrpack Format <https://docs.modrinth.com/docs/modpacks/format_definition>`_"
from ._helper import download_file, empty, check_path_inside_minecraft_directory
from .types import MrpackInformation, MrpackInstallOptions, CallbackDict
from ._internal_types.mrpack_types import MrpackIndex, MrpackFile
from .install import install_minecraft_version
from typing import List, Union, Optional
from .forge import install_forge_version
from .fabric import install_fabric
from .quilt import install_quilt
import zipfile
import json
import os


def _filter_mrpack_files(file_list: List[MrpackFile], mrpack_install_options: MrpackInstallOptions) -> List[MrpackFile]:
    """
    Gets all Mrpack Files that should be installed
    """
    filtered_list: List[MrpackFile] = []
    for file in file_list:
        if "env" not in file:
            filtered_list.append(file)
            continue

        if file["env"]["client"] == "required":
            filtered_list.append(file)
        if file["env"]["client"] == "optional" and file["path"] in mrpack_install_options.get("optionalFiles", []):
            filtered_list.append(file)

    return filtered_list


def get_mrpack_information(path: Union[str, os.PathLike]) -> MrpackInformation:
    """
    Gets some Information from a .mrpack file

    :param path: The Path the the .mrpack file
    :type path: Union[str, os.PathLike]
    :return: The Information about the given Mrpack
    """
    with zipfile.ZipFile(path, "r") as zf:
        with zf.open("modrinth.index.json", "r") as f:
            index: MrpackIndex = json.load(f)

            information: MrpackInformation = {}  # type: ignore
            information["name"] = index["name"]
            information["summary"] = index.get("summary", "")
            information["versionId"] = index["versionId"]
            information["formatVersion"] = index["formatVersion"]
            information["minecraftVersion"] = index["dependencies"]["minecraft"]

            information["optionalFiles"] = []
            for file in index["files"]:
                if "env" not in file:
                    continue

                if file["env"]["client"] == "optional":
                    information["optionalFiles"].append(file["path"])

            return information


def install_mrpack(path: Union[str, os.PathLike], minecraft_directory: Union[str, os.PathLike], modpack_directory: Optional[Union[str, os.PathLike]] = None, callback: Optional[CallbackDict] = None, mrpack_install_options: Optional[MrpackInstallOptions] = None) -> None:
    """
    Installs a .mrpack file

    :param path: The Path the the .mrpack file
    :param minecraft_directory: he path to your Minecraft directory
    :param modpack_directory: If you want to install the Pack in another Directory than your Minecraft directory, set it here.
    :param callback: The same dict as for :func:`~minecraft_launcher_lib.install.install_minecraft_version`
    :param mrpack_install_options: Some Options to install the Pack (see below)
    :raises FileOutsideMinecraftDirectory: A File should be placed outside the given Minecraft directory

    ``mrpack_install_options`` is a dict. All Options are Optional.

    .. code:: python

        mrpack_install_options = {
            "optionalFiles": [], # List with all Optional files
            "skipDependenciesInstall": False # If you want to skip the Dependencie install. Only used for testing purposes.
        }
    """
    minecraft_directory = os.path.abspath(minecraft_directory)
    path = os.path.abspath(path)

    if modpack_directory is None:
        modpack_directory = minecraft_directory
    else:
        modpack_directory = os.path.abspath(modpack_directory)

    if callback is None:
        callback = {}

    if mrpack_install_options is None:
        mrpack_install_options = {}

    with zipfile.ZipFile(path, "r") as zf:
        with zf.open("modrinth.index.json", "r") as f:
            index: MrpackIndex = json.load(f)

        # Download the files
        for file in _filter_mrpack_files(index["files"], mrpack_install_options):
            full_path = os.path.abspath(os.path.join(modpack_directory, file["path"]))

            check_path_inside_minecraft_directory(modpack_directory, full_path)

            download_file(file["downloads"][0], full_path, sha1=file["hashes"]["sha1"], callback=callback)

        # Extract the overrides
        for zip_name in zf.namelist():
            # Check if the entry is in the overrides and if it is a file
            if (not zip_name.startswith("overrides/") and not zip_name.startswith("client-overrides/")) or zf.getinfo(zip_name).file_size == 0:
                continue

            # Remove the overrides at the start of the Name
            # We don't have removeprefix() in Python 3.8
            if zip_name.startswith("client-overrides/"):
                file_name = zip_name[len("client-overrides/"):]
            else:
                file_name = zip_name[len("overrides/"):]

            # Constructs the full Path
            full_path = os.path.abspath(os.path.join(modpack_directory, file_name))

            check_path_inside_minecraft_directory(modpack_directory, full_path)

            zf.extract(zip_name, full_path)

        if mrpack_install_options.get("skipDependenciesInstall"):
            return

        # Install dependencies
        callback.get("setStatus", empty)("Installing Minecraft " + index["dependencies"]["minecraft"])
        install_minecraft_version(index["dependencies"]["minecraft"], minecraft_directory, callback=callback)

        if "forge" in index["dependencies"]:
            forge_version = index["dependencies"]["minecraft"] + "-" + index["dependencies"]["forge"]
            callback.get("setStatus", empty)(f"Installing Forge {forge_version}")
            install_forge_version(forge_version, minecraft_directory, callback=callback)

        if "fabric-loader" in index["dependencies"]:
            callback.get("setStatus", empty)("Installing Fabric " + index["dependencies"]["fabric-loader"] + " for Minecraft " + index["dependencies"]["minecraft"])
            install_fabric(index["dependencies"]["minecraft"], minecraft_directory, loader_version=index["dependencies"]["fabric-loader"], callback=callback)

        if "quilt-loader" in index["dependencies"]:
            callback.get("setStatus", empty)("Installing Quilt " + index["dependencies"]["quilt-loader"] + " for Minecraft " + index["dependencies"]["minecraft"])
            install_quilt(index["dependencies"]["minecraft"], minecraft_directory, loader_version=index["dependencies"]["quilt-loader"], callback=callback)


def get_mrpack_launch_version(path: Union[str, os.PathLike]) -> str:
    """
    Returns that Version that needs to be used with :func:`~minecraft_launcher_lib.command.get_minecraft_command`.

    :param path: The Path the the .mrpack file
    :return: The version
    """
    with zipfile.ZipFile(path, "r") as zf:
        with zf.open("modrinth.index.json", "r") as f:
            index: MrpackIndex = json.load(f)

            if "forge" in index["dependencies"]:
                return index["dependencies"]["minecraft"] + "-forge-" + index["dependencies"]["forge"]
            elif "fabric-loader" in index["dependencies"]:
                return "fabric-loader-" + index["dependencies"]["fabric-loader"] + "-" + index["dependencies"]["minecraft"]
            elif "quilt-loader" in index["dependencies"]:
                return "quilt-loader-" + index["dependencies"]["quilt-loader"] + "-" + index["dependencies"]["minecraft"]
            else:
                return index["dependencies"]["minecraft"]
