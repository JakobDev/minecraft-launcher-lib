Troubleshooting
==================================================
Here is a quick checklist for you, if Minecraft doesn't starts.

- Start the Version in the official Launcher

    At first you should try to start the Minecraft version in official Launcher. If it didn't start there, the problem is not in minecraft-launcher-lib or your code.

- Call install_minecraft_version()

    Before you start Minecraft, you should first call install_minecraft_version(). This function ensures that everything is right and installs parts if needed.
    It should even be called, if you installed a version with a installer e.g. Optifine.

- Use the subprocess module

    There are many ways to call a shell command in Python. Maybe your GUI Tooolkit brings it's own function e.g. QProcess from Qt. But nor all of them supports a list of strings.
    To make sure this is not the problem try to start the command with subproces.run(command). Do not use os.system().

- Check the Java version

    While newer versions of Minecraft has a Java runtime version in it's version.json, older versions don't have it. Some older versions requires a older Java version.
    Make sure to launch this old versions with the right Java version. Check out the command module documentation to learn how to set the Java version.

- Check your JVM Arguments

    If you use custom JVM Arguments, make sure all of them start with - and not a other char e.g. a whitespace.

If all of the steps above failed, please fill a `Bug Report <https://codeberg.org/JakobDev/minecraft-launcher-lib/issues>`_.
