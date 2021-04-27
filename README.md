# minecraft-launcher-lib

A Python library for creating a custom minecraft launcher. This library containts functions to install and execute minecraft and interacting with mojang accounts.

```python
import minecraft_launcher_lib
import subprocess

#Get latest version
latest_version = minecraft_launcher_lib.utils.get_latest_version()["release"]

#Get Minecraft directory
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

#Make sure, the latest version of Minecraft is installed
minecraft_launcher_lib.install.install_minecraft_version(latest_version,minecraft_directory)

#Login
login_data = minecraft_launcher_lib.account.login_user("JohnDoe","secret")

#Get Minecraft command
options = {
    "username": login_data["selectedProfile"]["name"],
    "uuid": login_data["selectedProfile"]["id"],
    "token": login_data["accessToken"]
}
minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(latest_version,minecraft_directory,options)

#Start Minecraft
subprocess.call(minecraft_command)
```

Features:
- Easy installing
- Get command to run Minecraft
- Login to Mojang account
- Support Forge, Fabric and Liteloader
- Old versions like alpha or beta supported
- All functions have type annotations and docstrings
- Full Documention online available
- Examples available
- OpenSource

[View more examples](https://gitlab.com/JakobDev/minecraft-launcher-lib/-/tree/master/examples)

[Read the documentation](https://minecraft-launcher-lib.readthedocs.io/en/latest/index.html)

[Thanks to tomsik68 who documented how a minecraft launcher works](https://github.com/tomsik68/mclauncher-api/wiki)
