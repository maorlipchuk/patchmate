#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


class MetadataLineWrapper(object):
    def __init__(self, line):
        self.line = line
        self.type = self._get_line_type()

    def _get_line_type(self):
        if self._is_maintainer_line():
            return "maintainers"
        elif self._is_cc_line():
            return "cc"
        elif self._is_recursive_line():
            return "recursive"
        else:
            pass

    def _is_maintainer_line(self):
        return True if re.search(r"MAINTAINER", self.line) else False

    def _is_cc_line(self):
        return True if re.search(r"CC", self.line) else False

    def _is_recursive_line(self):
        return True if re.search(r"RECURSIVE", self.line) else False

    def _add_receivers(self, key, result):
        content = re.match(r".*{}=(?P<content>.*)".format(key.upper()), self.line).group('content')
        for potential_receiver in content.split(','):
            potential_receiver = potential_receiver.strip()
            if "group" in potential_receiver:
                group = re.match(r'group:(?P<group>[A-Za-z0-9_]*)', potential_receiver).group('group')
                getattr(result, key.lower()).groups.add(group)
            else:
                name, email = re.match(r'"(?P<name>.*)" <(?P<email>.*@.*)>', potential_receiver).groups()
                getattr(result, key.lower()).receivers.add((name, email))

    def _add_recursive_info(self, result):
        recursive_flag = re.match(".*RECURSIVE=(?P<number>[0-1])", self.line).group('number')
        result.recursive = recursive_flag

    def add_content(self, result):
        if self.type in ('maintainers', 'cc'):
            self._add_receivers(self.type, result)
        elif self.type == "recursive":
            self._add_recursive_info(result)
