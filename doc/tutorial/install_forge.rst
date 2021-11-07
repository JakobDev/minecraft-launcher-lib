Install Forge
==========================
This tutorial shows how to install forge using minecraft-launcher-lib. Please note that the Forge Devs do not want automatic installations unless you donated to them.

-------------------------
Get Forge Version
-------------------------
Before you install Forge, you need to know what Forge version you need. Use find_forge_version():

.. code:: python

    forge_version = minecraft_launcher_lib.forge.find_forge_version("1.17.1")
    if forge_version is None:
        print("This Minecraft Version is not supported by Forge")
        return

In this case we get the latest Forge version for 1.17.1.

-------------------------
Install Forge Version
-------------------------
Now we have the Forge version, so we can install it. Use install_forge_version().

    .. code:: python

        minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_directory)

install_forge_version() supports the same callbacks as install_minecraft_version(). install_forge_version() does not support versions prior to 1.12.
Use supports_automatic_install(9 to check if your Forge version is supported by this function.

-------------------------
Launch Forge Version
-------------------------
Unfortunately, the version we got with find_forge_version() can't be used for get_minecraft_command(), because forge installs it under a little different name.
Use get_installed_versions() to get the right version id for the launch.
