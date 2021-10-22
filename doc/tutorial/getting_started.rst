Getting Started
==================================================
This first chapter of the documentation shows how to install and run Minecraft. The login with Microsoft is skipped here.

-------------------------
Minecraft Directory
-------------------------
To get started with minecraft-launcher-lib, you need a Minecraft Directory first. You can use a new directory or the default Directory of Minecraft. You can get the default Directory with minecraft_launcher_lib.utils.get_minecraft_directory().

.. code:: python

    # Get the Minecraft Directory of your System
    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
    # Or use your own
    minecraft_directory = "path/to/your/minecraft/directory"

-------------------------
Install Minecraft
-------------------------
Before you can launch launch Minecraft, you need to install it. This can be done by using install_minecraft_version. Let's say we want to install Version 1.17 in our Minecraft Directory.

.. code:: python

    minecraft_launcher_lib.install.install_minecraft_version("1.17", minecraft_directory)

To get the information how to install Minecraft, minecraft-launcher-lib looks first for a JSON file in your Minecraft Directory. In the case of 1.17 it's minecraft_directory/versions/1.17/1.17.json. This allows installing moded versions that are not official from Mojang.
If the JSON file not does exists minecraft-launcher-lib tries to download it from the Mojang Servers. install_minecraft_version ensures that the Minecraft installation is correct, so you need to call it every time before you launch Minecraft, even if you had the version already installed.

-------------------------
Get Minecraft Versions
-------------------------
If you don't want to start a single version like 1.17 every time you need a list of all Minecraft version. To get that list use minecraft_launcher_lib.utils.get_available_versions(minecraft_directory). It returns this list:

.. code:: python

    [
        {
            "id": "some_id",
            "type": "release"
        },
        {
            "id": "some_other_id",
            "type": "snapshot"
        }
    ]

The id is the Minecraft version that can be used as argument for install_minecraft_version and other versions. The type says what type the version is. Possible values are: release, snapshot, beta, alpha.

To get the latest version, use get_latest_version().

.. code:: python

    latest_release = minecraft_launcher_lib.utils.get_latest_version()["release"]
    latest_snapshot = minecraft_launcher_lib.utils.get_latest_version()["snapshot"]

-------------------------
Launch Minecraft
-------------------------
Since you know how to install Minecraft, it's now time to start it. First we need a dict with all options. The minimal options dict is this:

.. code:: python

    {
        "username": "The Username",
        "uuid": "The UUID",
        "token": "The acces token"
    }

The Username and UUID belongs to a Account. Since Name and UUID are public, the Token is used to log in. The token is generated every time when a User logs in with his Microsoft Account. Minecraft can be launched with a not existing user and a wrong token. This can be used for test cases. minecraft-launcher-lib allows creating a dict with a test user.

.. code:: python

    options = minecraft_launcher_lib.utils.generate_test_options()

We use the test options here to keep it simple. The login with Microsoft comes latter. Keep in mind that publishing a Launcher which allows User who haven't bought Minecraft to play is illegal, so use this only for test cases in development. You can add more options to the dict like the resolution, but this is not needed to launch.

Now we have the options, we need to get the Minecraft command. In this case for Version 1.17.

.. code:: python

    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command("1.17", minecraft_directory, options)

The command that your get is a list of strings that can be used to run Minecraft e.g. with the subprocess module.