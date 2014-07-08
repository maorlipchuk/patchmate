#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from results_container import ResultsContainer
from line_wrapper import MetadataLineWrapper


class PotentialReceiver(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return '"{}" <{}>'.format(self.name, self.email)


class GroupOfPotentialReceivers(object):
    def __init__(self, name):
        self.group_name = name

    def __str__(self):
        return "Group: {}".format(self.group_name)

    def _get_maintainers(self, result, project_root):
        if result.maintainers.groups:
            for group in result.maintainers.groups:
                result.maintainers.receivers += GroupOfPotentialReceivers(group)._get_emails(project_root).maintainers.receivers
        return result

    def _get_cc(self, result, project_root):
        if result.cc.groups:
            for group in result.cc.groups:
                result.cc.receivers += GroupOfPotentialReceivers(group)._get_emails(project_root).cc.receivers
        return result

    def _get_emails(self, project_root):
        result = ResultsContainer()
        groups_dir = os.path.join(project_root, 'review', 'groups')
        group_file_path = os.path.join(groups_dir, "{}.metadata".format(self.group_name))
        with open(group_file_path) as group_file:
            for line in group_file.readlines():
                MetadataLineWrapper(line).add_content(result)

        result = self._get_cc(result, project_root)
        result = self._get_maintainers(result, project_root)

        return result

    def get_emails(self, project_root):
        d = self._get_emails(project_root)
        maintainers = [PotentialReceiver(name, email) for name, email in d.maintainers.receivers]
        cc = [PotentialReceiver(name, email) for name, email in d.cc.receivers]
        return {"maintainers": maintainers, 'cc': cc}
