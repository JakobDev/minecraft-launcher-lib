import minecraft_launcher_lib


def test_get_jvm_runtimes():
    runtime_list = minecraft_launcher_lib.runtime.get_jvm_runtimes()
    for i in runtime_list:
        assert isinstance(i, str)
