# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
import minecraft_launcher_lib
import datetime


def test_get_minecraft_news() -> None:
    news = minecraft_launcher_lib.news.get_minecraft_news()

    assert news["version"] == 1

    for entry in news["entries"]:
        assert isinstance(entry["title"], str)
        assert isinstance(entry["category"], str)
        assert isinstance(entry["date"], datetime.date)
        assert isinstance(entry["text"], str)

        assert isinstance(entry["playPageImage"]["title"], str)
        assert isinstance(entry["playPageImage"]["url"], str)

        assert isinstance(entry["newsPageImage"]["title"], str)
        assert isinstance(entry["newsPageImage"]["url"], str)
        assert isinstance(entry["newsPageImage"]["dimensions"]["width"], int)
        assert isinstance(entry["newsPageImage"]["dimensions"]["height"], int)

        assert isinstance(entry["readMoreLink"], str)

        for current_type in entry["newsType"]:
            assert isinstance(current_type, str)

        assert isinstance(entry["id"], str)


def test_get_java_patch_notes() -> None:
    patch_notes = minecraft_launcher_lib.news.get_java_patch_notes()

    assert patch_notes["version"] == 1

    for entry in patch_notes["entries"]:
        assert isinstance(entry["title"], str)
        assert entry["type"] in ("release", "snapshot")
        assert isinstance(entry["version"], str)

        assert isinstance(entry["image"]["title"], str)
        assert isinstance(entry["image"]["url"], str)

        assert isinstance(entry["body"], str)
        assert isinstance(entry["id"], str)
        assert isinstance(entry["contentPath"], str)
