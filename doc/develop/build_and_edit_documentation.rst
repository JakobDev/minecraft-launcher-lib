Build and edit documentation
==================================================
minecraft-launcher-lib uses `Sphinx <https://www.sphinx-doc.org>`_ for it's documentation. The documentation is hosted on `Read the Docs <https://readthedocs.org/>`_.
You can find the source files for the documentation in :repolink:`doc folder <doc>`.

-------------------------
Plugins
-------------------------
minecraft-launcher-lib uses the following Sphinx plugins:

- `sphinx-reredirects <https://pypi.org/project/sphinx-reredirects>`_: The module documentation has been moved in the modules directory. This Plugin creates redirects, so older links will still work.
- `sphinx-notfound-page <https://pypi.org/project/sphinx-notfound-page>`_: Used for setting the custom 404 page.
- `sphinx-rtd-dark-mode <https://pypi.org/project/sphinx-rtd-dark-mode>`_: Provides the dark theme, that you can turn on by clicking on the button in the bottom right corner.
- `sphinx-copybutton <https://pypi.org/project/sphinx-copybutton>`_: Provides the copy button on the code blocks
- `sphinxext-opengraph <https://pypi.org/project/sphinxext-opengraph>`_: Generates `Open Graph metadata <https://ogp.me/>`_

These plugins are all completely optional. You can build the documentation without having these plugins installed. The features, that the plugins provide are missing in that case.

-------------------------
Building
-------------------------
First you need to install Sphinx and the Read the Docs theme:

.. code::

    pip install sphinx sphinx-rtd-theme

You can also install the plugins, if you want to e.g. test the dark mode.

To build the documentation open a command line in the doc folder and run:

.. code::

    # Unix based Systems
    make html
    # Windows
    .\make.bat html

Now you can view the documentation by opening _build/html/index.html in your favorite browser.

-------------------------
Examples
-------------------------
The examples are stored in the :repolink:`examples folder <examples>`. They are added to the documentation during build. Please do not edit anything inside doc/examples. All files in this folder are overwritten during the build.
