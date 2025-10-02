"""Module"""
import unittest

import hello_world


class HelloTestCase(unittest.TestCase):
    """Class"""
    def test_hello(self):
        """Func"""
        m = "message"
        self.assertEqual(m, hello_world.text())
