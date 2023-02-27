from typing import List, Dict, Literal, TypedDict
from .shared_types import ClientJsonLibrary


class _ForgeInstallProcessor(TypedDict, total=False):
    sides: List[Literal["client", "server"]]
    jar: str
    classpath: List[str]
    args: List[str]


class ForgeInstallProfile(TypedDict):
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
