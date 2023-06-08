from typing import List, Dict, Union, Literal, TypedDict


class ClientJsonRule(TypedDict):
    action: Literal["allow", "disallow"]
    os: Dict[Literal["name", "arch", "vesion"], str]
    features: Dict[Literal["has_custom_resolution", "is_demo_user", "has_quick_plays_support", "is_quick_play_singleplayer", "is_quick_play_multiplayer", "is_quick_play_realms"], bool]


class ClientJsonArgumentRule(TypedDict, total=False):
    compatibilityRules: List[ClientJsonRule]
    rules: List[ClientJsonRule]
    value: Union[str, List[str]]


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
    classifiers: Dict[Literal["javadoc", "natives-linux", "natives-macos", "natives-windows", "sources"], _ClientJsonLibraryDownloadsArtifact]


class ClientJsonLibrary(TypedDict, total=False):
    name: str
    downloads: _ClientJsonLibraryDownloads
    extract: Dict[Literal["exclude"], List[str]]
    rules: List[ClientJsonRule]
    natives: Dict[Literal["linux", "osx", "windows"], str]
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
    arguments: Dict[Literal["game", "jvm"], List[Union[str, ClientJsonArgumentRule]]]
    minecraftArguments: str
    assetIndex: _ClientJsonAssetIndex
    assets: str
    downloads: Dict[Literal["client", "client_mappings", "server", "server_mappings"], _ClientJsonDownloads]
    javaVersion: _ClientJsonJavaVersion
    libraries: List[ClientJsonLibrary]
    logging: Dict[Literal["client"], _ClientJsonLogging]
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
    latest: Dict[Literal["release", "snapshot"], str]
    versions: List[_VersionListManifestJsonVersion]
