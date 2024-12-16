# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from typing import TypedDict


class _AssetsJsonObject(TypedDict):
    hash: str
    size: int


class AssetsJson(TypedDict):
    objects: dict[str, _AssetsJsonObject]
