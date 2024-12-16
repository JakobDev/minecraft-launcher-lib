from typing import Literal, TypedDict


class VanillaLauncherProfilesJsonProfile(TypedDict, total=False):
    created: str
    gameDir: str
    icon: str
    javaArgs: str
    javaDir: str
    lastUsed: str
    lastVersionId: str
    name: str
    resolution: dict[Literal["height", "width"], int]
    type: str


class VanillaLauncherProfilesJson(TypedDict):
    profiles: dict[str, VanillaLauncherProfilesJsonProfile]
    version: int
