from typing import Dict, Literal, TypedDict


class VanillaLauncherProfilesJsonProfile(TypedDict, total=False):
    created: str
    gameDir: str
    icon: str
    javaArgs: str
    javaDir: str
    lastUsed: str
    lastVersionId: str
    name: str
    resolution: Dict[Literal["height", "width"], int]
    type: str


class VanillaLauncherProfilesJson(TypedDict):
    profiles: Dict[str, VanillaLauncherProfilesJsonProfile]
    version: int
