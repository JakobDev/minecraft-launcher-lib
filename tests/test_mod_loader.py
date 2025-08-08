# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2025 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
import minecraft_launcher_lib
import pytest


def test_mod_loader_get_latest_loader_version(monkeypatch: pytest.MonkeyPatch) -> None:
    loader = minecraft_launcher_lib.mod_loader.get_mod_loader("forge")

    monkeypatch.setattr(loader, "get_loader_versions", lambda minecraft_version, stable_only: ["test-stable-loader"])
    assert loader.get_latest_loader_version("test") == "test-stable-loader"

    monkeypatch.setattr(loader, "get_loader_versions", lambda minecraft_version, stable_only: [] if stable_only else ["test-unstable-loader"])
    assert loader.get_latest_loader_version("test") == "test-unstable-loader"

    monkeypatch.setattr(loader, "get_loader_versions", lambda minecraft_version, stable_only: [])
    with pytest.raises(minecraft_launcher_lib.exceptions.UnsupportedVersion):
        loader.get_latest_loader_version("test")


def test_get_mod_loader() -> None:
    for loader_id in ("forge", "neoforge", "fabric", "quilt"):
        assert minecraft_launcher_lib.mod_loader.get_mod_loader(loader_id).get_id() == loader_id

    with pytest.raises(ValueError) as ex:
        minecraft_launcher_lib.mod_loader.get_mod_loader("invalid")

    assert ex.value.args[0] == "mod loader invalid not found"


def test_list_mod_loader() -> None:
    assert minecraft_launcher_lib.mod_loader.list_mod_loader() == ["forge", "neoforge", "fabric", "quilt"]
