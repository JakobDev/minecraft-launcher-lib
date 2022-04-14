fabric
==========================
fabric contains functions for dealing with the fabric modloader

.. code:: python

    install_fabric(minecraft_version: str, minecraft_directory: Union[str, os.PathLike], loader_version: str = None, callback: Dict[str, Callable] = None, java: str = None) -> None

Installs the fabric modloader. path is the path to your Minecraft directory. minecraft_version is a vanilla version that is supported by fabric. loader_version is the loader version. If not given it will use the latest. callback is the same dict as in the install module. java is a path to a java runtime to execute with.

.. code:: python

    get_all_minecraft_versions() -> List[Dict[str,Union[str,bool]]]

Returns all available Minecraft Versions for fabric

.. code:: python

    get_stable_minecraft_versions() -> List[str]

Returns a list which only contains the stable Minecraft versions that supports fabric

.. code:: python

    get_latest_minecraft_version() -> str

Returns the latest unstable Minecraft versions that supports fabric. This could be a snapshot.

.. code:: python

    get_latest_stable_minecraft_version() -> str

Returns the latest stable Minecraft version that supports fabric

.. code:: python

    is_minecraft_version_supported(version: str) -> bool

Checks if a Minecraft version supported by fabric

.. code:: python

    get_all_loader_versions() ->  List[Dict[str,Union[str,bool,int]]]

Returns all loader versions

.. code:: python

    get_latest_loader_version() -> str

Get the latest loader version

.. code:: python

    get_latest_installer_version() -> str

Returns the latest installer version
