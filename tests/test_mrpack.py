from typing import List, Dict, Any
import minecraft_launcher_lib
import requests
import hashlib
import pathlib
import zipfile
import random
import pytest
import json
import copy
import os


def _create_test_index_pack(index: Dict[str, Any], tmp_path: pathlib.Path, overrides: List[str] = [], client_overrides: List[str] = []) -> str:
    while True:
        name = f"temp-pack-{random.randrange(100, 10000)}.mrpack"
        if not (tmp_path / name).exists():
            temp_pack = str(tmp_path / name)
            break

    with zipfile.ZipFile(temp_pack, "w") as zf:
        zf.writestr("modrinth.index.json", json.dumps(index))

        for i in overrides:
            zf.writestr(f"overrides/{i}", "This is a test override")

        for i in client_overrides:
            zf.writestr(f"client-overrides/{i}", "This is a test client-override")

    return temp_pack


def _create_test_dir(tmp_path: pathlib.Path) -> str:
    while True:
        name = f"temp-dir-{random.randrange(100, 10000)}"
        if not (tmp_path / name).exists():
            return str(tmp_path / name)


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
                **_generate_test_file("https://example.com")
            },
            {
                **{
                    "path": "b.txt",
                    "env": {
                        "client": "required",
                        "server": "required"
                    }
                },
                **_generate_test_file("https://example.com")
            },
            {
                **{
                    "path": "c.txt",
                    "env": {
                        "client": "optional",
                        "server": "optional"
                    }
                },
                **_generate_test_file("https://example.com")
            },
            {
                **{
                    "path": "d.txt",
                    "env": {
                        "client": "unsupported",
                        "server": "unsupported"
                    }
                },
                **_generate_test_file("https://example.com")
            },
        ],
        "dependencies": {
            "minecraft": "1.19"
        }
    }


def test_get_mrpack_information(tmp_path: pathlib.Path) -> None:
    index = _get_test_index()

    # Test without summary
    info = minecraft_launcher_lib.mrpack.get_mrpack_information(_create_test_index_pack(index, tmp_path))

    assert info["name"] == "Test"
    assert info["summary"] == ""
    assert info["versionId"] == "minecraft-launcher-lib.test"
    assert info["formatVersion"] == 1
    assert info["minecraftVersion"] == "1.19"
    assert info["optionalFiles"] == ["c.txt"]

    # Test with summary
    index["summary"] = "Summary"
    info_summary = minecraft_launcher_lib.mrpack.get_mrpack_information(_create_test_index_pack(index, tmp_path))

    assert info_summary["summary"] == "Summary"


def test_install_mrpack(tmp_path) -> None:
    index = _get_test_index()

    # Test without Optional File
    first_dir = _create_test_dir(tmp_path)
    minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(index, tmp_path), first_dir, mrpack_install_options={"skipDependenciesInstall": True})
    assert sorted(os.listdir(first_dir)) == sorted(["a.txt", "b.txt"])

    # Test with Optional File
    second_dir = _create_test_dir(tmp_path)
    minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(index, tmp_path), second_dir, mrpack_install_options={"skipDependenciesInstall": True, "optionalFiles": ["c.txt"]})
    assert sorted(os.listdir(second_dir)) == sorted(["a.txt", "b.txt", "c.txt"])

    # Test overides
    third_dir = _create_test_dir(tmp_path)
    minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(index, tmp_path, overrides=["overrides.txt"], client_overrides=["client/test.txt"]), third_dir, mrpack_install_options={"skipDependenciesInstall": True})
    assert sorted(os.listdir(third_dir)) == sorted(["a.txt", "b.txt", "overrides.txt", "client"])
    assert sorted(os.listdir(os.path.join(third_dir, "client"))) == sorted(["test.txt"])

    # Test FileOutsideMinecraftDirectory Exception with Files
    fourth_dir = _create_test_dir(tmp_path)
    exception_index = copy.deepcopy(index)
    exception_index["files"].append({**{
        "path": "../error.txt"
    },
        **_generate_test_file("https://example.com")
    })
    with pytest.raises(minecraft_launcher_lib.exceptions.FileOutsideMinecraftDirectory):
        minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(exception_index, tmp_path), fourth_dir, mrpack_install_options={"skipDependenciesInstall": True})

    # Test FileOutsideMinecraftDirectory Exception with Overrides
    fifth_dir = _create_test_dir(tmp_path)
    with pytest.raises(minecraft_launcher_lib.exceptions.FileOutsideMinecraftDirectory):
        minecraft_launcher_lib.mrpack.install_mrpack(_create_test_index_pack(index, tmp_path, overrides=["../overrides.txt"]), fifth_dir, mrpack_install_options={"skipDependenciesInstall": True})


def test_mrpack_launch_version(tmp_path) -> None:
    index = _get_test_index()

    index["dependencies"]["forge"] = "41.1.0"
    assert minecraft_launcher_lib.mrpack.get_mrpack_launch_version(_create_test_index_pack(index, tmp_path)) == "1.19-forge-41.1.0"
    del index["dependencies"]["forge"]

    index["dependencies"]["fabric-loader"] = "0.14.15"
    assert minecraft_launcher_lib.mrpack.get_mrpack_launch_version(_create_test_index_pack(index, tmp_path)) == "fabric-loader-0.14.15-1.19"
    del index["dependencies"]["fabric-loader"]

    index["dependencies"]["quilt-loader"] = "0.18.2"
    assert minecraft_launcher_lib.mrpack.get_mrpack_launch_version(_create_test_index_pack(index, tmp_path)) == "quilt-loader-0.18.2-1.19"
    del index["dependencies"]["quilt-loader"]
