#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from commits_test_data import removed_one_line, replace_line_new_one, replace_line_two_ones, replace_line_two_ones_removed_one_line_add_one
from patchmate.heuristics.blame_heuristic.blame_script import original_line_numbers


def data_provider(fn_data_provider):
    """Data provider decorator, allows another callable to provide the data for the test"""
    def test_decorator(fn):
        def repl(self, *args):
            for i in fn_data_provider():
                try:
                    fn(self, *i)
                except AssertionError:
                    print "Assertion error caught with data set ", i
                    raise
        return repl
    return test_decorator


class TestBlameScript(unittest.TestCase):
    data = lambda: (
        (removed_one_line, set([6])),
        (replace_line_new_one, set([6])),
        (replace_line_two_ones, set([6])),
        (replace_line_two_ones_removed_one_line_add_one, set([6, 10]))
    )

    @data_provider(data)
    def test_get_originam_line_numbers(self, commit, expected_value):
        print expected_value
        self.assertEqual(original_line_numbers(commit), expected_value)


if __name__ == "__main__":
    unittest.main()
