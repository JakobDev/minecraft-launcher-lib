from typing import TypedDict, List, Callable
import datetime


class MinecraftOptions(TypedDict, total=False):
    username: str
    uuid: str
    token: str
    executablePath: str
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


class CallbackDict(TypedDict, total=False):
    setStatus: Callable[[str], None]
    setProgress: Callable[[int], None]
    setMax: Callable[[int], None]


class MinecraftVersionInfo(TypedDict):
    id: str
    type: str
    releaseTime: datetime.datetime


class FabricMinecraftVersion(TypedDict):
    version: str
    stable: bool


class FabricLoader(TypedDict):
    separator: str
    build: int
    maven: str
    version: str
    stable: bool
