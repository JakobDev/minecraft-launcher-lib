import minecraft_launcher_lib


def test_list_forge_versions():
    version_list = minecraft_launcher_lib.forge.list_forge_versions()
    assert isinstance(version_list[0], str)


def test_find_forge_version():
    assert isinstance(minecraft_launcher_lib.forge.find_forge_version("1.16.2"), str)
    assert minecraft_launcher_lib.forge.find_forge_version("Test123") is None
