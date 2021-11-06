# minecraft-launcher-lib

A Python library for creating a custom minecraft launcher. This library containts functions to install and execute minecraft and interacting with mojang accounts.

```python
import minecraft_launcher_lib
import subprocess
import sys

# Set the data for your Azure Application here. For more information look at the documentation.
CLIENT_ID = "YOUR CLIENT ID"
SECRET = "YOUR SECRET"
REDIRECT_URL = "YOUR REDIRECT URL"

# Get latest version
latest_version = minecraft_launcher_lib.utils.get_latest_version()["release"]

# Get Minecraft directory
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

# Make sure, the latest version of Minecraft is installed
minecraft_launcher_lib.install.install_minecraft_version(latest_version, minecraft_directory)

# Login
print(f"Please open {minecraft_launcher_lib.microsoft_account.get_login_url(CLIENT_ID, REDIRECT_URL)} in your browser and copy the url you are redirected into the prompt below.")
code_url = input()

# Check if the url contains a code
if not minecraft_launcher_lib.microsoft_account.url_contains_auth_code(code_url):
    print("The url is not valid")
    sys.exit(1)

# Get the code from the url
auth_code = minecraft_launcher_lib.microsoft_account.get_auth_code_from_url(code_url)

# Get the login data
login_data = minecraft_launcher_lib.microsoft_account.complete_login(CLIENT_ID, SECRET, REDIRECT_URL, auth_code)

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
- Support Forge, Fabric and Liteloader
- Old versions like alpha or beta supported
- All functions have type annotations and docstrings
- Only depents on [requests](https://pypi.org/project/requests)
- Supports [PyPy](https://www.pypy.org)
- Full Documention with tutorial online available
- Examples available
- OpenSource

[View more examples](https://gitlab.com/JakobDev/minecraft-launcher-lib/-/tree/master/examples)

[Read the documentation](https://minecraft-launcher-lib.readthedocs.io/en/latest/index.html)

[Thanks to tomsik68 who documented how a minecraft launcher works](https://github.com/tomsik68/mclauncher-api/wiki)
