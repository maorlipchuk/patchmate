#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from receivers import GroupOfPotentialReceivers, PotentialReceiver


class MetadataLineWrapper(object):
    def __init__(self, line):
        self.line = line
        self.type = self._get_line_type()

    def _get_line_type(self):
        if self._is_maintainer_line():
            return "maintainer"
        elif self._is_cc_line():
            return "cc"
        elif self._is_recursive_line():
            return "recursive"
        else:
            raise Exception("Unexpected line type")

    def _is_maintainer_line(self):
        return True if re.search(r"MAINTAINER", self.line) else False

    def _is_cc_line(self):
        return True if re.search(r"CC", self.line) else False

    def _is_recursive_line(self):
        return True if re.search(r"RECURSIVE", self.line) else False

    def _add_receivers(self, key, result):
        content = re.match(r".*{}=(?P<content>.*)".format(key.upper()), self.line).group('content')
        for maintainer in content.split(','):
            maintainer = maintainer.strip()
            if "group" in maintainer:
                group_name = re.match(r'group:(?P<group_name>.*)', maintainer).group('group_name')
                result['{}'.format(key.lower())]['groups'].append(GroupOfPotentialReceivers(group_name))
            else:
                name, email = re.match(r'"(?P<name>.*)" <(?P<email>.*@.*)>', maintainer).groups()
                result['{}'.format(key.lower())]['receivers'].append(PotentialReceiver(name, email))

    def _add_recursive_info(self, result):
        recursive_flag = re.match(".*RECURSIVE=(?P<number>[0-1])", self.line).group('number')
        result['recursive'] = recursive_flag

    def add_content(self, result):
        if self.type in ('maintainer', 'cc'):
            self._add_receivers(self.type, result)
        elif self.type == "recursive":
            self._add_recursive_info(result)
