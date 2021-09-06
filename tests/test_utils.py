import minecraft_launcher_lib
import json
import os


def create_test_version_file(minecraft_directory: str):
    os.makedirs(os.path.join(minecraft_directory, "versions", "utilstest"))
    with open(os.path.join(minecraft_directory, "versions", "utilstest", "utilstest.json"), "w", encoding="utf-8") as f:
        data = {}
        data["id"] = "utilstest"
        data["type"] = "release"
        json.dump(data, f)


def test_get_minecraft_directory():
    assert isinstance(minecraft_launcher_lib.utils.get_minecraft_directory(), str)


def test_get_latest_version():
    latest_version = minecraft_launcher_lib.utils.get_latest_version()
    assert "release" in latest_version
    assert "snapshot" in latest_version


def test_get_version_list():
    version_list = minecraft_launcher_lib.utils.get_version_list()
    assert "type" in version_list[0]
    assert "id" in version_list[0]


def test_get_installed_versions(tmpdir):
    create_test_version_file(tmpdir)
    version_list = minecraft_launcher_lib.utils. get_installed_versions(tmpdir)
    version_list = minecraft_launcher_lib.utils. get_installed_versions(str(tmpdir))
    assert version_list[0]["id"] == "utilstest"
    assert version_list[0]["type"] == "release"


def test_get_available_versions(tmpdir):
    create_test_version_file(tmpdir)
    version_list = minecraft_launcher_lib.utils.get_available_versions(tmpdir)
    version_list = minecraft_launcher_lib.utils.get_available_versions(str(tmpdir))
    assert "type" in version_list[0]
    assert "id" in version_list[0]


def test_get_java_executable():
    assert isinstance(minecraft_launcher_lib.utils.get_java_executable(), str)


def test_get_library_version():
    assert isinstance(minecraft_launcher_lib.utils.get_library_version(), str)


def test_generate_test_options():
    options = minecraft_launcher_lib.utils.generate_test_options()
    assert isinstance(options["username"], str)
    assert isinstance(options["uuid"], str)
    assert isinstance(options["token"], str)


def test_is_version_valid(tmpdir):
    create_test_version_file(tmpdir)
    assert minecraft_launcher_lib.utils.is_version_valid("1.16", tmpdir) is True
    assert minecraft_launcher_lib.utils.is_version_valid("1.16", str(tmpdir)) is True
    assert minecraft_launcher_lib.utils.is_version_valid("utilstest", tmpdir) is True
    assert minecraft_launcher_lib.utils.is_version_valid("utilstest", str(tmpdir)) is True
    assert minecraft_launcher_lib.utils.is_version_valid("Test123", str(tmpdir)) is False
    assert minecraft_launcher_lib.utils.is_version_valid("Test123", tmpdir) is False
