Introduction
==========================

-------------------------
What's this?
-------------------------
minecraft-launcher-lib is (as the Name might suggest) a Python library for creating a custom Minecraft launcher.
It allows you to easily install and launch Minecraft without needing to know technical details.
It also included functions for some optional things you may want to have e.g. Installing modloaders like Forge/Fabric/Quilt or installing Modpacks.
Many different things are included, so you can write a Launcher that fit's exactly your needs.

- You want a simple script that just launches the latest Minecraft version? No problem!
- You want to play a Modpack with your friends, but they have problems installing it? Just create a custom launcher using minecraft-launcher-lib that installs Minecraft together with the Modpack and automatically connects to your server.
- You want to create a branded Launcher for your Modpack, to make sure it everyone can install it? With minecraft-launcher-lib you can do this easily!

-------------------------
Goals
-------------------------
These are the main goals of minecraft-launcher-lib:

- minecraft-launcher-lib can launch any version out there. If the official Launcher can launch it, minecraft-launcher-lib can launch it too!
- minecraft-launcher-lib installs and launches the Game, but never patches it.
- minecraft-launcher-lib works on every Operating System and architecture that is supported by Minecraft.
- minecraft-launcher-lib is written in pure. It only depends on requests for the Network. No big dependency tree is used.
- minecraft-launcher-lib should stay backwards compatible. This is not always possible because of changes on the side of Mojang/Microsoft e.g. the switch from Mojang to Microsoft accounts,
  but if minecraft-launcher-lib is not forced, it should never break backwards compatibility. A program that is written using an older version should also work on the latest version without changes.
  To ensure this, minecraft-launcher-lib has a test coverage of over 95%.
- minecraft-laucnher-lib is fully static typed. It helps you develop with an IDE and you can use type checkers like `mypy <https://www.mypy-lang.org/>`_.

-------------------------
Getting Started
-------------------------
This documentation contains a tutorial. You should start with the :doc:`/tutorial/getting_started` tutorial.
You can also take a look at the :doc:`/modules/index` documentation which contains the full public API.
There are also :doc:`/examples/index` which shows how to use minecraft-launcher-lib in real code.
If you want to see full programs which are using minecraft-launcher-lib, you can visit the :doc:`/showcase`.
