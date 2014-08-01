#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re


class PotentialReceiver(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return '"{}" <{}>'.format(self.name, self.email)


class GroupOfPotentialReceivers(object):
    groups_file_content = None

    def __init__(self, name):
        self.group_name = name
        self.receivers = []

    def __str__(self):
        return "Group: {}".format(self.group_name)

    def _get_groups_metadata_content_file(self, project_root):
        if not GroupOfPotentialReceivers.groups_file_content:
            groups_metadata_file_path = os.path.join(project_root, 'review', 'groups.metadata')
            with open(groups_metadata_file_path) as group_file:
                GroupOfPotentialReceivers.groups_file_content = group_file.read()

    def _get_emails(self, project_root):
        self._get_groups_metadata_content_file(project_root)
        content = re.search(".*{}=(?P<content>.*)".format(self.group_name), GroupOfPotentialReceivers.groups_file_content).group('content')

        for potential_receiver in content.split(','):
            potential_receiver = potential_receiver.strip()
            if "group" in potential_receiver:
                group = re.match(r'group:(?P<group>[A-Za-z0-9_]*)', potential_receiver).group('group')
                self.receivers += GroupOfPotentialReceivers(group).get_emails(project_root)
            else:
                name, email = re.match(r'"(?P<name>.*)" <(?P<email>.*@.*)>', potential_receiver).groups()
                self.receivers.append(PotentialReceiver(name, email))
        return self.receivers

    def get_emails(self, project_root):
        receivers_list = self._get_emails(project_root)
        return receivers_list
