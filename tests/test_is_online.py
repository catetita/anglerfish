#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Test for anglerfish.is_online()."""


import unittest

from anglerfish import is_online


class TestName(unittest.TestCase):

    maxDiff, __slots__ = None, ()

    def test_is_online(self):
        result = is_online()
        assert isinstance(result, bool)
        assert result


if __name__.__contains__("__main__"):
    print(__doc__)
    unittest.main()
