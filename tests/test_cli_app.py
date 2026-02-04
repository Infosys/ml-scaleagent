import unittest
from app.cli import app


class TestCliApp(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(app)
