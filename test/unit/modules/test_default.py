import unittest
import mock

class TrivialTestCase(unittest.TestCase):
    def setUp(self):
        print("Setting up TrivialTestCase.")

    def test_trivial(self):
        self.assertEquals(True, True)
