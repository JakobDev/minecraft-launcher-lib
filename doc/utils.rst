utils
==========================
utils just contains a few functions for helping you.

.. code:: python

    get_minecraft_directory()

Returns the path to the standard minecraft directory.

.. code:: python

    get_latest_version()

Returns the latest versions of snapshot and release.

.. code:: python

    get_version_list()

Returns a list of all versions with the type.

.. code:: python

    get_installed_versions(path)

Returns a list with all installed versions in the given path.

.. code:: python

    get_available_versions(path)

Returns a list with all installable and only local installed (e.g. Forge) versions.

.. code:: python

    get_java_executable()

Return the path to the java executable. This may not work correctly on all systems.

.. code:: python

    get_library_version()

Return the version of the library.

.. code:: python

    generate_test_options()

Generates test options for get_minecraft_command(). Use this function to test launching without logging in. This should not be used in production.

.. code:: python

    is_version_valid(version: str,path: str) -> bool

Checks if the given version exists
