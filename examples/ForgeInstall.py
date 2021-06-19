#!/usr/bin/env python3
# This example shows how to install forge using minecraft-launcher-lib
import minecraft_launcher_lib
import sys


def ask_yes_no(text: str) -> bool:
    while True:
        answer = input(text + " [y|n]")
        if answer.lower() == "y":
            return True
        elif answer.lower() == "n":
            return False
        else:
            print("Please enter y or n")


def main():
    vanilla_version = input("Select the Minecraft version for which you want to install forge:")
    # Find the latest forge version for that Minecraft version
    forge_version = minecraft_launcher_lib.forge.find_forge_version(vanilla_version)
    # Checks if a forge version exists for that version
    if forge_version is None:
        print("This Minecraft version is not supported by forge")
        sys.exit(0)
    # Checks if the version can be installed automatic
    if minecraft_launcher_lib.forge.supports_automatic_install(forge_version):
        if ask_yes_no(f"Do you want to install forge {forge_version}?"):
            minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
            callback = {
                "setStatus": lambda text: print(text)
            }
            minecraft_launcher_lib.forge.install_forge_version(forge_version, minecraft_directory, callback=callback)
    else:
        print(f"Forge {forge_version} can't be installed automatic.")
        if ask_yes_no("Do you want to run the installer?"):
            minecraft_launcher_lib.forge.run_forge_installer(forge_version)


if __name__ == "__main__":
    main()
