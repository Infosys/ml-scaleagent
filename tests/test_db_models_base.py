import unittest
from app.db.models import base


class TestDbModelsBase(unittest.TestCase):
    def test_import(self):
        self.assertIsNotNone(base)
