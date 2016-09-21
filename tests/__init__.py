import unittest

class InitializationTests(unittest.TestCase):
  def test_initialization(self):
    self.assertEqual(1+1, 2)
  def test_import(self):
    try:
      import pypoint
    except ImportError:
      self.fail("Was not able to import pypoint")
