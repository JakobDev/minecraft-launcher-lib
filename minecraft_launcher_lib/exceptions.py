class VersionNotFound(ValueError):
    """
    The given version does not exists
    """
    def __init__(self,version: str):
        self.version = version
        self.msg = f"Version {version} was not found"
        ValueError.__init__(self, self.msg)
