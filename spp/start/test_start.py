import unittest
from spp import create_app

from spp import db, test_parent
from spp.models import User

from flask_login import current_user, logout_user


class PrimaryTests(test_parent.sppTester):

    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)

        self.uname = "bernd"
        self.upass = "das_brot"

    def tearDown(self):
        with self.app.app_context():
            User.query.filter(User.username == self.uname).delete() # delete test user
            db.session.commit()

    def test_main_not_logged_in(self):
        """
        Test all the pages inside of the start module
        for their behaviour should an unauthorised user
        try to visit them
        -> /
        -> /logout
        -> /account
        -> /login
        -> /register
        """
        tester = self.app.test_client()
        response = tester.get("/",
                              content_type="html/text",
                              follow_redirects=True)
        self.assertTrue(
            b"Welcome to Screamsocial" in response.data)
        response = tester.get("/logout",
                              content_type="html/text",
                              follow_redirects=True)
        self.assertTrue(
            b"Yay." in response.data)
        response = tester.get("/account",
                              content_type="html/text",
                              follow_redirects=True)
        self.assertTrue(
            b"Unauthorised!" in response.data)
        response = tester.get("/login",
                              content_type="html/text",
                              follow_redirects=True)
        self.assertTrue(
            b"Login" in response.data and
            b"Username" in response.data)
        response = tester.get("/register",
                              content_type="html/text",
                              follow_redirects=True)
        self.assertTrue(
            b"Register" in response.data and
            b"Repeat Password" in response.data)

    def test_login(self):
        """
        Test login functionality. Creates a test user (bernd, das_brot)
        for test purposes, this user is later deleted (by the teardown
        function).
        """
        user = User(username=self.uname)
        user.set_password(self.upass)
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        tester = self.app.test_client()
        response = tester.post(
            "/login",
            data={"username": self.uname, "password": self.upass},
            follow_redirects=True
        )
        self.assertTrue(b"Logged in as bernd" in response.data)

    def test_fail_login(self):
        """
        Try to logon with the test user, but the test user
        is not registered. Login should fail.
        """
        tester = self.app.test_client()
        response = tester.post(
            "/login",
            data={"username": self.uname, "password": self.upass},
            follow_redirects=True
        )
        self.assertTrue(b"Login failed. Try again." in response.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
