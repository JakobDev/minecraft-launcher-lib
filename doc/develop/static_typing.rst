Static typing
==========================
minecraft-launcher-lib uses `mypy <https://www.mypy-lang.org/>`_ to enforce static typing.

-------------------------
Using mypy
-------------------------
To get started, install mypy together with requests and the types for requests:

.. code::

    pip install requests types-requests mypy

To run mypy open a command line in the root directory of minecraft-launcher-lib and execute:

.. code::

    mypy minecraft_launcher_lib

If mypy shows a error,or, you should fix it.
