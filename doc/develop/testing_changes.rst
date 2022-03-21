Testing changes
==========================
While there are :doc:`automatic tests</develop/automatic_tests>` for the utils functions, the main part (installing launching and logging in into Microsoft) must be tested by yourself.

Open a command line in the root directory of minecraft-launcher-lib and open the Python Interpreter. In the Interpreter run:

.. code::

    >>> import minecraft_launcher_lib
    >>> print(minecraft_launcher_lib.__file___)

It should print the path to your current directory. After you've confirmed, that you are using the version you are currently working on, you can start testing.

Just run the functions you have changed and see, if everything worked correctly. Please test installation and launching in a clean directory and not your normal .minecraft directory.
