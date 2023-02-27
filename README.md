# minecraft-launcher-lib

![PyPI](https://img.shields.io/pypi/v/minecraft-launcher-lib)
![PyPI - Downloads](https://img.shields.io/pypi/dm/minecraft-launcher-lib)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/minecraft-launcher-lib)
![PyPI - License](https://img.shields.io/pypi/l/minecraft-launcher-lib)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/minecraft-launcher-lib)
![Read the Docs](https://img.shields.io/readthedocs/minecraft-launcher-lib)

A Python library for creating a custom minecraft launcher. This library containts functions to install and execute minecraft and interacting with mojang accounts.

```python
import minecraft_launcher_lib
import subprocess
import sys

# Set the data for your Azure Application here. For more information look at the documentation.
CLIENT_ID = "YOUR CLIENT ID"
REDIRECT_URL = "YOUR REDIRECT URL"

# Get latest version
latest_version = minecraft_launcher_lib.utils.get_latest_version()["release"]

# Get Minecraft directory
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

# Make sure, the latest version of Minecraft is installed
minecraft_launcher_lib.install.install_minecraft_version(latest_version, minecraft_directory)

# Login
login_url, state, code_verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(CLIENT_ID, REDIRECT_URL)
print(f"Please open {login_url} in your browser and copy the url you are redirected into the prompt below.")
code_url = input()

# Get the code from the url
try:
    auth_code = minecraft_launcher_lib.microsoft_account.parse_auth_code_url(code_url, state)
except AssertionError:
    print("States do not match!")
    sys.exit(1)
except KeyError:
    print("Url not valid")
    sys.exit(1)

# Get the login data
login_data = minecraft_launcher_lib.microsoft_account.complete_login(CLIENT_ID, None, REDIRECT_URL, auth_code, code_verifier)

# Get Minecraft command
options = {
    "username": login_data["name"],
    "uuid": login_data["id"],
    "token": login_data["access_token"]
}
minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(latest_version, minecraft_directory, options)

# Start Minecraft
subprocess.call(minecraft_command)
```

Features:
- Easy installing
- Get command to run Minecraft
- Login to Microsoft account
- Supports [Forge](https://minecraftforge.net), [Fabric](https://fabricmc.net), [Quilt](https://quiltmc.org) and Liteloader
- Old versions like alpha or beta supported
- All functions have type annotations and docstrings
- Only depents on [requests](https://pypi.org/project/requests)
- Supports [PyPy](https://www.pypy.org)
- Full Documention with tutorial online available
- Supports reading and writing profiles of the Vanilla Launcher
- Install of [mrpack modpacks](https://docs.modrinth.com/docs/modpacks/format_definition)
- All public APIs are static typed
- Examples available
- OpenSource

[View more examples](https://codeberg.org/JakobDev/minecraft-launcher-lib/src/branch/master/examples)

[Read the documentation](https://minecraft-launcher-lib.readthedocs.io)

[Thanks to tomsik68 who documented how a minecraft launcher works](https://github.com/tomsik68/mclauncher-api/wiki)

[Buy me a coffe](https://ko-fi.com/jakobdev)
