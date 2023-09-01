#!/usr/bin/env python3
# This example shows how to simple install and launch the latest version of Minecraft.
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
subprocess.run(minecraft_command)
