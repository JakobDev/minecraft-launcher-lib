Get Installation Progress
==========================
Installing a new Minecraft version can, depending on the internet connection, take some time. It would be nice to show the user the progress e.g. in a Progressbar.

To tell your program the current progress, minecraft-launcher-lib uses callbacks. Callbacks are just normal functions that you write and that are called by minecraft-launcher-lib. Here is a example:

.. code:: python

    import minecraft_launcher_lib


    current_max = 0


    def set_status(status: str):
        print(status)


    def set_progress(progress: int):
        if current_max != 0:
            print(f"{progress}/{current_max}")


    def set_max(new_max: int):
        global current_max
        current_max = new_max


    minecraft_directory = minecraft_launcher_lib.utils.get_minecraft_directory()

    callback = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max
    }

    minecraft_launcher_lib.install.install_minecraft_version("1.17", minecraft_directory, callback=callback)

As you can see callback is a dict with functions. The functions are defined by you. You can write in these functions whatever you want. In the example above it prints the current status to the commandline.
