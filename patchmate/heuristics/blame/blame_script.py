#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

line_number_regexp = r'@@ -(?P<line_number>[[0-9]+)(,[0-9]+)? \+(?P<line_number2>[0-9]+)(,[0-9]+)? @@.*'


def original_line_numbers(commit_info):
    """
    commit_hash -> only number.
    """
    line_number = 0
    result = set([])
    count_changed_lines = 0
    for line in commit_info.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue

        elif re.match(line_number_regexp, line):
            line_number = int(re.match(line_number_regexp, line).group('line_number'))
            line_number2 = int(re.match(line_number_regexp, line).group('line_number2'))
            if line_number > line_number2:
                result.add(line_number)

        elif line.startswith('+'):
            # if code line is added
            count_changed_lines += 1

        elif line.startswith('-'):
            # if code line is removed
            result.add(line_number + count_changed_lines)
            count_changed_lines -= 1

    return result
