from typing import TypedDict


class _AssetsJsonObject(TypedDict):
    hash: str
    size: int


class AssetsJson(TypedDict):
    objects: dict[str, _AssetsJsonObject]
