exceptions
==========================
exceptions contains all custom exceptions that can be raised

VersionNotFound
    Raised when a given version does not exists

UnsupportedVersion
    Raised when install_fabric() is called with a unsupported version.

ExternalProgramError
    Raised when a external program fails to execute

InvalidRefreshToken
    Raised when complete_refresh() is called with a invalid refresh token
