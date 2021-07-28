import unittest
from spp import create_app

from spp import db
from spp.models import User

from flask_login import current_user, logout_user


class PrimaryTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        # Necessary for filling in the forms automatically
        self.app.config['WTF_CSRF_ENABLED'] = False
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        pass

    def test_Start(self):
        tester = self.app.test_client()
        response = tester.get('/', content_type="html/text")
        self.assertTrue(b"Yay." in response.data)

    def test_Unauthorised(self):
        tester = self.app.test_client()
        response = tester.get("/account",
                              content_type="html/text",
                              follow_redirects=True)
        self.assertTrue(b"Unauthorised" in response.data)

    def test_logout_not_logged_in(self):
        # TODO THIS WILL ~~ALWAYS~~ PASS, rework the test
        tester = self.app.test_client()
        response = tester.get("/logout",
                              content_type="html/text",
                              follow_redirects=True)
        self.assertTrue(
            b"Yay." in response.data)

    def test_login(self):
        uname, upass = "bernd", "das_brot"
        user = User(username=uname)
        user.set_password(upass)
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
        tester = self.app.test_client()
        response = tester.post(
            "/login",
            data={"username": uname, "password": upass},
            follow_redirects=True
        )
        self.assertTrue(b"bernd" in response.data)
        with self.app.app_context():
            db.session.delete(user)
            db.session.commit()

        response = tester.post(
            "/login",
            data={"username": uname, "password": upass},
            follow_redirects=True
        )
        self.assertTrue(b"Login failed. Try again." in response.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
