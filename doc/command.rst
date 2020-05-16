command
==========================
command contains the function for creating the minecraft command.

.. code:: python

    get_minecraft_command(version,path,options)

Returns the command for running minecraft as list. The given command can be executed with subprocess. utils containt a function where you can get the default minecraft directory.

options is a dict:

.. code:: python

    options = {
        #This is needed
        "username": The Username,
        "uuid": uuid of the user,
        "token": the accessToken,
        #This is optional
        "executablePath": "java", #The path to the java executable
        "jvmArguments": [], #The jvmArguments
        "launcherName": "minecraft-launcher-lib", #The name of your launcher
        "launcherVersion": "1.0", #The version of your launcher
        "gameDirectory": "/home/user/.minecraft", #The gameDirectory (default is the path given in arguments)
        "demo": False, #Run Minecraft in demo mode
        "customResolution": False, #Enable custom resolution
        "resolutionWidth": "854", #The resolution width
        "resolutionHeight": "480", #The resolution heigth
        "server": "example.com", #The ip of a server where Minecraft connect to after start
        "port": "123", #The port of a server where Minecraft connect to after start
        "nativesDirectory": "minecraft_directory/versions/version/natives" #The natives directory
    }

You can use the account module to get the needed information.
