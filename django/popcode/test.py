import unittest
from .DB import MGC
from django.test import Client


class Tester(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    # Test if the database is connected
    def test_DBConnected(self):
        try:
            MGC.server_info()
        except Exception as e:
            print(e)
            self.fail("DB connection failed")

    # Test if / is accessible
    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # Test if /login is accessible
    def test_login(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

    # Test if /signup is accessible
    def test_signup(self):
        response = self.client.get("/signup")
        self.assertEqual(response.status_code, 200)

    # Test if /api/logout is accessible and clear session token and username
    def test_logout(self):
        self.client.session["username"] = "test"
        self.client.session["token"] = "test"
        self.client.session.save()
        response = self.client.get("/api/logout")
        self.assertEqual(response.status_code, 302)
        self.assertTrue("username" not in self.client.session)
        self.assertTrue("token" not in self.client.session)
