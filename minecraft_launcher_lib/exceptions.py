"exceptions contains all custom exceptions that can be raised by minecraft_launcher_lib"
from .types import VanillaLauncherProfile
from typing import List


class VersionNotFound(ValueError):
    """
    The given version does not exists
    """
    def __init__(self, version: str) -> None:
        self.version: str = version
        "The version that caused the exception"

        self.msg: str = f"Version {version} was not found"
        "A message to display"

        ValueError.__init__(self, self.msg)


class UnsupportedVersion(ValueError):
    """
    This Exception is raised when you try to run :func:`~minecraft_launcher_lib.fabric.install_fabric` with a unsupported version
    """
    def __init__(self, version: str) -> None:
        self.version: str = version
        "The version that caused the exception"

        self.msg: str = f"Version {version} is not supported"
        "A message to display"

        ValueError.__init__(self, self.msg)


class ExternalProgramError(Exception):
    """
    This Exception is raised when a external program failed
    """
    def __init__(self, command: List[str], stdout: bytes, stderr: bytes) -> None:
        self.command: List[str] = command
        "The command that caused the error"

        self.stdout: bytes = stdout
        "The stdout of the command"

        self.stderr: bytes = stderr
        "The stderr of the command"


class InvalidRefreshToken(ValueError):
    """
    Raised when :func:`~minecraft_launcher_lib.microsoft_account.complete_refresh` is called with a invalid refresh token
    """
    pass


class InvalidVanillaLauncherProfile(ValueError):
    """
    Raised when a function from the :doc:`vanilla_launcher` module is called with a invalid vanilla profile
    """
    def __init__(self, profile: VanillaLauncherProfile) -> None:
        self.profile: VanillaLauncherProfile = profile
        "The invalid profile"

        super().__init__("Invalid VanillaLauncherProfile")
