# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
"""
news includes functions to retrieve news about Minecraft using the official API from Mojang

.. warning::
    The format of the data returned by this API may change at any time
"""
from .types import MinecraftNews, JavaPatchNotes
from ._helper import get_user_agent
import datetime
import requests


def get_minecraft_news() -> MinecraftNews:
    "Returns general news about Minecraft"
    news = requests.get("https://launchercontent.mojang.com/news.json", headers={"user-agent": get_user_agent()}).json()

    for entry in news["entries"]:
        entry["date"] = datetime.date.fromisoformat(entry["date"])

    return news


def get_java_patch_notes() -> JavaPatchNotes:
    "Returns the patch notes for Minecraft Java Edition"
    return requests.get("https://launchercontent.mojang.com/javaPatchNotes.json", headers={"user-agent": get_user_agent()}).json()
