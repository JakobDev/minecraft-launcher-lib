Automatic tests
==========================
minecraft-launcher-lib uses `Pytest <https://pytest.org>`_ to run some automatic tests. The tests only covers the utils functions. The main things like installing, launching and logging in to Microsoft are not covered, because I don't know how to do this, if it should work in the Codeberg CI as well.

-------------------------
Using Pytest
-------------------------
To get started, install it:

.. code::

    pip install pytest

To run the tests, open a command line in the root directory of minecraft-launcher-lib and execute:

.. code::

    pytest

If a test fails, you should fix the bug.
