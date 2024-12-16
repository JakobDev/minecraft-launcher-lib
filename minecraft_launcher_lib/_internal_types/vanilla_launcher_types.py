# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
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
