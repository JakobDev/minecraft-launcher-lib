import minecraft_launcher_lib


def test_find_system_java_versions():
    version_list = minecraft_launcher_lib.java_utils.find_system_java_versions()

    assert isinstance(version_list, list)

    for i in version_list:
        assert isinstance(i, str)
