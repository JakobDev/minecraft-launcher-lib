import minecraft_launcher_lib
import datetime
import pathlib
import pytest
import os


def test_get_jvm_runtimes():
    runtime_list = minecraft_launcher_lib.runtime.get_jvm_runtimes()
    for i in runtime_list:
        assert isinstance(i, str)


def test_get_installed_jvm_runtimes(tmp_path: pathlib.Path):
    for i in ["a", "b", "c"]:
        os.makedirs(os.path.join(tmp_path, "runtime", i))
    runtime_list = minecraft_launcher_lib.runtime.get_installed_jvm_runtimes(tmp_path)
    runtime_list.sort()
    assert runtime_list == ["a", "b", "c"]


def test_install_jvm_runtime_invalid_version(tmp_path: pathlib.Path):
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.runtime.install_jvm_runtime("InvalidVersion", tmp_path)


def test_get_jvm_runtime_information():
    info = minecraft_launcher_lib.runtime.get_jvm_runtime_information(minecraft_launcher_lib.runtime.get_jvm_runtimes()[0])
    assert isinstance(info["released"], datetime.datetime)
    assert isinstance(info["name"], str)
    assert len(info) == 2

    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.runtime.get_jvm_runtime_information("InvalidVersion")
