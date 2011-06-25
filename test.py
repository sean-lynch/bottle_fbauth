import unittest
import os
import bottle
import bottle_fbauth

FACEBOOK_APP_ID     = "<Provided FB App ID>"
FACEBOOK_APP_SECRET = "<Provided FB App Secret>"

class FBAuthTest(unittest.TestCase):
    def setUp(self):
        self.app = bottle.Bottle(catchall=False)

    def test_with_keyword(self):
        self.plugin = self.app.install(bottle_fbauth.FBAuthPlugin(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET))

        @self.app.get('/')
        def test(fb_user):
            self.assertEqual(fb_user, None)
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

    def test_without_keyword(self):
        self.plugin = self.app.install(bottle_fbauth.FBAuthPlugin(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET))

        @self.app.get('/')
        def test():
            pass
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET'}, lambda x, y: None)

        @self.app.get('/2')
        def test(**kw):
            self.assertFalse('fb_user' in kw)
        self.app({'PATH_INFO':'/2', 'REQUEST_METHOD':'GET'}, lambda x, y: None)
        
if __name__ == '__main__':
    unittest.main()
