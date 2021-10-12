from typing import NoReturn, List


class VersionNotFound(ValueError):
    """
    The given version does not exists
    """
    def __init__(self, version: str) -> NoReturn:
        self.version = version
        self.msg = f"Version {version} was not found"
        ValueError.__init__(self, self.msg)


class UnsupportedVersion(ValueError):
    """
    This Exception is raised when you try to run install_fabric() with a unsupported version
    """
    def __init__(self, version: str) -> NoReturn:
        self.version = version
        self.msg = f"Version {version} is not supported"
        ValueError.__init__(self, self.msg)


class ExternalProgramError(Exception):
    """
    This Exception is raised when a external program failed
    """
    def __init__(self, command: List[str], stdout: str, stderr: str) -> NoReturn:
        self.command = command
        self.stdout = stdout
        self.stderr = stderr


class InvalidRefreshToken(ValueError):
    """
    Raised when complete_refresh() is called with a invalid refresh token
    """
    pass
