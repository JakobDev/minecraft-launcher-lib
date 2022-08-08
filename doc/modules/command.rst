command
==========================
command contains the function for creating the minecraft command.

.. code:: python

    get_minecraft_command(version: str, minecraft_directory: Union[str, os.PathLike], options: MinecraftOptions) -> List[str]

Returns the command for running minecraft as list. The given command can be executed with subprocess. utils contains a function to get the default minecraft directory.

options is a dict:

.. code:: python

    options = {
        #This is needed
        "username": The Username,
        "uuid": uuid of the user,
        "token": the accessToken,
        #This is optional
        "executablePath": "java", # The path to the java executable
        "defaultExecutablePath": "java", # The path to the java executable if the version.json has none
        "jvmArguments": [], #The jvmArguments
        "launcherName": "minecraft-launcher-lib", # The name of your launcher
        "launcherVersion": "1.0", # The version of your launcher
        "gameDirectory": "/home/user/.minecraft", # The gameDirectory (default is the path given in arguments)
        "demo": False, # Run Minecraft in demo mode
        "customResolution": False, # Enable custom resolution
        "resolutionWidth": "854", # The resolution width
        "resolutionHeight": "480", # The resolution heigth
        "server": "example.com", # The ip of a server where Minecraft connect to after start
        "port": "123", # The port of a server where Minecraft connect to after start
        "nativesDirectory": "minecraft_directory/versions/version/natives", # The natives directory
        "enableLoggingConfig": False, # Enable use of the log4j configuration file
        "disableMultiplayer": False, # Disables the multiplayer
        "disableChat": False # Disables the chat
    }

You can use the account module to get the needed information.
For more information about the options take a look at the :doc:`/tutorial/more_launch_options` tutorial.
