account
==========================
account contains functions for interacting with your mojang account.

.. code:: python

    login_user(username, password)

Login to your mojang account. The response contains things like accessToken, clientToken, uuid and something else.

Note:
You should never save username and password! Only the client token.

.. code:: python

    validate_access_token(username, password)

Returns true, if the accessToken is valid. Otherwise it will return false. You should check that before running minecraft.

.. code:: python

    refresh_access_token(access_token, client_token)

Get a new accessToken.

.. code:: python

    logout_user(username, password)

Log a user out.

.. code:: python

    invalidate_access_token(access_token, client_token)

Make an accessToken invalid.

.. code:: python

    upload_skin(uuid, access_token, path_to_skin.png, slim_model=False)

Upload a Skin.

.. code:: python

    reset_skin(uuid, access_token)

Reset a Skin.
