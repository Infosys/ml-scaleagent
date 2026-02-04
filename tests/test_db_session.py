import unittest
from app.db import session


class TestDbSession(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(session)
