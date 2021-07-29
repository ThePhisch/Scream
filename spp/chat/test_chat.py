
from typing import Tuple, List
import unittest

from flask.app import Flask
from spp import create_app, test_parent

from spp import db
from spp.models import User

from flask_login import current_user, logout_user


class PrimaryTests(test_parent.sppTester):

    testUsersSource = [
        ("Meredith", "Grey"),
        ("Alex", "Karev"),
        ("George", "O'Malley"),
        ("Izzie", "Stevens"),
        ("Cristina", "Yang")
    ]

    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self.app = create_app()

    @classmethod
    def formatUsers(cls, source: Tuple[str, str]) -> User:
        user = User(username=source[0])
        user.set_password(source[1])
        return user

    app = create_app()

    @classmethod
    def setUpClass(cls) -> None:
        with cls.app.app_context():
            # Delete test users (if they haven't been cleaned by tearDownClass)
            for username in map(lambda x: x[0], cls.testUsersSource):
                User.query.filter(User.username == username).delete()
            db.session.commit()
        # Format test users
        cls.testUsers = map(cls.formatUsers, cls.testUsersSource)
        with cls.app.app_context():
            # Create test users
            for user in cls.testUsers:
                db.session.add(user)
            db.session.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.app.app_context():
            # Delete test users
            for user in cls.testUsers:
                User.query.filter(User.username == user.username).delete()
            db.session.commit()

    def test_make_room(self) -> None:
        """
        Create room 'newroom' by user 'Meredith'
        -> log in user
        -> create room
        -> close room
        -> logout
        """
        # Login with user 'Meredith'
        tester = self.app.test_client()
        meredith = self.testUsersSource[0]
        response = tester.post("/login", data={"username": meredith[0],
                                               "password": meredith[1]},
                               follow_redirects=True)
        self.assertTrue(b"Logged in as Meredith" in response.data)

        # Create new room 'newroom'
        response = tester.post(
            "/lobby", data={"room": "newroom"}, follow_redirects=True)
        self.assertTrue(b"newroom" in response.data)
        self.assertTrue(b"Close room" in response.data)

        # Close new room 'newroom'
        response = tester.get("/chat/newroom/close",
                              content_type="html/text", follow_redirects=True)
        self.assertFalse(b"newroom" in response.data)
        self.assertFalse(b"Close room" in response.data)

        # Logout user 'Meredith'
        response = tester.get("/logout",
                              content_type="html/text",
                              follow_redirects=True)
        self.assertFalse(b"Logged in as Meredith" in response.data)
