import unittest
from app.cli import __init__


class TestCliInit(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(__init__)
