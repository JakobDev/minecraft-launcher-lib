# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"java_utils contains some functions to help with Java"
from .types import JavaInformation
import subprocess
import platform
import re
import os


def get_java_information(path: str | os.PathLike) -> JavaInformation:
    """
    Returns Some Information about the given Java Installation

    .. note::
        This Function executes the Java executable to determine details such as the version. This might be a security risk.

    Example:

    .. code:: python

        java_path = "<path>"
        information = minecraft_launcher_lib.java_utils.get_java_information(java_path)
        print("Name: " + information["name"])
        print("Version: " + information["version"])
        print("Java path: " + information["java_path"])

    :param path: The Path to the Installation. It must be the Directory. If your Java executable is e.g. /usr/lib/jvm/java-19-openjdk-amd64/bin/java this Parameter must be /usr/lib/jvm/java-19-openjdk-amd64.
    :return: A dict with Information about the given java installation
    :raises ValueError: Wrong path
    """
    if platform.system() == "Windows":
        if not os.path.isfile(os.path.join(path, "bin", "java.exe")):
            raise ValueError(os.path.abspath(os.path.join(path, "bin", "java.exe")) + " was not found")
    else:
        if not os.path.isfile(os.path.join(path, "bin", "java")):
            raise ValueError(os.path.abspath(os.path.join(path, "bin", "java")) + " was not found")

    lines = subprocess.run([os.path.join(path, "bin", "java"), "-showversion"], capture_output=True, text=True).stderr.splitlines()
    information: JavaInformation = {}  # type: ignore
    information["path"] = str(path)
    information["name"] = os.path.basename(path)
    information["version"] = re.search(r'(?<=version ")[\d|\.|_]+(?=")', lines[0]).group()  # type: ignore
    information["is_64bit"] = "64-Bit" in lines[2]
    information["openjdk"] = lines[0].startswith("openjdk")

    if platform.system() == "Windows":
        information["java_path"] = os.path.join(os.path.abspath(path), "bin", "java.exe")
        information["javaw_path"] = os.path.join(os.path.abspath(path), "bin", "javaw.exe")
    else:
        information["java_path"] = os.path.join(os.path.abspath(path), "bin", "java")
        information["javaw_path"] = None

    return information


def _search_java_directory(path: str | os.PathLike) -> list[str]:
    "Used by find_system_java_versions() to parse a Directory"
    if not os.path.isdir(path):
        return []

    java_list: list[str] = []
    for i in os.listdir(path):
        current_entry = os.path.join(path, i)

        if os.path.isfile(current_entry) or os.path.islink(current_entry):
            continue

        if os.path.isfile(os.path.join(current_entry, "bin", "java")) or os.path.isfile(os.path.join(current_entry, "bin", "java.exe")):
            java_list.append(current_entry)

    return java_list


def find_system_java_versions(additional_directories: list[str | os.PathLike] | None = None) -> list[str]:
    """
    Try to find all Java Versions installed on the System. You can use this to e.g. let the User choose between different Java Versions in a Dropdown.
    macOS is not supported yet.

    Example:

    .. code:: python

        for version in minecraft_launcher_lib.java_utils.find_system_java_versions():
            print(version)

    :param additional_directories: A List of additional Directories to search for Java in custom locations
    :return: A List with all Directories of Java Installations
    """
    java_list: list[str] = []

    match platform.system():
        case "Windows":
            java_list += _search_java_directory(r"C:\Program Files (x86)\Java")
            java_list += _search_java_directory(r"C:\Program Files\Java")
        case "Linux":
            java_list += _search_java_directory("/usr/lib/jvm")
            java_list += _search_java_directory("/usr/lib/sdk")

    if additional_directories is not None:
        for i in additional_directories:
            java_list += _search_java_directory(i)

    return java_list


def find_system_java_versions_information(additional_directories: list[str | os.PathLike] | None = None) -> list[JavaInformation]:
    """
    Same as :func:`find_system_java_version`, but uses :func:`get_java_information` to get some Information about the Installation instead of just proving a Path.
    macOS is not supported yet

    .. note::
        This Function executes the Java executable to determine details such as the version. This might be a security risk.

    Example:

    .. code:: python

        for version_information in minecraft_launcher_lib.java_utils.find_system_java_versions_information():
            print("Path: " + version_information["path"])
            print("Name: " + version_information["name"])
            print("Version: " + version_information["version"])
            print("Java path: " + version_information["java_path"])
            print()

    :param additional_directories: A List of additional Directories to search for Java in custom locations
    :return: A List with Information of Java Installations
    """
    java_information_list: list[JavaInformation] = []
    for i in find_system_java_versions(additional_directories=additional_directories):
        java_information_list.append(get_java_information(i))
    return java_information_list
