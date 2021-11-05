More Launch Options
==========================
minecraft-launcher-lib offers various options for launching Minecraft. This page shows the most important ones. For a full list check out the documentation of the command module.

-------------------------
JVM Arguemnts
-------------------------
JVM Arguemnts are a list of strings. Each argument is a entry in the list. Here is a example:

.. code:: python

    # Right
    options["jvmArguments"] = ["-Xmx2G", "-Xms2G"]

    # Wrong
    options["jvmArguments"] = ["-Xmx2G -Xms2G"]

    # Wrong
    options["jvmArguments"] = "-Xmx2G -Xms2G"

Make sure every argument starts with a -, otherwise Minecraft will not start with a "Could not find or load main class" error.

-------------------------
Java Executable
-------------------------
The Java Executable is the path the Java which is used to run Minecraft. If the version.json contains a Java Runtime, it minecraft-launcher-lib will download and use these version. Otherwise it will just use the java command.
minecraft-launcher-lib allows to overwrite this. This can be useful, if you want to start a older version which needs a older Java and does not contain a runtime in the version.json.

.. code:: python

    options["executablePath"] = "path/to/java"

-------------------------
Custom Resolution
-------------------------
minecraft-launcher-lib allows starting Minecraft with a custom resolution. The first thing you have to do is enable the custom resolution. After that you can set it:

.. code:: python

     # Enable custom resolution
     options["customResolution"] = True
     # Set custom resolution
     options["resolutionWidth"] = "600"
     options["resolutionHeight"] = "500"

Make sure you use strings and not int for the resolution.

-------------------------
Game Directory
-------------------------
The Game Directory is the directory where Minecraft saves all his stuff like Worlds, Resourcepacks, Options etc. By default your Minecraft Directory is used as Game Directory.

.. code:: python

     options["gameDirectory"] = "path/to/your/game/directory"

If the directory does not exists, Minecraft will create it.

-------------------------
Use Demo Mode
-------------------------
Minecraft has a build-in Demo mode, which is used, if somebody who does not bought Minecraft launches the Game through the official launcher. minecraft-launcher-lib allows you to enable the Demo mode.
You need at least Minecraft version 1.3.1 to use the Demo mode.

.. code:: python

     options["demo"] = True