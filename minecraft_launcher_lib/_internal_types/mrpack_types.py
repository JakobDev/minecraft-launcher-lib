from typing import List, TypedDict, Literal


class MrpackFileHashes(TypedDict):
    sha1: str
    sha256: str


class MrpackFileEnv(TypedDict):
    client: Literal["required", "optional", "unsupported"]
    server: Literal["required", "optional", "unsupported"]


class MrpackFile(TypedDict, total=False):
    path: str
    hashes: MrpackFileHashes
    env: MrpackFileEnv
    downloads: List[str]
    fileSize: int


MrpackDependencies = TypedDict("MrpackDependencies", {
    "minecraft": str,
    "forge": str,
    "fabric-loader": str,
    "quilt-loader": str
}, total=False)


class MrpackIndex(TypedDict, total=False):
    formatVersion: int
    game: str
    versionId: str
    name: str
    summary: str
    files: List[MrpackFile]
    dependencies: MrpackDependencies
