from typing import Literal, TypedDict


class _RuntimeListJsonEntryManifest(TypedDict):
    sha1: str
    size: int
    url: str


class _RuntimeListJsonEntry(TypedDict):
    availability: dict[Literal["group", "progress"], int]
    manifest: _RuntimeListJsonEntryManifest
    version: dict[Literal["name", "released"], str]


RuntimeListJson = dict[str, dict[str, list[_RuntimeListJsonEntry]]]


class _PlatformManifestJsonFileDownloads(TypedDict):
    sha1: str
    size: int
    url: str


class _PlatformManifestJsonFile(TypedDict, total=False):
    downloads: dict[Literal["lzma", "raw"], _PlatformManifestJsonFileDownloads]
    type: Literal["file", "directory", "link"]
    executable: bool
    target: str


class PlatformManifestJson(TypedDict):
    files: dict[str, _PlatformManifestJsonFile]
