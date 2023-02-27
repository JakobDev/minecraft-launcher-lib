from typing import List, Dict, Literal, TypedDict


class _RuntimeListJsonEntryManifest(TypedDict):
    sha1: str
    size: int
    url: str


class _RuntimeListJsonEntry(TypedDict):
    availability: Dict[Literal["group", "progress"], int]
    manifest: _RuntimeListJsonEntryManifest
    version: Dict[Literal["name", "released"], str]


RuntimeListJson = Dict[str, Dict[str, List[_RuntimeListJsonEntry]]]


class _PlatformManifestJsonFileDownloads(TypedDict):
    sha1: str
    size: int
    url: str


class _PlatformManifestJsonFile(TypedDict, total=False):
    downloads: Dict[Literal["lzma", "raw"], _PlatformManifestJsonFileDownloads]
    type: Literal["file", "directory", "link"]
    executable: bool
    target: str


class PlatformManifestJson(TypedDict):
    files: Dict[str, _PlatformManifestJsonFile]
