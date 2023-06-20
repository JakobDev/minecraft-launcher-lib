import minecraft_launcher_lib
import requests_mock
import subprocess
import platform
import datetime
import pathlib
import pytest
import json
import os


def test_get_jvm_runtimes() -> None:
    runtime_list = minecraft_launcher_lib.runtime.get_jvm_runtimes()
    for i in runtime_list:
        assert isinstance(i, str)


def test_get_installed_jvm_runtimes(tmp_path: pathlib.Path) -> None:
    assert len(minecraft_launcher_lib.runtime.get_installed_jvm_runtimes(tmp_path)) == 0

    for i in ["a", "b", "c"]:
        os.makedirs(os.path.join(tmp_path, "runtime", i))

    runtime_list = minecraft_launcher_lib.runtime.get_installed_jvm_runtimes(tmp_path)
    runtime_list.sort()
    assert runtime_list == ["a", "b", "c"]


def test_install_jvm_runtime(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    with open(os.path.join(os.path.dirname(__file__), "data", "runtime", "list.json"), "r", encoding="utf-8") as f:
        list_data = json.load(f)

    with open(os.path.join(os.path.dirname(__file__), "data", "runtime", "runtime.json"), "r", encoding="utf-8") as f:
        runtime_data = json.load(f)

    with open(os.path.join(os.path.dirname(__file__), "data", "runtime", "error.json"), "r", encoding="utf-8") as f:
        error_data = json.load(f)

    monkeypatch.setattr(platform, "architecture", lambda: ("test",))
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    requests_mock.get("https://launchermeta.mojang.com/v1/products/java-runtime/2ec0cc96c44e5a76b9c8b7c39df7210883d12871/all.json", json=list_data)
    requests_mock.get("https://test.json", json=runtime_data)
    requests_mock.get("https://error.json", json=error_data)
    requests_mock.real_http = True

    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.runtime.install_jvm_runtime("java-runtime-invalid", tmp_path)

    minecraft_launcher_lib.runtime.install_jvm_runtime("java-runtime-empty", tmp_path)

    assert len(os.listdir(tmp_path)) == 0

    # This functions needs to be patched, so the test also works on non Unix Systems
    monkeypatch.setattr(os, "symlink", lambda target, file: pathlib.Path(file).write_text(target), raising=False)
    monkeypatch.setattr(subprocess, "run", lambda cmd: pathlib.Path(cmd[2] + ".execute").touch() if cmd[0] == "chmod" else None)

    minecraft_launcher_lib.runtime.install_jvm_runtime("java-runtime-test", tmp_path)

    assert (tmp_path / "runtime" / "java-runtime-test" / "linux" / ".version").read_text().strip() == "17.0.3"
    assert os.path.isfile(tmp_path / "runtime" / "java-runtime-test" / "linux" / "java-runtime-test.sha1")
    assert os.path.isfile(tmp_path / "runtime" / "java-runtime-test" / "linux" / "java-runtime-test" / "jre.bundle" / "Contents" / "Home" / "COPYRIGHT")
    assert os.path.isfile(tmp_path / "runtime" / "java-runtime-test" / "linux" / "java-runtime-test" / "jre.bundle" / "Contents" / "Home" / "LICENSE")
    assert os.path.isfile(tmp_path / "runtime" / "java-runtime-test" / "linux" / "java-runtime-test" / "jre.bundle" / "Contents" / "Home" / "LICENSE.execute")
    assert os.path.isdir(tmp_path / "runtime" / "java-runtime-test" / "linux" / "java-runtime-test" / "lib" / "desktop" / "mime")
    assert (tmp_path / "runtime" / "java-runtime-test" / "linux" / "java-runtime-test" / "links" / "testlink").read_text().strip() == "../target"

    # Test, if the exceptions are handeld
    monkeypatch.setattr(subprocess, "run", lambda cmd: exec("raise FileNotFoundError()"))
    monkeypatch.setattr(os, "symlink", lambda target, file: exec("raise Exception()"), raising=False)
    minecraft_launcher_lib.runtime.install_jvm_runtime("java-runtime-test", tmp_path)

    with pytest.raises(minecraft_launcher_lib.exceptions.FileOutsideMinecraftDirectory):
        minecraft_launcher_lib.runtime.install_jvm_runtime("java-runtime-error", tmp_path)


def test_get_executable_path(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "architecture", lambda: ("test",))
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    linux_java = (tmp_path / "runtime" / "java-runtime-test" / "linux" / "java-runtime-test" / "bin" / "java")
    os.makedirs(linux_java.parent)
    linux_java.touch()
    assert minecraft_launcher_lib.runtime.get_executable_path("java-runtime-test", tmp_path) == str(linux_java)

    monkeypatch.undo()
    monkeypatch.setattr(platform, "architecture", lambda: ("test",))
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    windows_java = (tmp_path / "runtime" / "java-runtime-test" / "windows-x64" / "java-runtime-test" / "bin" / "java.exe")
    os.makedirs(windows_java.parent)
    windows_java.touch()
    assert minecraft_launcher_lib.runtime.get_executable_path("java-runtime-test", tmp_path) == str(windows_java)

    monkeypatch.undo()
    monkeypatch.setattr(platform, "machine", lambda: "arm64")
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    mac_java = (tmp_path / "runtime" / "java-runtime-test" / "mac-os-arm64" / "java-runtime-test" / "jre.bundle" / "Contents" / "Home" / "bin" / "java")
    os.makedirs(mac_java.parent)
    mac_java.touch()
    assert minecraft_launcher_lib.runtime.get_executable_path("java-runtime-test", tmp_path) == str(mac_java)

    monkeypatch.undo()
    assert minecraft_launcher_lib.runtime.get_executable_path("java-runtime-invalid", tmp_path) is None


def _test_runtime_information() -> None:
    info = minecraft_launcher_lib.runtime.get_jvm_runtime_information("java-runtime-gamma")
    assert isinstance(info["released"], datetime.datetime)
    assert isinstance(info["name"], str)
    assert len(info) == 2


def test_get_jvm_runtime_information(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(platform, "architecture", lambda: ("32bit",))
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    _test_runtime_information()

    monkeypatch.undo()
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    _test_runtime_information()

    monkeypatch.setattr(platform, "architecture", lambda: ("32bit",))
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    with pytest.raises(minecraft_launcher_lib.exceptions.PlatformNotSupported):
        minecraft_launcher_lib.runtime.get_jvm_runtime_information("java-runtime-gamma")

    monkeypatch.undo()
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    _test_runtime_information()

    monkeypatch.undo()
    monkeypatch.setattr(platform, "machine", lambda: "arm64")
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    _test_runtime_information()

    monkeypatch.undo()
    monkeypatch.setattr(platform, "machine", lambda: "test")
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    _test_runtime_information()

    monkeypatch.undo()
    monkeypatch.setattr(platform, "system", lambda: "Haiku")
    with pytest.raises(minecraft_launcher_lib.exceptions.PlatformNotSupported):
        minecraft_launcher_lib.runtime.get_jvm_runtime_information("java-runtime-gamma")

    monkeypatch.undo()
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.runtime.get_jvm_runtime_information("InvalidVersion")
