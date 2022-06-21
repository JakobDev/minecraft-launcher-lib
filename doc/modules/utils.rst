utils
==========================
utils just contains a few functions for helping you.

.. code:: python

    get_minecraft_directory() -> str

Returns the path to the standard minecraft directory.

.. code:: python

    get_latest_version() -> LatestMinecraftVersions

Returns the latest versions of snapshot and release.

.. code:: python

    get_version_list() -> List[MinecraftVersionInfo]

Returns a list of all versions with the type and release time.

.. code:: python

    get_installed_versions(minecraft_directory: Union[str, os.PathLike])  -> List[MinecraftVersionInfo]

Returns a list with all installed versions in the given path.

.. code:: python

    get_available_versions(minecraft_directory: Union[str, os.PathLike]) -> List[MinecraftVersionInfo]

Returns a list with all installable and only local installed (e.g. Forge) versions.

.. code:: python

    get_java_executable() -> str

Return the path to the java executable. This may not work correctly on all systems.

.. code:: python

    get_library_version() -> str

Return the version of the library.

.. code:: python

    generate_test_options() -> MinecraftOptions

Generates test options for get_minecraft_command(). Use this function to test launching without logging in. This should not be used in production.

.. code:: python

    is_version_valid(version: str,minecraft_directory: Union[str, os.PathLike]) -> bool

Checks if the given version exists

.. code:: python

    get_minecraft_news(page_size: int = 20) -> Dict

Get the news from minecraft.net

.. code:: python

    is_vanilla_version(version: str) -> bool

Checks if the given version is a vanilla version

.. code:: python

    is_platform_supported() -> bool

Checks if the current platform is supported
