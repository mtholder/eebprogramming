#!/usr/bin/env python
"""Template for the __init__ file in a python package."""

import unittest
from firstpy import get_logger

_LOG = get_logger("firstpy/tests")


class TestSomeFunction(unittest.TestCase):
    def test_basic(self):
        from firstpy import some_function
        _LOG.debug("About to test 'some_function(0)'")
        self.assertEqual(some_function(0), 1)
        _LOG.debug("done testing 'some_function(0)'")



if __name__ == '__main__':
    unittest.main()
