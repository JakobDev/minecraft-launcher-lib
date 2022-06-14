Custom Types
==========================
You will see types like e.g MinecraftOptions or MinecraftVersionInfo. They are defined in :doc:`/modules/types` and :doc:`/modules/microsoft_types`.
They are all normal Dicts. Let's take a look at MinecraftVersionInfo:

.. code:: python

    class MinecraftVersionInfo(TypedDict):
        id: str
        type: str
        releaseTime: datetime.datetime

It means the following: This function returns a Dict with these keys:

- id: A string
- type: A string
- releaseTime: A datetime.datetime

This type definition is just there to help your IDE. The function itself returns just a normal Dict.

.. code:: python

    version_list = minecraft_launcher_lib.utils.get_version_list()
    print(version_list[0]["id"])

    print(type(version_list[0]))
    # <class 'dict'>

As said above, it is there to help your IDE. When the function definition just say, that it returns a Dict, your IDE will not know what the Dict contains.
But when using a TypedDict, your IDE, will exactly know what the Dict contains and can offer your better autocompletion and a better type checking.

You can even use it when you are calling a function:

.. code:: python

    import minecraft_launcher_lib

    options: minecraft_launcher_lib.types.MinecraftOptions = {}
    options["username"] = "Test123"

When using a IDE, you will see that it will start autocompleting the keys of the Dict while writing.

For more information about TypedDict see `PEP 589 <https://peps.python.org/pep-0589/>`_.
