#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from add_potential_reviewers.heuristics.blame_heuristic.commits import removed_one_line, replace_line_new_one, replace_line_two_ones_removed_one_line_add_one


last_commited_files = "git log --name-status HEAD^..HEAD"
line_number_regexp = r'@@ -(?P<line_number>[[0-9]+)(,[0-9]+)? \+(?P<line_number2>[0-9]+)(,[0-9]+)? @@.*'


def original_line_numbers(commit_info):
    """
    commit_hash -> only number.
    """
    result = set([])
    count_changed_lines = 0
    for line in commit_info.splitlines():
        if line.startswith("+++") or line.startswith("---"): continue

        elif re.match(line_number_regexp, line):
            #MATCH LINE NUMBERS
            line_number2 = int(re.match(line_number_regexp, line).group('line_number2'))
            line_number = int(re.match(line_number_regexp, line).group('line_number'))
            if line_number > line_number2:
                result.add(line_number)

        elif line.startswith('+'):
            #if code line is added
            count_changed_lines -= 1

        elif line.startswith('-'):
            #if code line is removed
            result.add(line_number - count_changed_lines)
            count_changed_lines += 1

    return result


print original_line_numbers(replace_line_two_ones_removed_one_line_add_one)
print original_line_numbers(replace_line_new_one)
print original_line_numbers(removed_one_line)
