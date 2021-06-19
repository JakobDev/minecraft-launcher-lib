import minecraft_launcher_lib


def test_list_forge_versions():
    version_list = minecraft_launcher_lib.forge.list_forge_versions()
    assert isinstance(version_list[0], str)


def test_find_forge_version():
    assert isinstance(minecraft_launcher_lib.forge.find_forge_version("1.16.2"), str)
    assert minecraft_launcher_lib.forge.find_forge_version("Test123") is None


def test_is_forge_version_valid():
    assert minecraft_launcher_lib.forge.is_forge_version_valid("1.16.5-36.1.32") is True
    assert minecraft_launcher_lib.forge.is_forge_version_valid("Test123") is False


def test_supports_automatic_install():
    assert minecraft_launcher_lib.forge.supports_automatic_install("1.16.5-36.1.32") is True
    assert minecraft_launcher_lib.forge.supports_automatic_install("1.12-14.21.1.2443") is False
