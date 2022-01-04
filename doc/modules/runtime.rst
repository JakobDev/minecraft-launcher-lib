runtime
==========================
runtime allows to install the java runtime. This module is used by install_minecraft_version(), so you don't need to use it in your code most of the time.

.. code:: python

     install_jvm_runtime(jvm_version: str, minecraft_directory: Union[str, os.PathLike], callback: Dict[str, Callable] = None) -> NoReturn

Installs the given jvm runtime.  callback is the same dict as in the install module.

.. code:: python

    get_jvm_runtimes() -> List[str]

Returns a list of all available runtimes.

.. code:: python

    get_executable_path(jvm_version: str, minecraft_directory: Union[str, os.PathLike]) -> Optional[str]

Returns the path to the executable. Returns None if none is found.
