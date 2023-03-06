Codestyle
==========================
minecraft-launcher-lib uses `PEP8 <https://https://pep8.org/>`_ as it's codestyle with the following additional rules:

- Lines longer than 80 chars are allowed. We are not in the 90s anymore. Any modern screen can display way more than 80 chars per line without scrolling.
- All functions must have `type annotations <https://blog.logrocket.com/understanding-type-annotation-python/>`_
- All functions must have docstrings

-------------------------
Check the Codestyle
-------------------------
minecraft-launcher-lib uses `flake8 <https://flake8.pycqa.org>`_ along with the `flake8-annotation <https://pypi.org/project/flake8-annotations/>`_, the `flake8-docstring-checker <https://pypi.org/project/flake8-docstring-checker/>`_  plugin, and the `flake8-assert-finder <https://pypi.org/project/flake8-assert-finder/>`_  plugin to do a automatic style check. To get started, install it:

.. code::

    pip install flake8 flake8-annotation flake8-docstring-checker

To run it, open a command line in the root directory of minecraft-launcher-lib and run:

.. code::

    flake8

If it prints nothing, everything is OK. If it prints something, you should fix it.
