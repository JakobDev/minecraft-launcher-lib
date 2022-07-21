microsoft_account
==========================
microsoft_account contains functions for login with a Microsoft Account. Before using this module you need to `create a Azure application <https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app>`_.
Many thanks to wiki.vg for it's `documentation of the login process <https://wiki.vg/Microsoft_Authentication_Scheme>`_.
For a list of all types see :doc:`/modules/microsoft_types`.

.. code:: python

    get_login_url(client_id: str, redirect_uri: str) -> str

| Returns the url to the website on which the user logs in.
| For a more secure alternative, use get_secure_login_data()

.. code:: python

    get_secure_login_data(client_id: str, redirect_uri: str, state: Optional[str] = None) -> tuple[str, str, str]:

| Generates the login data for a secure login with pkce and state.
| Prevents Cross-Site Request Forgery attacks and authorization code injection attacks.
| Returns the url to the website on which the user logs in, the state and the code verifier.

.. code:: python

    url_contains_auth_code(url: str) -> bool

Checks if the given url contains a authorization code.

.. code:: python

    get_auth_code_from_url(url: str) -> Optional[str]

| Get the authorization code from the url.
| If you want to check the state, use parse_auth_code_url(), which throws errors instead of returning an optional value.
| Returns the auth code or None if the the code is nonexistent.

.. code:: python

    parse_auth_code_url(url: str, state: Optional[str]) -> str:

| Parse the authorization code url and checks the state if supplied.
| Returns the auth code

.. code:: python

    complete_login(client_id: str, client_secret: Optional[str], redirect_uri: str, auth_code: str, code_verifier: Optional[str] = None) -> CompleteLoginResponse:

Do the complete login process. It returns the following:

.. code:: json

    {
        "id" : "The uuid",
        "name" : "The username",
        "access_token": "The acces token",
        "refresh_token": "The refresh token",
        "skins" : [{
            "id" : "6a6e65e5-76dd-4c3c-a625-162924514568",
            "state" : "ACTIVE",
            "url" : "http://textures.minecraft.net/texture/1a4af718455d4aab528e7a61f86fa25e6a369d1768dcb13f7df319a713eb810b",
            "variant" : "CLASSIC",
            "alias" : "STEVE"
        } ],
        "capes" : []
    }

.. code:: python

    complete_refresh(client_id: str, client_secret: Optional[str], redirect_uri: Optional[str], refresh_token: str) -> CompleteLoginResponse:

Do the complete login process with a refresh token. It returns the same as complete_login().

.. code:: python

    get_authorization_token(client_id: str, client_secret: Optional[str], redirect_uri: str, auth_code: str, code_verifier: Optional[str]) -> AuthorizationTokenResponse:

Get the authorization token.

.. code:: python

    refresh_authorization_token(client_id: str, client_secret: Optional[str], redirect_uri: Optional[str], refresh_token: str) -> AuthorizationTokenResponse:

Refresh the authorization token.

.. code:: python

    authenticate_with_xbl(access_token: str) -> XBLResponse

Authenticate with Xbox Live.

.. code:: python

    authenticate_with_xsts(xbl_token: str) -> XSTSResponse

Authenticate with XSTS.

.. code:: python

    authenticate_with_minecraft(userhash: str, xsts_token: str) -> MinecraftAuthenticateResponse

Authenticate with Minecraft.

.. code:: python

    get_store_information(access_token: str) -> MinecraftProfileResponse

Get the store information.

.. code:: python

    get_profile(access_token: str) -> MinecraftProfileResponse

Get the profile.
