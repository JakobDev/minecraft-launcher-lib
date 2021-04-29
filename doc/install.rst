install
==========================
install allows you to install minecraft.

.. code:: python

    install_minecraft_version(versionid: str,path: str,callback: Dict[str,Callable]=None)

Installs a minecraft version into the given path. e.g. install_version("1.14","/tmp/minecraft"). utils contains a function to get the default minecraft directory.

callback is a dict with functions that are called with arguments to get the progress. You can use it to show the progress to the user.

.. code:: python

    callback = {
        "setStatus": some_function, #This function is called to set a text
        "setProgress" some_function, #This function is called to set the progress.
        "setMax": some_function, #This function is called to set to max progress.
    }

Files that are already exists will not be replaced.
