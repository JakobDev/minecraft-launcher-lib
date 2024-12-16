# This file is part of minecraft-launcher-lib (https://codeberg.org/JakobDev/minecraft-launcher-lib)
# SPDX-FileCopyrightText: Copyright (c) 2019-2024 JakobDev <jakobdev@gmx.de> and contributors
# SPDX-License-Identifier: BSD-2-Clause
from ._test_helper import prepare_test_versions, get_test_callbacks, prepare_requests_mock, create_bytes_zip
from typing import List, Dict, Any
import minecraft_launcher_lib
import pytest_subtests
import requests_mock
import subprocess
import platform
import requests
import hashlib
import pathlib
import zipfile
import pytest
import json
import copy
import os


def _create_test_index_pack(index: Dict[str, Any], mrpack_path: pathlib.Path, overrides: List[str] = [], client_overrides: List[str] = []) -> pathlib.Path:
    with zipfile.ZipFile(mrpack_path, "w") as zf:
        zf.writestr("modrinth.index.json", json.dumps(index))

        for i in overrides:
            zf.writestr(f"overrides/{i}", "This is a test override")

        for i in client_overrides:
            zf.writestr(f"client-overrides/{i}", "This is a test client-override")

    return mrpack_path


_test_file_cache: Dict[str, Dict[str, Any]] = {}


def _generate_test_file(url: str) -> Dict[str, Any]:
    if url in _test_file_cache:
        return _test_file_cache[url]

    r = requests.get(url, stream=True)

    data = {
        "hashes": {
            "sha1": hashlib.sha1(r.content).hexdigest(),
            "sha512": hashlib.sha512(r.content).hexdigest()
        },
        "downloads": [url],
        "fileSize": len(r.content)
    }

    _test_file_cache[url] = data
    return data


def _get_test_index() -> Dict[str, Any]:
    return {
        "formatVersion": 1,
        "name": "Test",
        "versionId": "minecraft-launcher-lib.test",
        "files": [
            {
                **{
                    "path": "a.txt"
                },
                **_generate_test_file("minecraft-launcher-lib-test://text.txt")
            },
            {
                **{
                    "path": "b.txt",
                    "env": {
                        "client": "required",
                        "server": "required"
                    }
                },
                **_generate_test_file("minecraft-launcher-lib-test://text.txt")
            },
            {
                **{
                    "path": "c.txt",
                    "env": {
                        "client": "optional",
                        "server": "optional"
                    }
                },
                **_generate_test_file("minecraft-launcher-lib-test://text.txt")
            },
            {
                **{
                    "path": "d.txt",
                    "env": {
                        "client": "unsupported",
                        "server": "unsupported"
                    }
                },
                **_generate_test_file("minecraft-launcher-lib-test://text.txt")
            },
        ],
        "dependencies": {
            "minecraft": "test1"
        }
    }


def test_get_mrpack_information(requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    prepare_requests_mock(requests_mock)

    index = _get_test_index()

    # Test without summary
    info = minecraft_launcher_lib.mrpack.get_mrpack_information(_create_test_index_pack(index, tmp_path / "WithoutSummary.mrpack"))

    assert info["name"] == "Test"
    assert info["summary"] == ""
    assert info["versionId"] == "minecraft-launcher-lib.test"
    assert info["formatVersion"] == 1
    assert info["minecraftVersion"] == "test1"
    assert info["optionalFiles"] == ["c.txt"]

    # Test with summary
    index["summary"] = "Summary"
    info_summary = minecraft_launcher_lib.mrpack.get_mrpack_information(_create_test_index_pack(index, tmp_path / "WithSummary.mrpack"))

    assert info_summary["summary"] == "Summary"


def test_install_mrpack(monkeypatch: pytest.MonkeyPatch, subtests: pytest_subtests.SubTests, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    prepare_requests_mock(requests_mock)

    index = _get_test_index()

    with subtests.test("Without optional file"):
        test_dir = tmp_path / "WithoutOptionalFile"
        minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(index, tmp_path / "WithoutOptionalFile.mrpack"), test_dir, mrpack_install_options={"skipDependenciesInstall": True})
        assert sorted(os.listdir(test_dir)) == sorted(["a.txt", "b.txt"])

    with subtests.test("With optional file"):
        test_dir = tmp_path / "WithOptionalFile"
        minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(index, tmp_path / "WithOptionalFile.mrpack"), test_dir, mrpack_install_options={"skipDependenciesInstall": True, "optionalFiles": ["c.txt"]})
        assert sorted(os.listdir(test_dir)) == sorted(["a.txt", "b.txt", "c.txt"])

    with subtests.test("Overrides"):
        test_dir = tmp_path / "Overrides"
        minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(index, tmp_path / "Overrides.mrpack", overrides=["overrides.txt", "subdir/overrides.txt"], client_overrides=["client/test.txt"]), test_dir, mrpack_install_options={"skipDependenciesInstall": True})
        assert sorted(os.listdir(test_dir)) == sorted(["a.txt", "b.txt", "overrides.txt", "client", "subdir"])
        assert sorted(os.listdir(os.path.join(test_dir, "subdir"))) == sorted(["overrides.txt"])
        assert sorted(os.listdir(os.path.join(test_dir, "client"))) == sorted(["test.txt"])

    with subtests.test("FileOutsideMinecraftDirectory Exception with files"):
        test_dir = tmp_path / "FileOutsideMinecraftDirectoryExceptionFiles"
        exception_index = copy.deepcopy(index)
        exception_index["files"].append({**{
            "path": "../error.txt"
        },
            **_generate_test_file("minecraft-launcher-lib-test://text.txt")
        })
        with pytest.raises(minecraft_launcher_lib.exceptions.FileOutsideMinecraftDirectory):
            minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(exception_index, tmp_path / "FileOutsideMinecraftDirectoryExceptionFiles.mrpack"), test_dir, mrpack_install_options={"skipDependenciesInstall": True})

    with subtests.test("FileOutsideMinecraftDirectory Exception with overrides"):
        test_dir = tmp_path / "FileOutsideMinecraftDirectoryExceptionOverrides"
        with pytest.raises(minecraft_launcher_lib.exceptions.FileOutsideMinecraftDirectory):
            minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(index, tmp_path / "FileOutsideMinecraftDirectoryExceptionOverrides.mrpack", overrides=["../overrides.txt"]), test_dir, mrpack_install_options={"skipDependenciesInstall": True})

    with subtests.test("Modpack directory"):
        test_dir = tmp_path / "ModpackDirectoryNotExisting"
        modpack_dir = tmp_path / "ModpackDirectory"
        minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(index, tmp_path / "ModpackDirectory.mrpack"), test_dir, modpack_directory=modpack_dir, mrpack_install_options={"skipDependenciesInstall": True})
        assert sorted(os.listdir(modpack_dir)) == sorted(["a.txt", "b.txt"])
        assert not os.path.isdir(test_dir)

    with subtests.test("ForgeInvalid"):
        forge_dir = tmp_path / "ForgeInvalid"
        forge_index = copy.deepcopy(index)
        forge_index["dependencies"]["forge"] = "invalid"
        prepare_test_versions(forge_dir)
        requests_mock.head("https://maven.minecraftforge.net/net/minecraftforge/forge/test1-invalid/forge-test1-invalid-installer.jar", status_code=404)
        requests_mock.head("https://maven.minecraftforge.net/net/minecraftforge/forge/test1-invalid-test1/forge-test1-invalid-test1-installer.jar", status_code=404)
        with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
            minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(forge_index, tmp_path / "ForgeInvalid.mrpack"), forge_dir, callback=get_test_callbacks())

    with subtests.test("ForgeValid"):
        monkeypatch.setattr(platform, "system", lambda: "Linux")
        monkeypatch.setattr(platform, "architecture", lambda: ("64bit", "ELF"))
        monkeypatch.setattr(subprocess, "run", lambda cmd, **kwargs: None)

        forge_dir = tmp_path / "ForgeValid"
        forge_index = copy.deepcopy(index)
        forge_index["dependencies"]["forge"] = "forgetest1"
        prepare_test_versions(forge_dir)
        requests_mock.get("https://maven.minecraftforge.net/net/minecraftforge/forge/test1-forgetest1/forge-test1-forgetest1-installer.jar", content=create_bytes_zip(pathlib.Path(__file__).parent / "data" / "forge" / "forgetest1"))
        requests_mock.head("https://maven.minecraftforge.net/net/minecraftforge/forge/test1-forgetest1/forge-test1-forgetest1-installer.jar", status_code=200)
        minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(forge_index, tmp_path / "ForgeValid.mrpack"), forge_dir, callback=get_test_callbacks())

        monkeypatch.undo()

    with subtests.test("Fabric"):
        fabric_dir = tmp_path / "Fabric"
        fabric_index = copy.deepcopy(index)
        fabric_index["dependencies"]["fabric-loader"] = "invalid"
        prepare_test_versions(fabric_dir)
        with pytest.raises(minecraft_launcher_lib.exceptions.UnsupportedVersion):
            minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(fabric_index, tmp_path / "Fabric.mrpack"), fabric_dir, callback=get_test_callbacks())

    with subtests.test("Quilt"):
        quilt_dir = tmp_path / "Quilt"
        quilt_index = copy.deepcopy(index)
        quilt_index["dependencies"]["quilt-loader"] = "invalid"
        prepare_test_versions(quilt_dir)
        with pytest.raises(minecraft_launcher_lib.exceptions.UnsupportedVersion):
            minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(quilt_index, tmp_path / "Quilt.mrpack"), quilt_dir, callback=get_test_callbacks())


def test_mrpack_launch_version(subtests: pytest_subtests.SubTests, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    prepare_requests_mock(requests_mock)

    index = _get_test_index()

    with subtests.test("Vanilla"):
        assert minecraft_launcher_lib.mrpack.get_mrpack_launch_version(_create_test_index_pack(index, tmp_path / "Vanilla.mrpack")) == "test1"

    with subtests.test("Forge"):
        index["dependencies"]["forge"] = "41.1.0"
        assert minecraft_launcher_lib.mrpack.get_mrpack_launch_version(_create_test_index_pack(index, tmp_path / "Forge.mrpack")) == "test1-forge-41.1.0"
        del index["dependencies"]["forge"]

    with subtests.test("Fabric"):
        index["dependencies"]["fabric-loader"] = "0.14.15"
        assert minecraft_launcher_lib.mrpack.get_mrpack_launch_version(_create_test_index_pack(index, tmp_path / "Fabric.mrpack")) == "fabric-loader-0.14.15-test1"
        del index["dependencies"]["fabric-loader"]

    with subtests.test("Quilt"):
        index["dependencies"]["quilt-loader"] = "0.18.2"
        assert minecraft_launcher_lib.mrpack.get_mrpack_launch_version(_create_test_index_pack(index, tmp_path / "Quilt.mrpack")) == "quilt-loader-0.18.2-test1"
        del index["dependencies"]["quilt-loader"]
