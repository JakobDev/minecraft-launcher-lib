# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"""
This module contains all Types for minecraft-launcher-lib. It may help your IDE. You don't need to use this module directly in your code.
If you are not interested in static typing just ignore it.
For more information about TypedDict see `PEP 589 <https://peps.python.org/pep-0589/>`_.
"""
from typing import Literal, TypedDict, Callable
import datetime


class MinecraftOptions(TypedDict, total=False):
    username: str
    uuid: str
    token: str
    executablePath: str
    defaultExecutablePath: str
    jvmArguments: list[str]
    launcherName: str
    launcherVersion: str
    gameDirectory: str
    demo: bool
    customResolution: bool
    resolutionWidth: str
    resolutionHeight: str
    server: str
    port: str
    nativesDirectory: str
    enableLoggingConfig: bool
    disableMultiplayer: bool
    disableChat: bool
    quickPlayPath: str | None
    quickPlaySingleplayer: str | None
    quickPlayMultiplayer: str | None
    quickPlayRealms: str | None


class CallbackDict(TypedDict, total=False):
    setStatus: Callable[[str], None]
    setProgress: Callable[[int], None]
    setMax: Callable[[int], None]


class LatestMinecraftVersions(TypedDict):
    release: str
    snapshot: str


class MinecraftVersionInfo(TypedDict):
    id: str
    type: str
    releaseTime: datetime.datetime
    complianceLevel: int


# fabric

class FabricMinecraftVersion(TypedDict):
    version: str
    stable: bool


class FabricLoader(TypedDict):
    separator: str
    build: int
    maven: str
    version: str
    stable: bool


# quilt

class QuiltMinecraftVersion(TypedDict):
    version: str
    stable: bool


class QuiltLoader(TypedDict):
    separator: str
    build: int
    maven: str
    version: str


# java_utils

class JavaInformation(TypedDict):
    path: str
    name: str
    version: str
    java_path: str
    javaw_path: str | None
    is_64bit: bool
    openjdk: bool


# vanilla_launcher

class VanillaLauncherProfileResolution(TypedDict):
    height: int
    width: int


class VanillaLauncherProfile(TypedDict, total=False):
    name: str
    version: str | None
    versionType: Literal["latest-release", "latest-snapshot", "custom"]
    gameDirectory: str | None
    javaExecutable: str | None
    javaArguments: list[str] | None
    customResolution: VanillaLauncherProfileResolution | None


# mrpack

class MrpackInformation(TypedDict):
    name: str
    summary: str
    versionId: str
    formatVersion: int
    minecraftVersion: str
    optionalFiles: list[str]


class MrpackInstallOptions(TypedDict, total=False):
    optionalFiles: list[str]
    skipDependenciesInstall: bool


# runtime

class JvmRuntimeInformation(TypedDict):
    name: str
    released: datetime.datetime


class VersionRuntimeInformation(TypedDict):
    name: str
    javaMajorVersion: int


class _NewsEntryPlayPageImage(TypedDict):
    title: str
    url: str


class _NewsEntryNewsPageImageDimensions(TypedDict):
    width: int
    height: int


class _NewsEntryNewsPageImage(TypedDict):
    title: str
    url: str
    dimensions: _NewsEntryNewsPageImageDimensions


class _NewsEntry(TypedDict):
    title: str
    category: str
    date: str
    text: str
    playPageImage: _NewsEntryPlayPageImage
    newsPageImage: _NewsEntryNewsPageImage
    readMoreLink: str
    newsType: list[str]
    id: str


class MinecraftNews(TypedDict):
    version: Literal[1]
    entries: list[_NewsEntry]


class _JavaPatchNoteEntryImage(TypedDict):
    url: str
    title: str


class _JavaPatchNoteEntry(TypedDict):
    title: str
    type: Literal["release", "snapshot"]
    version: str
    image: _JavaPatchNoteEntryImage
    body: str
    contentPath: str


class JavaPatchNotes(TypedDict):
    version: Literal[1]
    entries: list[_JavaPatchNoteEntry]
