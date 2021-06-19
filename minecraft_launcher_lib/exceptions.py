from typing import List


class VersionNotFound(ValueError):
    """
    The given version does not exists
    """
    def __init__(self, version: str):
        self.version = version
        self.msg = f"Version {version} was not found"
        ValueError.__init__(self, self.msg)


class UnsupportedVersion(ValueError):
    """
    This Exception is raised when you try to run install_fabric() with a unsupported version
    """
    def __init__(self, version: str):
        self.version = version
        self.msg = f"Version {version} is not supported"
        ValueError.__init__(self, self.msg)


class ExternalProgramError(Exception):
    """
    This Exception is raised when a external program failed
    """
    def __init__(self, command: List[str], stdout: str, stderr: str):
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
