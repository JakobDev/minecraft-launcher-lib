import minecraft_launcher_lib
import pytest
import os


def test_get_jvm_runtimes():
    runtime_list = minecraft_launcher_lib.runtime.get_jvm_runtimes()
    for i in runtime_list:
        assert isinstance(i, str)


def test_get_installed_jvm_runtimes(tmpdir):
    for i in ["a", "b", "c"]:
        os.makedirs(os.path.join(tmpdir, "runtime", i))
    runtime_list = minecraft_launcher_lib.runtime.get_installed_jvm_runtimes(tmpdir)
    runtime_list.sort()
    assert runtime_list == ["a", "b", "c"]


def test_install_jvm_runtime_invalid_version(tmpdir):
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.runtime.install_jvm_runtime("InvalidVersion", tmpdir)
