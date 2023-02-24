#!/usr/bin/env python3
# This example shows how use the mrpack module
import minecraft_launcher_lib
import subprocess
import sys
import os


def ask_yes_no(text: str) -> bool:
    while True:
        answer = input(f"{text} [Y/N]: ").strip().upper()

        if answer == "Y":
            return True
        elif answer == "N":
            return False
        else:
            print("Invalid answer. Use Y or N.")


def main() -> None:
    mrpack_path = input("Please enter the Path to your .mrpack File: ")

    if not os.path.isfile(mrpack_path):
        print(f"{mrpack_path} was not found", file=sys.stderr)
        sys.exit(1)

    try:
        mrpack_information = minecraft_launcher_lib.mrpack.get_mrpack_information(mrpack_path)
    except Exception:
        print(f"{mrpack_path} is not a valid .mrpack File")
        sys.exit(1)

    # Print some Information
    print("You have selected the following Pack:")
    print("Name: " + mrpack_information["name"])
    print("Summary: " + mrpack_information["summary"])
    print("Minecraft version: " + mrpack_information["minecraftVersion"])

    if not ask_yes_no("Do you want to install this Pack?"):
        return

    # Ask the User for the Directories
    minecraft_directory = input("Please enter the Path to your Minecraft directory (leave empty for default): ")

    if minecraft_directory == "":
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

    modpack_directory = input("Please enter the Path to the Directory you want to install the Modpack (leave empty for your Minecraft directory): ")

    if modpack_directory == "":
        modpack_directory = minecraft_directory

    # Adds the Optional Files
    mrpack_install_options: minecraft_launcher_lib.types.MrpackInstallOptions = {"optionalFiles": []}
    for i in mrpack_information["optionalFiles"]:
        if ask_yes_no(f"The Pack includes the Optional File {i}. Do you want to install it?"):
            mrpack_install_options["optionalFiles"].append(i)

    # Install
    print("Installing")
    minecraft_launcher_lib.mrpack.install_mrpack(mrpack_path, minecraft_directory, modpack_directory=modpack_directory, mrpack_install_options=mrpack_install_options, callback={"setStatus": print})
    print("Finished")

    if not ask_yes_no("Do you want to start Minecraft?"):
        return

    # We skip the Login in this Example
    options = minecraft_launcher_lib.utils.generate_test_options()
    options["gameDirectory"] = modpack_directory
    command = minecraft_launcher_lib.command.get_minecraft_command(minecraft_launcher_lib.mrpack.get_mrpack_launch_version(mrpack_path), minecraft_directory, options)
    subprocess.run(command)


if __name__ == "__main__":
    main()
