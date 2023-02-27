import minecraft_launcher_lib
import datetime
import pathlib
import json
import os


def create_test_version_file(minecraft_directory: pathlib.Path):
    os.makedirs(os.path.join(minecraft_directory, "versions", "utilstest"))
    with open(os.path.join(minecraft_directory, "versions", "utilstest", "utilstest.json"), "w", encoding="utf-8") as f:
        data = {}
        data["id"] = "utilstest"
        data["type"] = "release"
        data["releaseTime"] = "1970-01-01T00:00:00"
        data["complianceLevel"] = 1
        json.dump(data, f)


def test_get_minecraft_directory():
    assert isinstance(minecraft_launcher_lib.utils.get_minecraft_directory(), str)


def test_get_latest_version():
    latest_version = minecraft_launcher_lib.utils.get_latest_version()
    assert "release" in latest_version
    assert "snapshot" in latest_version


def test_get_version_list():
    version_list = minecraft_launcher_lib.utils.get_version_list()
    for i in version_list:
        assert isinstance(i["id"], str)
        assert isinstance(i["type"], str)
        assert isinstance(i["releaseTime"], datetime.datetime)
        assert isinstance(i["complianceLevel"], int)


def test_get_installed_versions(tmp_path: pathlib.Path):
    create_test_version_file(tmp_path)
    version_list = minecraft_launcher_lib.utils.get_installed_versions(tmp_path)
    version_list = minecraft_launcher_lib.utils.get_installed_versions(str(tmp_path))
    for i in version_list:
        assert isinstance(i["id"], str)
        assert isinstance(i["type"], str)
        assert isinstance(i["releaseTime"], datetime.datetime)
        assert isinstance(i["complianceLevel"], int)
    assert len(minecraft_launcher_lib.utils.get_installed_versions("not_existing_directory")) == 0


def test_get_available_versions(tmp_path: pathlib.Path):
    create_test_version_file(tmp_path)
    version_list = minecraft_launcher_lib.utils.get_available_versions(tmp_path)
    version_list = minecraft_launcher_lib.utils.get_available_versions(str(tmp_path))
    for i in version_list:
        assert isinstance(i["id"], str)
        assert isinstance(i["type"], str)
        assert isinstance(i["releaseTime"], datetime.datetime)
        assert isinstance(i["complianceLevel"], int)
    assert isinstance(minecraft_launcher_lib.utils.get_available_versions("not_existing_directory"), list)


def test_get_java_executable():
    assert isinstance(minecraft_launcher_lib.utils.get_java_executable(), str)


def test_get_library_version():
    assert isinstance(minecraft_launcher_lib.utils.get_library_version(), str)


def test_generate_test_options():
    options = minecraft_launcher_lib.utils.generate_test_options()
    assert isinstance(options["username"], str)
    assert isinstance(options["uuid"], str)
    assert isinstance(options["token"], str)


def test_is_version_valid(tmp_path: pathlib.Path):
    create_test_version_file(tmp_path)
    assert minecraft_launcher_lib.utils.is_version_valid("1.16", tmp_path) is True
    assert minecraft_launcher_lib.utils.is_version_valid("1.16", str(tmp_path)) is True
    assert minecraft_launcher_lib.utils.is_version_valid("utilstest", tmp_path) is True
    assert minecraft_launcher_lib.utils.is_version_valid("utilstest", str(tmp_path)) is True
    assert minecraft_launcher_lib.utils.is_version_valid("Test123", str(tmp_path)) is False
    assert minecraft_launcher_lib.utils.is_version_valid("Test123", tmp_path) is False


def test_get_minecraft_news():
    assert len(minecraft_launcher_lib.utils.get_minecraft_news()["article_grid"]) == 20
    assert len(minecraft_launcher_lib.utils.get_minecraft_news(page_size=50)["article_grid"]) == 50


def test_is_vanilla_version():
    assert minecraft_launcher_lib.utils.is_vanilla_version("1.18") is True
    assert minecraft_launcher_lib.utils.is_vanilla_version("test") is False


def test_is_platform_supported():
    assert isinstance(minecraft_launcher_lib.utils.is_platform_supported(), bool)
