account
==========================

.. warning::

    Minecraft has moved to Microsoft Accounts, so this module is now deprecated

account contains functions for interacting with your mojang account.

.. code:: python

    login_user(username: str, password: str) -> Dict[str,Any]

Login to your mojang account. The response contains things like accessToken, clientToken, uuid and something else.

Note:
You should never save username and password! Only the client token.

.. code:: python

    validate_access_token(access_token: str) -> bool

Returns true, if the accessToken is valid. Otherwise it will return false. You should check that before running minecraft.

.. code:: python

    refresh_access_token(access_token: str, client_token: str) -> Dict[str,Any]

Get a new accessToken.

.. code:: python

    logout_user(username: str, password: str) -> bool

Log a user out.

.. code:: python

    invalidate_access_token(access_token: str, client_token: str) -> Any

Make an accessToken invalid.

.. code:: python

    upload_skin(uuid: str, access_token: str, path: str, slim: bool=False) -> Any

Upload a Skin.

.. code:: python

    reset_skin(uuid: str, access_token: str) -> Any

Reset a Skin.
