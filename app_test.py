import os
import unittest

os.environ['SIMULATE_HARDWARE'] = '1'
os.environ['LOCK_SETTINGS_PATH'] = 'test-settings'

import db
from app import app

primary_pin = '1234'
sub_pin = '0000'


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        db.init()
        db.shelf.clear()

    def tearDown(self):
        db.shelf.close()

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'Login' in rv.data

    def test_login_logout(self):
        rv = self.login('1234')
        assert b'Profile' in rv.data
        rv = self.logout()
        assert b'Login' in rv.data
        rv = self.login('1111')
        assert b'PIN Invalid' in rv.data

    def test_primary_lock_unlock(self):
        self.login(primary_pin)
        rv = self.app.post('/lock', follow_redirects=True)
        assert b'Box has been locked for' in rv.data
        rv = self.app.post('/unlock', follow_redirects=True)
        assert b'Box is unlocked' in rv.data

    def test_sub_lock_unlock(self):
        self.login(sub_pin)
        rv = self.app.post('/lock', follow_redirects=True)
        assert b'Box has been locked for' in rv.data
        rv = self.app.post('/unlock', follow_redirects=True)
        assert b'Box is unlocked' in rv.data

    def test_primary_lock_and_sub_cant_unlock(self):
        self.login(primary_pin)
        self.app.post('/lock', follow_redirects=True)
        self.logout()

        self.login(sub_pin)
        rv = self.app.post('/lock', follow_redirects=True)
        assert b'Already locked' in rv.data
        rv = self.app.post('/unlock', follow_redirects=True)
        # still locked
        assert b'Box has been locked for' in rv.data

    def login(self, pin):
        return self.app.post('/',
                             data={'inputPassword': pin},
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
