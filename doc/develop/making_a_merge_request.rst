Making a Merge Request
==========================
minecraft-launcher-lib uses GitLab as development platform. If you want to contribute some changes, a need to make a Merge Request (MR) against the `GitLab repo of minecraft-launcher-lib <https://gitlab.com/JakobDev/minecraft-launcher-lib>`_.
A merge request is the same as a Pull Request on GitHub, which I think you should familiar with. It's works exactly the same way.

Before making a MR, you should follow this checklist:

- minecraft-launcher-lib currently targets version 3.8 of Python and the latest version of `PyPy <https://www.pypy.org/>`_. Make sure, you don't use features that were added in a newer Python version.
- Your code should work on Linux, Mac and Windows
- Please make sure, you follow the :doc:`/develop/codestyle`
- If possible, you should not break existing code that uses minecraft-launcher-lib
- If you can write a test, for your changes, you should do it
- You should update the :doc:`documentation</develop/build_and_edit_documentation>` with your changes
- Please don't add extra dependencies if not absolutely needed

After you've created a PR, flake8 and Pytest with all supported versions (including PyPy) will run. If one of those fails, GitLab will show it on the Website and you will get a mail.

Read the Docs is configured to build the documentation for each MR. Unfortunately, it will not provide a link or any hint, if the build was successful. You will have to visit `this site <https://readthedocs.org/projects/minecraft-launcher-lib/builds>`_ and search for your MR.

I'm looking forward to see your contribution and thanks in advance!
