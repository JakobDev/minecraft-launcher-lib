from typing import Dict, TypedDict


class _AssetsJsonObject(TypedDict):
    hash: str
    size: int


class AssetsJson(TypedDict):
    objects: Dict[str, _AssetsJsonObject]
