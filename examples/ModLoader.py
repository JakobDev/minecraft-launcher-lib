#!/usr/bin/env python3
# This example shows how use the mod loader module
import minecraft_launcher_lib
import subprocess


def choose(options: list[str]) -> int:
    for pos, text in enumerate(options):
        print(f"{pos + 1}: {text}")

    while True:
        try:
            answer = int(input(f"Select[1-{len(options)}]:")) - 1
            if answer >= 0 and answer < len(options):
                return answer
        except ValueError:
            pass


def ask_yes_no(text: str) -> bool:
    while True:
        answer = input(f"{text}[y/n]:").strip().upper()

        if answer == "Y":
            return True
        elif answer == "N":
            return False
        else:
            print("Invalid answer. Use y or n.")


def main() -> None:
    id_list = minecraft_launcher_lib.mod_loader.list_mod_loader()

    name_list = []
    for current_id in id_list:
        name_list.append(minecraft_launcher_lib.mod_loader.get_mod_loader(current_id).get_name())

    print("Please select a mod loader:")

    loader = minecraft_launcher_lib.mod_loader.get_mod_loader(id_list[choose(name_list)])
    version_list = loader.get_minecraft_versions(True)

    print()
    print("Please select the Minecraft version for which you want to install the mod loader.")
    vanilla_version = version_list[choose(version_list)]

    print()
    minecraft_directory = input("Enter the path to your Minecraft directory (leave blank for default):").strip()
    if minecraft_directory == "":
        minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

    installed_version = loader.install(vanilla_version, minecraft_directory, callback={"setStatus": print})

    print("Finished")

    if not ask_yes_no("Do you want to launch Minecraft?"):
        return

    command = minecraft_launcher_lib.command.get_minecraft_command(installed_version, minecraft_directory, minecraft_launcher_lib.utils.generate_test_options())
    subprocess.run(command, cwd=minecraft_directory)


if __name__ == "__main__":
    main()
