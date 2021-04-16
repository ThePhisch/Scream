import unittest
from spp import create_app

class PrimaryTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

    def tearDown(self):
        pass

    def test_Start(self):
        tester = self.app.test_client()
        response = tester.get('/', content_type="html/text")
        self.assertTrue(b"it worx!" in response.data)

if __name__ == "__main__":
    unittest.main(verbosity=2)