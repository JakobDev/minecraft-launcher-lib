import minecraft_launcher_lib
from typing import Union
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
