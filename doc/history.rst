History
==========================
I like the Design of the old Minecraft Launcher (2013-2016), but I don't like the Design of the new one which was released in 2016, so I kept using the old one.
I was aware that the old Launcher is not going to be supported forever. There are many 3rd party launcher out there so I thought: Why not writing my own Launcher that has the same GUI as the old Launcher?
So I started developing a Launcher in Python using QtWidgets from `PyQt5 <https://pypi.org/project/PyQt5>`_. I chose Python, because it's an easy to use language.
QtWidgets also allows me to write a classical styles user interface and is cross platform as a Bonus. I finished the GUI soon. Everything except the launching was working.
I looked how t do that, but is was complicated and I run into a few problems, so I was looking for a library to do that or working Python code that supports all edge cases.
I haven't found anything that was useable, so I decided to use `mclauncher-api <https://github.com/tomsik68/mclauncher-api>`_, which is a Java library.
I wrote a small wrapper program in Java that uses the lib and was called by my Launcher.
I released it and called it `jdMinecraftLauncher <https://codeberg.org/JakobDev/jdMinecraftLauncher>`_, so it can also used by other who like the good old design.

I knew, this was not a good solution so I kept working on a Python code that can launch and install Minecraft. I was able to archive this and install and launch the latest version at this time.
I tried to use the code with older versions, but I realized that the Way how to launch Minecraft changed a bit over time. I also got this part working.
I remembered, how hard it was for me to do this, so I decided to move all the functions that could also be used by others out of jdMinecarftLauncher into a library.
I am not very creative when it comes to names, so I just called the library minecraft-launcher-lib, because it's a library for Minecraft launchers.
minecraft-launcher-lib was primarily made to meet the needs of jdMinecarftLauncher, but I designed to library in a Way that it could be used by anyone out there and with any GUI toolkit.

Version 0.1 was published on `2019-11-18 on GitLab <https://gitlab.com/JakobDev/minecraft-launcher-lib/-/tree/0.1>`_ together with a
`very minimalistic documentation <https://minecraft-launcher-lib.readthedocs.io/en/0.1>`_ and `uploaded to PyPI <https://pypi.org/project/minecraft-launcher-lib/0.1>`_.

I kept working on it and added support for more and more Versions. I also tested the library more, as it was now
`integreated in jdMinecraftLauncher <https://codeberg.org/JakobDev/jdMinecraftLauncher/commit/e5aff324ce7eb267a8cc0c7c54b40fa824885f3f#diff-b99a8f5bebd1416008741ec2ba8f26701ebc50cc>`_.
`Version 1.0 <https://pypi.org/project/minecraft-launcher-lib/1.0>`_, which finally official supports all existing Versions was released on 2020-05-16.

After that, I added functions for automatically installing Forge, which was a lot of reverse engineering, and Farbric, which is just downloading and executing the Installer.
I also improved the Documentation and added tests using `Pytest <https://pytest.org>`_.

A big change came with the introduction of Microsoft Accounts. WIth old Mojang Accounts you just needed a Username and Password to log in.
Now you need to create a Azure App before you can get started. The login also needs to be done in a Web browser. This causes a lot of Problems.

It's gotten even worse: Since 2023 you need to apply to get the Permission to use the Minecraft API. this makes it way harder for people who want to try out this library.

Another big change happened in 2023: `GitLab announces that inactive Repos will be deleted after one Year <https://www.theregister.com/2022/08/05/gitlab_reverses_deletion_policy>`_.
This was reversed later, but I felt like GitLab, which I was using since Microsoft bought GitHub, is no longer a good and safe place for my Projects.
So I looked for another Code hosting service and found `Codeberg <https://codeberg.org>`_, which is non profit hosting service for OpenSource Projects.
After GitLab was `blocking the CI for new Users <https://about.gitlab.com/blog/2021/05/17/prevent-crypto-mining-abuse>`_, I decided that it was time to ditch GitLab and moved the Repo to Codeberg.
