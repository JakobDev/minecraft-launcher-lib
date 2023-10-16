Changelog
==================================================

-------------------------
6.3
-------------------------
- Fixed `#92 <https://codeberg.org/JakobDev/minecraft-launcher-lib/issues/92>`_
- Fixed `#93 <https://codeberg.org/JakobDev/minecraft-launcher-lib/issues/93>`_

-------------------------
6.2
-------------------------
- Fix raising InvalidChecksum exception

-------------------------
6.1
-------------------------
- Added :class:`~minecraft_launcher_lib.exceptions.AzureAppNotPermitted` exception
- Added :func:`~minecraft_launcher_lib.utils.is_minecraft_installed`
- Added callbacks to the :doc:`/modules/mrpack` module
- Fix some Bugs

-------------------------
6.0
-------------------------
- Added :doc:`/modules/vanilla_launcher` module
- Added :doc:`/modules/mrpack` module
- Added :doc:`/modules/quilt` module
- Added :func:`~minecraft_launcher_lib.runtime.get_jvm_runtime_information`
- Added :class:`~minecraft_launcher_lib.exceptions.InvalidChecksum` exception
- Remove account module (deprecated since 4.4 which was released 2022-02-16)
- Move module documentation into Code
- Change account type to msa
- Add support for Quick Play
- Add internal types
- Refactor Code

-------------------------
5.3
-------------------------
- Move minecraft-launcher-lib to Codeberg
- Add defaultExecutablePath option
- Add disableMultiplayer and disableChat options
- Change get_java_executable to use javaw.exe on Windows (`osfanbuff63 <https://gitlab.com/osfanbuff63>`_)

-------------------------
5.2
-------------------------
- Added a secure login option using pkce (get_secure_login_data)(`Manuel Quarneti <https://gitlab.com/mq-1>`_)
- Add forge_to_installed_version()
- Fix setMax callback

-------------------------
5.1
-------------------------
- Fix crash when custom clients use invalid releaseTime

-------------------------
5.0
-------------------------
- The minimum Python version is now 3.8
- All public APIs are now complety static typed (with help of `Manuel Quarneti <https://gitlab.com/mq-1>`_)
- minecraft-launcher-lib has now a py.typed file
- Installs now using requests.session for faster installing
- Add types and microsoft_types module
- Add is_platform_supported()
- Add get_installed_jvm_runtimes()
- The client secret is now optional for Microsoft Accounts
- Include release time in version list
- install_jvm_runtime() does now support symlinks
- Fix launching custom clients

-------------------------
4.6
-------------------------
- Add is_vanilla_version()
- Install version that is inherited from
- Fix command for 1.19-pre1
- Fix type annotations
- Cache requests
- Rewrite Maven parsing

-------------------------
4.5
-------------------------
- Fix Forge installation for 1.18 again (`Σcatnip <https://gitlab.com/sum-catnip>`_)

-------------------------
4.4
-------------------------
- Fix Forge installation for 1.18
- Do not use bare except
- Add DeprecationWarning to the account module

-------------------------
4.3
-------------------------
- Add get_executable_path()
- Fix using Java Runtime on Windows

-------------------------
4.2
-------------------------
- Fix launching Forge 1.17.1

-------------------------
4.1
-------------------------
- Add get_minecraft_news()
- Replace deprecated distutils.spawn.find_executable() with shutil.which()
- Add support for using a custom Java runtime in different functions (`BobDotCom <https://github.com/BobDotCom>`_)
- Fix Forge for 1.12.2
- Fix find_forge_version() (`BobDotCom <https://github.com/BobDotCom>`_)
- Packages can now be built without requests being installed (`BobDotCom <https://github.com/BobDotCom>`_)
- Fix finding Java runtime on Mac (`BobDotCom <https://github.com/BobDotCom>`_)

-------------------------
4.0
-------------------------
- Add Support for Microsoft Accounts
- All functions with a Path as Argument can now take a os.PathLike
- Fix crash in get_installed_versions() when a directory has no json file
- Fix Bug in install_forge_version()

-------------------------
3.6
-------------------------
- Fix install_forge_version() for 1.17.1

-------------------------
3.5
-------------------------
- Fix crash when logging is empty

-------------------------
3.4
-------------------------
- Add runtime module
- The runtime is now automatic installed if needed

-------------------------
3.3
-------------------------
- Add is_forge_version_valid()
- Add supports_automatic_install()
- Add UnsupportedVersion exception
- Add ExternalProgramError exception
- Add callbacks to install_fabric()
- Make install_forge_version() raise VersionNotFound exception
- Fix install_fabric()
- Better codestyle

-------------------------
3.2
-------------------------
- Use custom user agent for all requests
- Fix typo that causes crash (`DiamondsBattle <https://gitlab.com/DiamondsBattle>`_)

-------------------------
3.1
-------------------------
- Fix Bug in install_minecraft_version()

-------------------------
3.0
-------------------------
- Add fabric module
- install_minecraft_version supports now custom libraries urls
- Add VersionNotFound exception
- Add type annotations
- Add docstrings
- Add is_version_valid()
- Add generate_test_options()

-------------------------
2.1
-------------------------
- Add support for log4j configuration file
- Fix Bug with files in versions directory

-------------------------
2.0
-------------------------
- Add forge modul
- Add hash validation

-------------------------
1.4
-------------------------
- Fix downloading libraries on windows

-------------------------
1.3
-------------------------
- Fix downloading libraries without url
- Fix get_available_versions()
- Improve get_java_executable()

-------------------------
1.2
-------------------------
- Fix Typo

-------------------------
1.1
-------------------------
- Fix Forge for older versions

-------------------------
1.0
-------------------------
- Add function to extract natives
- Add functions for upload and reset a skin

-------------------------
0.5
-------------------------
- Better support for older versions
- Add new functions to utils

-------------------------
0.4
-------------------------
- The natives are now extracted
- Fix running older versions of Forge

-------------------------
0.3
-------------------------
- The classpath has now the correct seperator on windows
- Add option to set the executable path
- Add support for {arch} in natives

-------------------------
0.2
-------------------------
- Add support for Forge
- Add more options
- Add callback functions

-------------------------
0.1
-------------------------
- First Release
