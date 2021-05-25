import minecraft_launcher_lib


def test_get_all_minecraft_versions():
    version_list = minecraft_launcher_lib.fabric.get_all_minecraft_versions()
    assert isinstance(version_list[0]["version"], str)
    assert isinstance(version_list[0]["stable"], bool)


def test_get_stable_minecraft_versions():
    version_list = minecraft_launcher_lib.fabric.get_stable_minecraft_versions()
    assert isinstance(version_list[0], str)


def test_get_latest_minecraft_version():
    assert isinstance(minecraft_launcher_lib.fabric.get_latest_minecraft_version(), str)


def test_get_latest_stable_minecraft_version():
    assert isinstance(minecraft_launcher_lib.fabric.get_latest_stable_minecraft_version(), str)


def test_is_minecraft_version_supported():
    assert minecraft_launcher_lib.fabric.is_minecraft_version_supported("1.16") is True
    assert minecraft_launcher_lib.fabric.is_minecraft_version_supported("1.0") is False


def test_get_all_loader_versions():
    version_list = minecraft_launcher_lib.fabric.get_all_loader_versions()
    assert isinstance(version_list[0]["separator"], str)
    assert isinstance(version_list[0]["build"], int)
    assert isinstance(version_list[0]["maven"], str)
    assert isinstance(version_list[0]["version"], str)
    assert isinstance(version_list[0]["stable"], bool)


def test_get_latest_loader_version():
    assert isinstance(minecraft_launcher_lib.fabric.get_latest_loader_version(), str)


def test_get_latest_installer_version():
    assert isinstance(minecraft_launcher_lib.fabric.get_latest_installer_version(), str)
