import minecraft_launcher_lib


def test_VersionNotFound():
    v = minecraft_launcher_lib.exceptions.VersionNotFound("test")
    assert v.version == "test"
    assert v.msg == "Version test was not found"
    assert isinstance(v, ValueError)


def test_UnsupportedVersion():
    v = minecraft_launcher_lib.exceptions.UnsupportedVersion("test")
    assert v.version == "test"
    assert v.msg == "Version test is not supported"
    assert isinstance(v, ValueError)


def test_ExternalProgramError():
    c = minecraft_launcher_lib.exceptions.ExternalProgramError(["a", "b"], "out", "err")
    assert c.command == ["a", "b"]
    assert c.stdout == "out"
    assert c.stderr == "err"
    assert isinstance(c, Exception)


def test_InvalidRefreshToken():
    i = minecraft_launcher_lib.exceptions.InvalidRefreshToken()
    assert isinstance(i, ValueError)


def test_InvalidVanillaLauncherProfile():
    ex = minecraft_launcher_lib.exceptions.InvalidVanillaLauncherProfile({"name": "test"})
    assert ex.profile == {"name": "test"}
    assert isinstance(ex, ValueError)


def test_SecurityError():
    ex = minecraft_launcher_lib.exceptions.SecurityError("code", "msg")
    assert ex.code == "code"
    assert ex.message == "msg"
    assert isinstance(ex, Exception)


def test_FileOutsideMinecraftDirectory():
    ex = minecraft_launcher_lib.exceptions.FileOutsideMinecraftDirectory("path", "dir")
    assert ex.path == "path"
    assert ex.minecraft_directory == "dir"
    assert isinstance(ex, minecraft_launcher_lib.exceptions.SecurityError)


def test_InvalidChecksum():
    ex = minecraft_launcher_lib.exceptions.InvalidChecksum("url", "path", "expected", "actual")
    assert ex.url == "url"
    assert ex.path == "path"
    assert ex.expected_checksum == "expected"
    assert ex.actual_checksum == "actual"
    assert isinstance(ex, minecraft_launcher_lib.exceptions.SecurityError)
