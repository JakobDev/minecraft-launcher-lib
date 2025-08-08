Install a mod loader
==========================
minecraft-launcher-lib allows you to install a mod loader for Minecraft using the :mod:`~minecraft_launcher_lib.mod_loader` module.
Currently the following loader are supported:

- `Forge <https://minecraftforge.net>`_
- `NeoForge <https://neoforged.net>`_
- `Fabric <https://fabricmc.net>`_
- `Quilt <https://quiltmc.org>`_

To install a mod loader, minecraft-launcher-lib provides the mod loader module, which has a unified way of installing.

Fist you need to get the loader by it's id. Valid ID's are :code:`forge`, :code:`neoforge`, :code:`fabric` and :code:`quilt`.

In this exmaple, we want to install fabric. So let's get fabric.

    .. code:: python

        fabric =  minecraft_launcher_lib.mod_loader.get_mod_loader("fabric")

Now we can install fabric for version 1.21.

    .. code:: python

        fabric.install("1.21", minecraft_directory)


You can also take a look at the :doc:`complete example </examples/ModLoader>`.
