natives
==========================
natives contains a function for extracting natives libraries to a specific folder.

.. code:: python

    extract_natives(versionid: str,path: Union[str, os.PathLike],extract_path: str) -> NoReturn

Extract all native libraries from a version into the given directory. The directory will be created, if it does not exist.

Note:
The natives are all extracted while installing. So you don't need to use this function in most cases.
