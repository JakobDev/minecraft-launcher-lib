from ._test_helper import prepare_test_versions, prepare_requests_mock
import minecraft_launcher_lib
import requests_mock
import platform
import hashlib
import pathlib
import pytest
import os


def _assert_downloaded_file(path: pathlib.Path, size: int, hash: str) -> None:
    assert os.path.isfile(path)

    assert os.path.getsize(path) == size

    with open(path, "rb") as f:
        assert hashlib.sha1(f.read()).hexdigest() == hash


def test_install_minecraft_version(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    prepare_test_versions(tmp_path)
    prepare_requests_mock(requests_mock)

    minecraft_launcher_lib.install.install_minecraft_version("test1", tmp_path)

    _assert_downloaded_file(tmp_path / "libraries" / "ca" / "weblite" / "java-objc-bridge" / "1.1" / "java-objc-bridge-1.1.jar", 25, "2f8a26755f00bc8dc54cbf5e613f6d00f02a099e")
    _assert_downloaded_file(tmp_path / "libraries" / "org" / "slf4j" / "slf4j-api" / "2.0.1" / "slf4j-api-2.0.1.jar", 20, "03b7e695aa5cd7ca418ee6710e304d64d0491929")
    _assert_downloaded_file(tmp_path / "assets" / "log_configs" / "client-1.12.xml", 888, "bd65e7d2e3c237be76cfbef4c2405033d7f91521")
    _assert_downloaded_file(tmp_path / "versions" / "test1" / "test1.jar", 7, "173219a75174abb3e3a7bfd36148129df03f9123")


def test_install_minecraft_version_assets(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    prepare_test_versions(tmp_path)
    prepare_requests_mock(requests_mock)

    minecraft_launcher_lib.install.install_minecraft_version("assets", tmp_path)

    assert (tmp_path / "assets" / "objects" / "86" / "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8").is_file()
    assert (tmp_path / "assets" / "objects" / "e9" / "e9d71f5ee7c92d6dc9e92ffdad17b8bd49418f98").is_file()
    assert (tmp_path / "assets" / "objects" / "84" / "84a516841ba77a5b4648de2cd0dfcb30ea46dbb4").is_file()
    assert os.listdir(tmp_path / "assets" / "log_configs") == ["client-1.12.xml"]
    assert os.listdir(tmp_path / "assets" / "indexes") == ["test.json"]
    assert len(os.listdir(tmp_path / "assets" / "objects")) == 3


def test_install_minecraft_version_runtime(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    prepare_test_versions(tmp_path)
    prepare_requests_mock(requests_mock)

    minecraft_launcher_lib.install.install_minecraft_version("runtime", tmp_path)

    assert (tmp_path / "runtime" / "java-runtime-test" / "linux" / ".version").read_text().strip() == "17.0.3"


def test_install_minecraft_version_inherit(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    prepare_test_versions(tmp_path)
    prepare_requests_mock(requests_mock)

    minecraft_launcher_lib.install.install_minecraft_version("inherit", tmp_path)

    _assert_downloaded_file(tmp_path / "libraries" / "ca" / "weblite" / "java-objc-bridge" / "1.1" / "java-objc-bridge-1.1.jar", 25, "2f8a26755f00bc8dc54cbf5e613f6d00f02a099e")
    _assert_downloaded_file(tmp_path / "libraries" / "org" / "slf4j" / "slf4j-api" / "2.0.1" / "slf4j-api-2.0.1.jar", 20, "03b7e695aa5cd7ca418ee6710e304d64d0491929")
    _assert_downloaded_file(tmp_path / "libraries" / "com" / "ibm" / "icu" / "icu4j" / "71.1" / "icu4j-71.1.jar", 14, "78ef2a15d1afad3e435cdcaf12c502ac290ca707")
    _assert_downloaded_file(tmp_path / "assets" / "log_configs" / "client-1.12.xml", 888, "bd65e7d2e3c237be76cfbef4c2405033d7f91521")
    _assert_downloaded_file(tmp_path / "versions" / "inherit" / "inherit.jar", 7, "173219a75174abb3e3a7bfd36148129df03f9123")
    _assert_downloaded_file(tmp_path / "versions" / "test1" / "test1.jar", 7, "173219a75174abb3e3a7bfd36148129df03f9123")


def test_install_minecraft_version_extended(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    prepare_test_versions(tmp_path)

    prepare_requests_mock(requests_mock)

    minecraft_launcher_lib.install.install_minecraft_version("test2", tmp_path)

    _assert_downloaded_file(tmp_path / "libraries" / "ca" / "weblite" / "java-objc-bridge" / "1.1" / "java-objc-bridge-1.1.jar", 1, "86f7e437faa5a7fce15d1ddcb9eaeaea377667b8")


def test_install_minecraft_version_invalid_checksum(monkeypatch: pytest.MonkeyPatch, requests_mock: requests_mock.Mocker, tmp_path: pathlib.Path) -> None:
    monkeypatch.setattr(platform, "system", lambda: "Linux")

    prepare_test_versions(tmp_path)

    prepare_requests_mock(requests_mock)

    with pytest.raises(minecraft_launcher_lib.exceptions.InvalidChecksum):
        minecraft_launcher_lib.install.install_minecraft_version("checksum", tmp_path)


def test_install_minecraft_version_invalid_version(tmp_path: pathlib.Path) -> None:
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.install.install_minecraft_version("InvalidVersion", str(tmp_path))
