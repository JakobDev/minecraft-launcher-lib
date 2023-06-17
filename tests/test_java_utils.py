import minecraft_launcher_lib
from typing import List
import subprocess
import platform
import pathlib
import pytest
import sys


_org_subprocess_run = subprocess.run


def _subprocess_mock(cmd: List[str], **kwargs: dict) -> subprocess.CompletedProcess:
    return _org_subprocess_run([sys.executable, pathlib.Path(__file__).parent / "data" / "java_utils" / "java_mock.py"], **kwargs)


def test_get_java_information_unix(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(subprocess, "run", _subprocess_mock)

    with pytest.raises(ValueError, match="java was not found"):
        minecraft_launcher_lib.java_utils.get_java_information(tmp_path)

    (tmp_path / "bin").mkdir()
    (tmp_path / "bin" / "java").touch()

    info = minecraft_launcher_lib.java_utils.get_java_information(tmp_path)

    assert info["path"] == str(tmp_path)
    assert info["name"] == tmp_path.name
    assert info["version"] == "19.0.1"
    assert info["is_64bit"] is True
    assert info["openjdk"] is True
    assert info["java_path"] == str(tmp_path / "bin" / "java")
    assert info["javaw_path"] is None


def test_get_java_information_windows(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(subprocess, "run", _subprocess_mock)

    with pytest.raises(ValueError, match="java.exe was not found"):
        minecraft_launcher_lib.java_utils.get_java_information(tmp_path)

    (tmp_path / "bin").mkdir()
    (tmp_path / "bin" / "java.exe").touch()

    info = minecraft_launcher_lib.java_utils.get_java_information(tmp_path)

    assert info["path"] == str(tmp_path)
    assert info["name"] == tmp_path.name
    assert info["version"] == "19.0.1"
    assert info["is_64bit"] is True
    assert info["openjdk"] is True
    assert info["java_path"] == str(tmp_path / "bin" / "java.exe")
    assert info["javaw_path"] == str(tmp_path / "bin" / "javaw.exe")


def test_find_system_java_versions(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Windows")

    minecraft_launcher_lib.java_utils.find_system_java_versions(additional_directories=[tmp_path])

    monkeypatch.setattr(platform, "system", lambda: "Linux")

    (tmp_path / "test.txt").touch()
    (tmp_path / "testjava").mkdir()
    (tmp_path / "testjava" / "bin").mkdir()
    (tmp_path / "testjava" / "bin" / "java").touch()

    version_list = minecraft_launcher_lib.java_utils.find_system_java_versions(additional_directories=[tmp_path])

    assert isinstance(version_list, list)

    for i in version_list:
        assert isinstance(i, str)

    assert str(tmp_path / "testjava") in version_list


def test_find_system_java_versions_information(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(subprocess, "run", _subprocess_mock)

    (tmp_path / "testjava").mkdir()
    (tmp_path / "testjava" / "bin").mkdir()
    (tmp_path / "testjava" / "bin" / "java").touch()

    minecraft_launcher_lib.java_utils.find_system_java_versions_information(additional_directories=[tmp_path])
