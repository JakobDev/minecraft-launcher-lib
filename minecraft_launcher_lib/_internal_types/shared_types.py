# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from typing import Union, Literal, TypedDict


class ClientJsonRule(TypedDict):
    action: Literal["allow", "disallow"]
    os: dict[Literal["name", "arch", "vesion"], str]
    features: dict[Literal["has_custom_resolution", "is_demo_user", "has_quick_plays_support", "is_quick_play_singleplayer", "is_quick_play_multiplayer", "is_quick_play_realms"], bool]


class ClientJsonArgumentRule(TypedDict, total=False):
    compatibilityRules: list[ClientJsonRule]
    rules: list[ClientJsonRule]
    value: Union[str, list[str]]


class _ClientJsonAssetIndex(TypedDict):
    id: str
    sha1: str
    size: int
    totalSize: int
    url: str


class _ClientJsonDownloads(TypedDict):
    sha1: str
    size: int
    url: str


class _ClientJsonJavaVersion(TypedDict):
    component: str
    majorVersion: int


class _ClientJsonLibraryDownloadsArtifact(TypedDict):
    path: str
    url: str
    sha1: str
    size: int


class _ClientJsonLibraryDownloads(TypedDict, total=False):
    artifact: _ClientJsonLibraryDownloadsArtifact
    classifiers: dict[Literal["javadoc", "natives-linux", "natives-macos", "natives-windows", "sources"], _ClientJsonLibraryDownloadsArtifact]


class ClientJsonLibrary(TypedDict, total=False):
    name: str
    downloads: _ClientJsonLibraryDownloads
    extract: dict[Literal["exclude"], list[str]]
    rules: list[ClientJsonRule]
    natives: dict[Literal["linux", "osx", "windows"], str]
    url: str


class _ClientJsonLoggingFile(TypedDict):
    id: str
    sha1: str
    size: int
    url: str


class _ClientJsonLogging(TypedDict):
    argument: str
    file: _ClientJsonLoggingFile
    type: str


class ClientJson(TypedDict, total=False):
    id: str
    jar: str
    arguments: dict[Literal["game", "jvm"], list[Union[str, ClientJsonArgumentRule]]]
    minecraftArguments: str
    assetIndex: _ClientJsonAssetIndex
    assets: str
    downloads: dict[Literal["client", "client_mappings", "server", "server_mappings"], _ClientJsonDownloads]
    javaVersion: _ClientJsonJavaVersion
    libraries: list[ClientJsonLibrary]
    logging: dict[Literal["client"], _ClientJsonLogging]
    mainClass: str
    minimumLauncherVersion: int
    releaseTime: str
    time: str
    type: str
    complianceLevel: int
    inheritsFrom: str


class _VersionListManifestJsonVersion(TypedDict):
    id: str
    type: str
    url: str
    time: str
    releaseTime: str
    sha1: str
    complianceLevel: int


class VersionListManifestJson(TypedDict):
    latest: dict[Literal["release", "snapshot"], str]
    versions: list[_VersionListManifestJsonVersion]
