Automatic tests
==========================
minecraft-launcher-lib uses `Pytest <https://pytest.org>`_ to run some automatic tests.

-------------------------
Using Pytest
-------------------------
To get started, install all test dependencies

.. code:: shell

    pip install -r requirements-test.txt

To run the tests, open a command line in the root directory of minecraft-launcher-lib and execute:

.. code:: shell

    pytest

If a test fails, you should fix the bug.

-------------------------
Test Coverage
-------------------------
To see a detailed test coverage report (which lines are executed during the tests), open :code:`htmlcov/index.html` with your browser.
