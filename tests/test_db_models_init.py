import unittest
from app.db.models import __init__


class TestDbModelsInit(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(__init__)
