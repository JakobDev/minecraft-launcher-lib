# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from typing import TypedDict, Literal


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
    downloads: list[str]
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
    files: list[MrpackFile]
    dependencies: MrpackDependencies
