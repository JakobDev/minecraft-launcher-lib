#!/usr/bin/env python3
# This example shows how to install fabric using minecraft-launcher-lib
import minecraft_launcher_lib
import sys


def main():
    vanilla_version = input("Select the Minecraft version for which you want to install fabric:")
    if not minecraft_launcher_lib.fabric.is_minecraft_version_supported(vanilla_version):
        print("This version is not supported by fabric")
        sys.exit(0)
    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()
    callback = {
        "setStatus": lambda text: print(text)
    }
    minecraft_launcher_lib.fabric.install_fabric(vanilla_version, minecraft_directory, callback=callback)


if __name__ == "__main__":
    main()
