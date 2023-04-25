from .shared_types import ClientJson, ClientJsonLibrary
from typing import List, Dict, Literal, TypedDict


class _ForgeInstallProcessor(TypedDict, total=False):
    sides: List[Literal["client", "server"]]
    jar: str
    classpath: List[str]
    args: List[str]


class _ForgeInstallProfileInstall(TypedDict, total=False):
    profileName: str
    target: str
    path: str
    version: str
    filePath: str
    welcome: str
    minecraft: str
    mirrorList: str
    logo: str


class ForgeInstallProfile(TypedDict, total=False):
    spec: int
    profile: str
    version: str
    minecraft: str
    serverJarPath: str
    data: Dict[str, Dict[Literal["client", "server"], str]]
    processors: List[_ForgeInstallProcessor]
    libraries: List[ClientJsonLibrary]
    icon: str
    logo: str
    mirrorList: str
    welcome: str
    install: _ForgeInstallProfileInstall
    versionInfo: ClientJson
