import unittest
from spp import create_app, db

class sppTester(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.app.config['WTF_CSRF_ENABLED'] = False
        with self.app.app_context():
            db.create_all()