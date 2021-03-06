=====================
bottle_fbauth
=====================

This plugin simplifies the use of Facebook's JavaScript SDK authentication in
Bottle applications. Once installed, it will check for a logged in Facebook
user cookie and pass it to a bottle app's @routes if they have a ``fb_user`` 
keyword argument (configurable).

You will also need to download the Facebook Python SDK and include facebook.py
in your sys.path for to use this plugin. Facebook has abandoned their official
Python SDK but there is a community supported fork that is up to date available
for download here:
     
    https://github.com/pythonforfacebook/facebook-sdk

As mentioned, you'll use this in conjunction Facebook's JavaScript SDK which
is available here:

    https://github.com/facebook/facebook-js-sdk
        
For more information on how to use the cookie to retrieve information from
the Facebook GraphAPI, see the Python SDK's examples:

    https://github.com/facebook/python-sdk/tree/master/examples/appengine


Installation
===============

Download the latest version from github::

    $ git clone git://github.com/sean-lynch/bottle_fbauth.git
    
Usage
===============
 
Simply adding a ``fb_user`` keyword argument (or a custom value) will enable
the FBAuth plugin on the @route. When the keyword is detected, the plugin 
determines if a Facebook user is logged in (using the Facebook cookie) and 
passes the user's cookie as the ``fb_user`` keyword's value.
 
The plug-in will only attempt to authenticate a user if the keyword is 
present. The developer can control the behavior of the application when user is
not logged in by checking if `fb_user` is None, or by specifying 
fail_without_user=True when installing the plugin to have it automatically send 
abort(401, ...). The cookie can be used in conjunction with the Facebook API to
get user information. Alternatively, you can specify a user_resolver method 
during set which will be called to create a user object of your choice.

Example installation
::
    import bottle
    import bottle_fbauth

    FACEBOOK_APP_ID     = "..."
    FACEBOOK_APP_SECRET = "..."

    app = bottle.Bottle()
    plugin = bottle_fbauth.FBAuthPlugin(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
    app.install(plugin)

    @bottle.route('/home')
    def home(fb_user):
        if fb_user:
            return template('home', user=fb_user)
        return bottle.abort(401, "User not logged in")

Configuration
=============

The following configuration options exist for the plugin class:

* **fb_app_id**: The App ID provided by Facebook for your application
  (required).
* **fb_app_secret**: The App Secret provided by Facebook for your application
  (required).
* **user_resolver**: A callback which is used to resolve the FB cookie into a
  user object of your choosing. If None is specified, the cookie is returned
  directly to the @route (default: None).
* **fail_without_user**: If True, the plugin will call abort(401, ...) 
  automatically if no user is logged in (default: False)
* **user_override**: For testing purposes, you can provide a fixed user object
  to return instead of doing authentication (default: None)
* **keyword**: The keyword argument name that triggers the plugin (default: 'fb_auth').

You can override each of these values on a per-route basis:: 

    @bottle.route('/cache/:item', fbauth={'keyword': 'user'})
    def cache(item, user):
        ...


