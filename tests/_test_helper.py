import minecraft_launcher_lib
from typing import Union
import requests_mock
import pathlib
import shutil
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


def prepare_requests_mock(requests_mock: requests_mock.Mocker) -> None:
    requests_mock.get("minecraft-launcher-lib-test://assets.json", content=read_test_file("downloads/assets.json"))
    requests_mock.get("minecraft-launcher-lib-test://client.txt", content=read_test_file("downloads/client.txt"))

    requests_mock.get("minecraft-launcher-lib-test://libraries/java-objc-bridge.txt", content=read_test_file("downloads/libraries/java-objc-bridge.txt"))
    requests_mock.get("minecraft-launcher-lib-test://libraries/slf4j-api.txt", content=read_test_file("downloads/libraries/slf4j-api.txt"))

    requests_mock.get("minecraft-launcher-lib-test://client-1.12.xml", content=read_test_file("downloads/client-1.12.xml"))

    requests_mock.get("https://resources.download.minecraft.net/86/86f7e437faa5a7fce15d1ddcb9eaeaea377667b8", content=b"a")
    requests_mock.get("https://resources.download.minecraft.net/e9/e9d71f5ee7c92d6dc9e92ffdad17b8bd49418f98", content=b"b")
    requests_mock.get("https://resources.download.minecraft.net/84/84a516841ba77a5b4648de2cd0dfcb30ea46dbb4", content=b"c")

    requests_mock.get("https://libraries.minecraft.net/ca/weblite/java-objc-bridge/1.1/java-objc-bridge-1.1.jar", content=b"a")
