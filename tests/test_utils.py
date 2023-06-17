import minecraft_launcher_lib
import platform
import datetime
import pathlib
import pytest
import shutil
import json
import os


def _create_test_version_files(minecraft_directory: pathlib.Path) -> None:
    os.makedirs(os.path.join(minecraft_directory, "versions", "utilstest"))
    with open(os.path.join(minecraft_directory, "versions", "utilstest", "utilstest.json"), "w", encoding="utf-8") as f:
        data = {}
        data["id"] = "utilstest"
        data["type"] = "release"
        data["releaseTime"] = "1970-01-01T00:00:00"
        data["complianceLevel"] = 1
        json.dump(data, f)

    os.makedirs(os.path.join(minecraft_directory, "versions", "invalid-time"))
    with open(os.path.join(minecraft_directory, "versions", "invalid-time", "invalid-time.json"), "w", encoding="utf-8") as f:
        data = {}
        data["id"] = "invalid-time"
        data["type"] = "release"
        data["releaseTime"] = "invalid"
        data["complianceLevel"] = 1
        json.dump(data, f)

    (minecraft_directory / "versions" / "test.txt").touch()


def test_get_minecraft_directory(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    assert minecraft_launcher_lib.utils.get_minecraft_directory() == os.path.join(os.getenv("APPDATA", os.path.join(pathlib.Path.home(), "AppData", "Roaming")), ".minecraft")

    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    assert minecraft_launcher_lib.utils.get_minecraft_directory() == os.path.join(str(pathlib.Path.home()), "Library", "Application Support", "minecraft")

    monkeypatch.setattr(platform, "system", lambda: "Linux")
    assert minecraft_launcher_lib.utils.get_minecraft_directory() == os.path.join(str(pathlib.Path.home()), ".minecraft")


def test_get_latest_version() -> None:
    latest_version = minecraft_launcher_lib.utils.get_latest_version()
    assert "release" in latest_version
    assert "snapshot" in latest_version


def test_get_version_list() -> None:
    version_list = minecraft_launcher_lib.utils.get_version_list()
    for i in version_list:
        assert isinstance(i["id"], str)
        assert isinstance(i["type"], str)
        assert isinstance(i["releaseTime"], datetime.datetime)
        assert isinstance(i["complianceLevel"], int)


def test_get_installed_versions(tmp_path: pathlib.Path) -> None:
    _create_test_version_files(tmp_path)
    version_list = minecraft_launcher_lib.utils.get_installed_versions(tmp_path)
    version_list = minecraft_launcher_lib.utils.get_installed_versions(str(tmp_path))
    for i in version_list:
        assert isinstance(i["id"], str)
        assert isinstance(i["type"], str)
        assert isinstance(i["releaseTime"], datetime.datetime)
        assert isinstance(i["complianceLevel"], int)
    assert len(minecraft_launcher_lib.utils.get_installed_versions("not_existing_directory")) == 0


def test_get_available_versions(tmp_path: pathlib.Path) -> None:
    _create_test_version_files(tmp_path)
    version_list = minecraft_launcher_lib.utils.get_available_versions(tmp_path)
    version_list = minecraft_launcher_lib.utils.get_available_versions(str(tmp_path))
    for i in version_list:
        assert isinstance(i["id"], str)
        assert isinstance(i["type"], str)
        assert isinstance(i["releaseTime"], datetime.datetime)
        assert isinstance(i["complianceLevel"], int)
    assert isinstance(minecraft_launcher_lib.utils.get_available_versions("not_existing_directory"), list)


def test_get_java_executable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setenv("JAVA_HOME", "/testjavahome")
    assert minecraft_launcher_lib.utils.get_java_executable() == os.path.join("/testjavahome", "bin", "javaw.exe")

    monkeypatch.undo()
    monkeypatch.delenv("JAVA_HOME", False)
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(os.path, "isfile", lambda path: path == r"C:\Program Files (x86)\Common Files\Oracle\Java\javapath\javaw.exe")
    assert minecraft_launcher_lib.utils.get_java_executable() == r"C:\Program Files (x86)\Common Files\Oracle\Java\javapath\javaw.exe"

    monkeypatch.undo()
    monkeypatch.delenv("JAVA_HOME", False)
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(os.path, "isfile", lambda path: False)
    monkeypatch.setattr(shutil, "which", lambda name: "/testwhich" if name == "javaw" else None)
    assert minecraft_launcher_lib.utils.get_java_executable() == "/testwhich"

    monkeypatch.undo()
    monkeypatch.delenv("JAVA_HOME", False)
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(os.path, "isfile", lambda path: False)
    assert minecraft_launcher_lib.utils.get_java_executable() == "javaw"

    monkeypatch.undo()
    monkeypatch.setenv("JAVA_HOME", "/testjavahome")
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    assert minecraft_launcher_lib.utils.get_java_executable() == os.path.join("/testjavahome", "bin", "java")

    monkeypatch.undo()
    monkeypatch.delenv("JAVA_HOME", False)
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(os.path, "isfile", lambda path: False)
    monkeypatch.setattr(shutil, "which", lambda name: "/testwhich" if name == "java" else None)
    assert minecraft_launcher_lib.utils.get_java_executable() == "/testwhich"

    monkeypatch.undo()
    monkeypatch.delenv("JAVA_HOME", False)
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    monkeypatch.setattr(os.path, "isfile", lambda path: False)
    assert minecraft_launcher_lib.utils.get_java_executable() == "java"

    monkeypatch.undo()
    monkeypatch.setenv("JAVA_HOME", "/testjavahome")
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    assert minecraft_launcher_lib.utils.get_java_executable() == os.path.join("/testjavahome", "bin", "java")

    monkeypatch.undo()
    monkeypatch.delenv("JAVA_HOME", False)
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(os.path, "islink", lambda path: path == "/etc/alternatives/java", raising=False)
    monkeypatch.setattr(os, "readlink", lambda path: "testetc" if path == "/etc/alternatives/java" else None, raising=False)
    assert minecraft_launcher_lib.utils.get_java_executable() == "testetc"

    monkeypatch.undo()
    monkeypatch.delenv("JAVA_HOME", False)
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(os.path, "islink", lambda path: path == "/usr/lib/jvm/default-runtime", raising=False)
    monkeypatch.setattr(os, "readlink", lambda path: "testjvm" if path == "/usr/lib/jvm/default-runtime" else None, raising=False)
    assert minecraft_launcher_lib.utils.get_java_executable() == os.path.join("/usr", "lib", "jvm", "testjvm", "bin", "java")

    monkeypatch.undo()
    monkeypatch.delenv("JAVA_HOME", False)
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(os.path, "isfile", lambda path: False)
    monkeypatch.setattr(os.path, "islink", lambda path: False)
    monkeypatch.setattr(shutil, "which", lambda name: "/testwhich" if name == "java" else None)
    assert minecraft_launcher_lib.utils.get_java_executable() == "/testwhich"

    monkeypatch.undo()
    monkeypatch.delenv("JAVA_HOME", False)
    monkeypatch.setattr(shutil, "which", lambda name: None)
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(os.path, "isfile", lambda path: False)
    monkeypatch.setattr(os.path, "islink", lambda path: False)
    assert minecraft_launcher_lib.utils.get_java_executable() == "java"


def test_get_library_version() -> None:
    assert isinstance(minecraft_launcher_lib.utils.get_library_version(), str)


def test_generate_test_options() -> None:
    options = minecraft_launcher_lib.utils.generate_test_options()
    assert isinstance(options["username"], str)
    assert isinstance(options["uuid"], str)
    assert isinstance(options["token"], str)


def test_is_version_valid(tmp_path: pathlib.Path) -> None:
    _create_test_version_files(tmp_path)
    assert minecraft_launcher_lib.utils.is_version_valid("1.16", tmp_path) is True
    assert minecraft_launcher_lib.utils.is_version_valid("1.16", str(tmp_path)) is True
    assert minecraft_launcher_lib.utils.is_version_valid("utilstest", tmp_path) is True
    assert minecraft_launcher_lib.utils.is_version_valid("utilstest", str(tmp_path)) is True
    assert minecraft_launcher_lib.utils.is_version_valid("Test123", str(tmp_path)) is False
    assert minecraft_launcher_lib.utils.is_version_valid("Test123", tmp_path) is False


def test_get_minecraft_news() -> None:
    assert len(minecraft_launcher_lib.utils.get_minecraft_news()["article_grid"]) == 20
    assert len(minecraft_launcher_lib.utils.get_minecraft_news(page_size=50)["article_grid"]) == 50


def test_is_vanilla_version() -> None:
    assert minecraft_launcher_lib.utils.is_vanilla_version("1.18") is True
    assert minecraft_launcher_lib.utils.is_vanilla_version("test") is False


def test_is_platform_supported(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    assert minecraft_launcher_lib.utils.is_platform_supported() is True

    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    assert minecraft_launcher_lib.utils.is_platform_supported() is True

    monkeypatch.setattr(platform, "system", lambda: "Linux")
    assert minecraft_launcher_lib.utils.is_platform_supported() is True

    monkeypatch.setattr(platform, "system", lambda: "Haiku")
    assert minecraft_launcher_lib.utils.is_platform_supported() is False


def test_is_minecraft_installed(tmp_path: pathlib.Path) -> None:
    assert minecraft_launcher_lib.utils.is_minecraft_installed(tmp_path) is False

    (tmp_path / "versions").mkdir()
    (tmp_path / "libraries").mkdir()
    (tmp_path / "assets").mkdir()

    assert minecraft_launcher_lib.utils.is_minecraft_installed(tmp_path) is True
