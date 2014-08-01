#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from data_provider import data_provider
from commits_test_data import removed_one_line, replace_line_new_one, replace_line_two_ones, replace_line_two_ones_removed_one_line_add_one
from patchmate.heuristics.blame.blame_script import original_line_numbers


class TestBlameScript(unittest.TestCase):
    data = lambda: (
        (removed_one_line, set([6])),
        (replace_line_new_one, set([6])),
        (replace_line_two_ones, set([6])),
        (replace_line_two_ones_removed_one_line_add_one, set([6, 10]))
    )

    @data_provider(data)
    def test_get_original_line_numbers(self, commit, expected_value):
        self.assertEqual(original_line_numbers(commit), expected_value)


if __name__ == "__main__":
    unittest.main()
