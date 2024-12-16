# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from typing import TypedDict
import requests
import datetime


class RequestsResponseCache(TypedDict):
    response: requests.models.Response
    datetime: datetime.datetime


class MavenMetadata(TypedDict):
    release: str
    latest: str
    versions: list[str]
