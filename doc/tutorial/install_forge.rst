Install Forge
==========================
This tutorial shows how to install forge using minecraft-launcher-lib. Please note that the Forge Devs do not want automatic installations unless you donated to them.

-------------------------
Get Forge Version
-------------------------
Before you install Forge, you need to know what Forge version you need. Use :func:`~minecraft_launcher_lib.forge.find_forge_version`:

.. code:: python

    forge_version = minecraft_launcher_lib.forge.find_forge_version("1.17.1")
    if forge_version is None:
        print("This Minecraft Version is not supported by Forge")
        return

In this case we get the latest Forge version for 1.17.1.

-------------------------
Install Forge Version
-------------------------
Now we have the Forge version, so we can install it. Use :func:`~minecraft_launcher_lib.forge.install_forge_version`.

    .. code:: python

        minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_directory)

install_forge_version() supports the same callbacks as :func:`~minecraft_launcher_lib.install.install_minecraft_version`. :func:`~minecraft_launcher_lib.forge.install_forge_version` does not support very old versions.
Use :func:`~minecraft_launcher_lib.forge.supports_automatic_install` to check if your Forge version is supported by this function.

-------------------------
Launch Forge Version
-------------------------
Unfortunately, the version we got with :func:`~minecraft_launcher_lib.forge.find_forge_version` can't be used for :func:`~minecraft_launcher_lib.command.get_minecraft_command`, because forge installs it under a little different name.
Use :func:`~minecraft_launcher_lib.forge.find_forge_version` to get the right version id for the launch.
