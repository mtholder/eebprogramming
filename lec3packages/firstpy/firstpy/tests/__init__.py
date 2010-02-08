#!/usr/bin/env python
"""Template for the __init__ file in a python package."""

import unittest
class TestSomeFunction(unittest.TestCase):
    def test_basic(self):
        from firstpy import some_function
        self.assertEqual(some_function(0), 1)



if __name__ == '__main__':
    unittest.main()
