# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from .shared_types import ClientJson, ClientJsonLibrary
from typing import Literal, TypedDict


class _ForgeInstallProcessor(TypedDict, total=False):
    sides: list[Literal["client", "server"]]
    jar: str
    classpath: list[str]
    args: list[str]


class _ForgeInstallProfileInstall(TypedDict, total=False):
    profileName: str
    target: str
    path: str
    version: str
    filePath: str
    welcome: str
    minecraft: str
    mirrorList: str
    logo: str


class ForgeInstallProfile(TypedDict, total=False):
    spec: int
    profile: str
    version: str
    minecraft: str
    serverJarPath: str
    data: dict[str, dict[Literal["client", "server"], str]]
    processors: list[_ForgeInstallProcessor]
    libraries: list[ClientJsonLibrary]
    icon: str
    logo: str
    mirrorList: str
    welcome: str
    install: _ForgeInstallProfileInstall
    versionInfo: ClientJson
