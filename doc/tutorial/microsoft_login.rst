Microsoft Login
==================================================
Login with a Microsoft Account requires a Web browser and a Azure Application.

-------------------------
Create Azure Application
-------------------------
To login with Microsoft you need to create a Azure Application first. Follow `this tutorial <https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app>`_ to create one.
You need the Clinet ID, the Secret and the redirect URL of your new Application.


-------------------------
Let the User log in
-------------------------
The login happens in a Web browser. This can be the normal Browser of the System or a Browser Widget embed in your Program. To get the url that is used for the login use minecraft_launcher_lib.microsoft_account.get_login_url(client_id: str, redirect_uri: str).
Open the URL and test if you can login. After you've logged in you will be redirected to https://<your redirect URL>?code=codegoeshere&state=<optional. codegoeshere is the code that you need. You can use minecraft_launcher_lib.microsoft_account.get_auth_code_from_url(url: str)
to get the code from the url. You can also use minecraft_launcher_lib.microsoft_account.url_contains_auth_code(url: str) to check if the given URL has a code.

-------------------------
Do the Login
-------------------------
Use minecraft_launcher_lib.microsoft_account.complete_login(client_id: str, client_secret: str, redirect_uri: str, auth_code: str) to login to Minecraftt. The auth code is the code from URL you've got in the previous step. You get this result:

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

As you can see it contains everything you need for the options dict of get_minecraft_command().

-------------------------
Refresh
-------------------------
To refresh just use minecraft_launcher_lib.microsoft_account.complete_refresh(client_id: str, client_secret: str, redirect_uri: str, refresh_token: str). The refresh token is from the function above.
If the refresh fails, it will throw a InvalidRefreshToken exception. In this case you need the user to login again.