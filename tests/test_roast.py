import unittest
import features.roast
import logging

class TestRoast(unittest.TestCase):

    def test_roast(self):
        try:
            features.roast.generate_roast()
        except Exception as exc:
            logging.error(exc)