Microsoft Login
==================================================
Login with a Microsoft Account requires a Web browser and a Azure Application.

-------------------------
Create Azure Application
-------------------------
To login with Microsoft you need to create a Azure Application first. Follow `this tutorial <https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app>`_ to create one.
You need the Client ID, the Secret and the redirect URL of your new Application.

-------------------------
Apply for Permission
-------------------------
As stated `here <https://help.minecraft.net/hc/en-us/articles/16254801392141p>`_, new created Azure Apps need to apply for Permission using `this Form <https://aka.ms/mce-reviewappid>`_ before they can use the Minecraft API.
Apps that have been created before this change keeps working without a chance.
:func:`~minecraft_launcher_lib.microsoft_account.complete_login` will raise a :class:`~minecraft_launcher_lib.exceptions.AzureAppNotPermitted` Exception if your App don't have the Permission to use the Minecraft API.
If you get any other Exception, that probably means something else with your Azure App is not right.

-------------------------
Let the User log in
-------------------------
The login happens in a Web browser. This can be the normal Browser of the System or a Browser Widget embed in your Program. To get the url that is used for the login use minecraft_launcher_lib.microsoft_account.get_login_url(client_id: str, redirect_uri: str).
Open the URL and test if you can login. After you've logged in you will be redirected to :code:`https://<your redirect URL>?code=codegoeshere&state=<optional`. :code:`codegoeshere` is the code that you need.
You can use :code:`minecraft_launcher_lib.microsoft_account.get_auth_code_from_url(url: str)`
to get the code from the url. You can also use :code:`minecraft_launcher_lib.microsoft_account.url_contains_auth_code(url: str)` to check if the given URL has a code.

-------------------------
Secure option
-------------------------
The :code:`minecraft_launcher_lib.microsoft_account.get_secure_login_data(client_id: str, redirect_uri: str, state: str = _generate_state())` generates the login data for a secure login with pkce and state to prevent Cross-Site Request Forgery attacks and authorization code injection attacks.
This is the recommended way to login.
You can parse the auth code and verify the state with :code:`minecraft_launcher_lib.microsoft_account.parse_auth_code_url(url: str, state: str)`

-------------------------
Do the Login
-------------------------
Use :code:`minecraft_launcher_lib.microsoft_account.complete_login(client_id: str, redirect_uri: str, auth_code: str, code_verifier: Optional[str])` to login to Minecraft.
The auth code is the code from URL you've got in the previous step.
The code verifier is the code verifier you've got if you used the secure login method.
You get this result:

.. code:: json

    {
        "id" : "The uuid",
        "name" : "The username",
        "access_token": "The access token",
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

As you can see it contains everything you need for the options dict of :func:`~minecraft_launcher_lib.command.get_minecraft_command`.

-------------------------
Refresh
-------------------------
To refresh just use :code:`minecraft_launcher_lib.microsoft_account.complete_refresh(client_id: str, refresh_token: str)`. The refresh token is from the function above.
If the refresh fails, it will throw a InvalidRefreshToken exception. In this case you need the user to login again.
