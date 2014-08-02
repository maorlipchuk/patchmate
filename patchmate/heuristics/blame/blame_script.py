#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

line_number_regexp = r'@@ -(?P<removed_line>[[0-9]+)(,[0-9]+)? \+(?P<added_line>[0-9]+)(,[0-9]+)? @@.*'


def original_line_numbers(commit_info):
    """
    Returns information about line number before changing

    :param commit_info: Commit text info
    :type commit_info: str
    """
    removed_line = count_changed_lines = 0
    result = set([])

    for line in commit_info.splitlines():
        if line.startswith("+++") or line.startswith("---"):
            continue

        elif re.match(line_number_regexp, line):
            removed_line = int(re.match(line_number_regexp, line).group('removed_line'))
            added_line = int(re.match(line_number_regexp, line).group('added_line'))
            if removed_line > added_line:
                result.add(removed_line)

        elif line.startswith('+'):
            # if code line is added
            count_changed_lines += 1

        elif line.startswith('-'):
            # if code line is removed
            result.add(removed_line + count_changed_lines)
            count_changed_lines -= 1

    return result
