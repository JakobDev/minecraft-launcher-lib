import minecraft_launcher_lib
from typing import Union, Any
import requests_mock
import hashlib
import pathlib
import shutil
import json
import lzma
import os


def prepare_test_versions(tmp_path: Union[str, os.PathLike]) -> None:
    shutil.copytree(pathlib.Path(__file__).parent / "data" / "versions", os.path.join(tmp_path, "versions"))


def assert_func(expression: bool) -> None:
    if not expression:
        raise AssertionError()


def get_test_callbacks() -> minecraft_launcher_lib.types.CallbackDict:
    return {
        "setStatus": lambda value: assert_func(isinstance(value, str)),
        "setProgress": lambda value: assert_func(isinstance(value, int)),
        "setMax": lambda value: assert_func(isinstance(value, int))
    }


def read_test_file(name: str) -> bytes:
    with open(os.path.join(os.path.dirname(__file__), "data", name), "rb") as f:
        return f.read()


def read_test_json_file(name: str) -> Any:
    with open(os.path.join(os.path.dirname(__file__), "data", name), "r", encoding="utf-8") as f:
        return json.load(f)


def prepare_requests_mock(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get("minecraft-launcher-lib-test://text.txt", text="Hello World")
    requests_mock.get("minecraft-launcher-lib-test://text.txt.lzma", content=lzma.compress(b"Hello World"))

    requests_mock.get("minecraft-launcher-lib-test://assets.json", content=read_test_file("downloads/assets.json"))
    requests_mock.get("minecraft-launcher-lib-test://client.txt", content=read_test_file("downloads/client.txt"))
    requests_mock.get("minecraft-launcher-lib-test://client-inherit.txt", text="inherit")

    requests_mock.get("minecraft-launcher-lib-test://libraries/java-objc-bridge.txt", content=read_test_file("downloads/libraries/java-objc-bridge.txt"))
    requests_mock.get("minecraft-launcher-lib-test://libraries/slf4j-api.txt", content=read_test_file("downloads/libraries/slf4j-api.txt"))
    requests_mock.get("minecraft-launcher-lib-test://libraries/icu4j.txt", text="icu4j-71.1.jar")

    requests_mock.get("minecraft-launcher-lib-test://client-1.12.xml", content=read_test_file("downloads/client-1.12.xml"))

    requests_mock.get("https://resources.download.minecraft.net/86/86f7e437faa5a7fce15d1ddcb9eaeaea377667b8", content=b"a")
    requests_mock.get("https://resources.download.minecraft.net/e9/e9d71f5ee7c92d6dc9e92ffdad17b8bd49418f98", content=b"b")
    requests_mock.get("https://resources.download.minecraft.net/84/84a516841ba77a5b4648de2cd0dfcb30ea46dbb4", content=b"c")

    requests_mock.get("https://libraries.minecraft.net/ca/weblite/java-objc-bridge/1.1/java-objc-bridge-1.1.jar", content=b"a")

    # Runtime
    requests_mock.get("https://launchermeta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json", content=read_test_file("runtime/list.json"))
    requests_mock.get("https://test.json", content=read_test_file("runtime/runtime.json"))
    requests_mock.get("https://error.json", content=read_test_file("runtime/error.json"))

    fabric_quilt_versions = [
        {"version": "unstable", "stable": False},
        {"version": "test2", "stable": True}
    ]
    requests_mock.get("https://meta.fabricmc.net/v2/versions/game", json=fabric_quilt_versions)
    requests_mock.get("https://meta.quiltmc.org/v3/versions/game", json=fabric_quilt_versions)

    online_release_version = read_test_json_file("versions/test1/test1.json")
    online_release_version["id"] = "online-release"
    online_release_version_bytes = json.dumps(online_release_version).encode("utf-8")
    requests_mock.get("minecraft-launcher-lib-test://versions/online-release.json", content=online_release_version_bytes)

    version_list = {
        "latest": {
            "release": "online-release",
            "snapshot": "online-snapshot"
        },
        "versions": [
            {
                "id": "online-release",
                "type": "release",
                "url": "minecraft-launcher-lib-test://versions/online-release.json",
                "time": "2023-12-18T15:46:45+00:00",
                "releaseTime": "2023-12-18T15:46:45+00:00",
                "sha1": hashlib.sha1(online_release_version_bytes).hexdigest(),
                "complianceLevel": 1
            }
        ]
    }
    requests_mock.get("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json", json=version_list)
