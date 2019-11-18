command
==========================
command contains the function for creating the minecraft account.

.. code:: python

    get_command(version,path,options)

Returns the command for running minecraft as list. The given command can be executed with subprocess. utils containt a function where you can get the default minecraft directory.

options is a dict:

.. code:: python

    options = {
        #This is needed
        "username": The Username,
        "uuid": uuid of the user,
        "token": the accessToken,
        #This is optional
        "gameDirectory": The gameDirectory (default is the path given in arguments)
    }

You can use the account module to get the needed information.
