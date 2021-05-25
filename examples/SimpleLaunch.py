#!/usr/bin/env python3
# This example shows how to simple install and launch the latest version of Minecraft.
import minecraft_launcher_lib
import subprocess

# Get latest version
latest_version = minecraft_launcher_lib.utils.get_latest_version()["release"]

# Get Minecraft directory
minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

# Make sure, the latest version of Minecraft is installed
minecraft_launcher_lib.install.install_minecraft_version(latest_version, minecraft_directory)

# Login
login_data = minecraft_launcher_lib.account.login_user("JohnDoe", "secret")

# Get Minecraft command
options = {
    "username": login_data["selectedProfile"]["name"],
    "uuid": login_data["selectedProfile"]["id"],
    "token": login_data["accessToken"]
}
minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(latest_version, minecraft_directory, options)

# Start Minecraft
subprocess.call(minecraft_command)
