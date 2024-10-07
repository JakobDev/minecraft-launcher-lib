"""
This module contains all Types for minecraft-launcher-lib. It may help your IDE. You don't need to use this module directly in your code.
If you are not interested in static typing just ignore it.
For more information about TypedDict see `PEP 589 <https://peps.python.org/pep-0589/>`_.
"""
from typing import Literal, TypedDict, List, Callable, Optional
import datetime


class MinecraftOptions(TypedDict, total=False):
    username: str
    uuid: str
    token: str
    executablePath: str
    defaultExecutablePath: str
    jvmArguments: List[str]
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
    quickPlayPath: Optional[str]
    quickPlaySingleplayer: Optional[str]
    quickPlayMultiplayer: Optional[str]
    quickPlayRealms: Optional[str]


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
    javaw_path: Optional[str]
    is_64bit: bool
    openjdk: bool


# vanilla_launcher

class VanillaLauncherProfileResolution(TypedDict):
    height: int
    width: int


class VanillaLauncherProfile(TypedDict, total=False):
    name: str
    version: Optional[str]
    versionType: Literal["latest-release", "latest-snapshot", "custom"]
    gameDirectory: Optional[str]
    javaExecutable: Optional[str]
    javaArguments: Optional[List[str]]
    customResolution: Optional[VanillaLauncherProfileResolution]


# mrpack

class MrpackInformation(TypedDict):
    name: str
    summary: str
    versionId: str
    formatVersion: int
    minecraftVersion: str
    optionalFiles: List[str]


class MrpackInstallOptions(TypedDict, total=False):
    optionalFiles: List[str]
    skipDependenciesInstall: bool


# runtime

class JvmRuntimeInformation(TypedDict):
    name: str
    released: datetime.datetime


class VersionRuntimeInformation(TypedDict):
    name: str
    javaMajorVersion: int
