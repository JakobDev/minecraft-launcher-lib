forge
==========================
.. note::
    Before using this module, please read this comment from the forge developers:

    .. code:: text

        Please do not automate the download and installation of Forge.
        Our efforts are supported by ads from the download page.
        If you MUST automate this, please consider supporting the project through https://www.patreon.com/LexManos/

    It's your choice, if you want to respect that and support forge.

forge allows you to install forge.

.. code:: python

    install_forge_version(versionid: str, minecraft_directory: Union[str, os.PathLike], callback: Dict[str,Callable]=None) -> NoReturn

Installs the given forge version in the given path. versionid must be one of the ids you get with list_forge_versions(). callback is the same dict as in the install module.

This function does not work for minecraft versions older than 1.13.

.. code:: python

    run_forge_installer(version: str) -> NoReturn

Download and execute the forge installer of the given forge version.

.. code:: python

    list_forge_versions() -> List[str]

Returns a list with all forge versions.

.. code:: python

    find_forge_version(vanilla_version: str) -> str

Returns the newest forge version for the given vanilla version. Returns None, if the given vanilla version has no forge version.

.. code:: python

    is_forge_version_valid(forge_version: str) -> bool

Checks if a forge version is valid.

.. code:: python

    supports_automatic_install(forge_version: str) -> bool

Checks if install_forge_version() supports the given forge version.
