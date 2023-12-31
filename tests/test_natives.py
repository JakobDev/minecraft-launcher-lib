import minecraft_launcher_lib
import platform
import pathlib
import pytest
import shutil
import os


def _prepare_natives_test_env(tmp_path: pathlib.Path) -> None:
    shutil.copytree(os.path.join(os.path.dirname(__file__), "data", "versions"), tmp_path / "versions")


def test_extract_natives_linux(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    _prepare_natives_test_env(tmp_path)

    monkeypatch.setattr(platform, "system", lambda: "Linux")

    minecraft_launcher_lib.install.install_minecraft_version("natives", tmp_path)

    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "liblwjgl.so")
    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "liblwjgl64.so")
    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "libopenal.so")
    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "liblwjgl64.so")
    assert not os.path.isdir(tmp_path / "versions" / "natives" / "natives" / "META-INF")

    minecraft_launcher_lib.natives.extract_natives("natives", tmp_path, tmp_path / "extract")

    assert os.path.isfile(tmp_path / "extract" / "liblwjgl.so")
    assert os.path.isfile(tmp_path / "extract" / "liblwjgl64.so")
    assert os.path.isfile(tmp_path / "extract" / "libopenal.so")
    assert os.path.isfile(tmp_path / "extract" / "liblwjgl64.so")
    assert not os.path.isdir(tmp_path / "extract" / "META-INF")


def test_extract_natives_mac(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    _prepare_natives_test_env(tmp_path)

    monkeypatch.setattr(platform, "system", lambda: "Darwin")

    minecraft_launcher_lib.install.install_minecraft_version("natives", tmp_path)

    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "liblwjgl.jnilib")
    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "openal.dylib")
    assert not os.path.isdir(tmp_path / "versions" / "natives" / "natives" / "META-INF")

    minecraft_launcher_lib.natives.extract_natives("natives", tmp_path, tmp_path / "extract")

    assert os.path.isfile(tmp_path / "extract" / "liblwjgl.jnilib")
    assert os.path.isfile(tmp_path / "extract" / "openal.dylib")
    assert not os.path.isdir(tmp_path / "extract" / "META-INF")


def test_extract_natives_windows(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    _prepare_natives_test_env(tmp_path)

    monkeypatch.setattr(platform, "architecture", lambda: ("64bit",))
    monkeypatch.setattr(platform, "system", lambda: "Windows")

    minecraft_launcher_lib.install.install_minecraft_version("natives", tmp_path)

    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "lwjgl.dll")
    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "lwjgl64.dll")
    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "OpenAL32.dll")
    assert os.path.isfile(tmp_path / "versions" / "natives" / "natives" / "OpenAL64.dll")
    assert not os.path.isdir(tmp_path / "versions" / "natives" / "natives" / "META-INF")

    minecraft_launcher_lib.natives.extract_natives("natives", tmp_path, tmp_path / "extract64")

    assert os.path.isfile(tmp_path / "extract64" / "lwjgl.dll")
    assert os.path.isfile(tmp_path / "extract64" / "lwjgl64.dll")
    assert os.path.isfile(tmp_path / "extract64" / "OpenAL32.dll")
    assert os.path.isfile(tmp_path / "extract64" / "OpenAL64.dll")
    assert not os.path.isdir(tmp_path / "extract64" / "META-INF")

    monkeypatch.setattr(platform, "architecture", lambda: ("32bit",))

    minecraft_launcher_lib.install.install_minecraft_version("natives", tmp_path)
    minecraft_launcher_lib.natives.extract_natives("natives", tmp_path, tmp_path / "extract32")

    assert os.path.isfile(tmp_path / "extract32" / "lwjgl.dll")
    assert os.path.isfile(tmp_path / "extract32" / "lwjgl64.dll")
    assert os.path.isfile(tmp_path / "extract32" / "OpenAL32.dll")
    assert os.path.isfile(tmp_path / "extract32" / "OpenAL64.dll")
    assert not os.path.isdir(tmp_path / "extract64" / "META-INF")


def test_extract_natives_inherit(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    _prepare_natives_test_env(tmp_path)

    monkeypatch.setattr(platform, "system", lambda: "Linux")

    minecraft_launcher_lib.install.install_minecraft_version("inherit-natives", tmp_path)

    minecraft_launcher_lib.natives.extract_natives("inherit-natives", tmp_path, tmp_path / "extract")

    assert os.path.isfile(tmp_path / "extract" / "liblwjgl.so")
    assert os.path.isfile(tmp_path / "extract" / "liblwjgl64.so")
    assert os.path.isfile(tmp_path / "extract" / "libopenal.so")
    assert os.path.isfile(tmp_path / "extract" / "liblwjgl64.so")
    assert not os.path.isdir(tmp_path / "extract" / "META-INF")


def test_extract_natives_invalid_version(tmp_path: pathlib.Path) -> None:
    # Checks if the VersionNotFound exception raised
    with pytest.raises(minecraft_launcher_lib.exceptions.VersionNotFound):
        minecraft_launcher_lib.natives.extract_natives("InvalidVersion", str(tmp_path), tmp_path / "extract")
