#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class GroupOfPotentialReceivers(object):
    def __init__(self, name):
        self.group_name = name

    def __str__(self):
        return "Group: {}".format(self.group_name)

    def get_emails(self, project_root):
        """
        TO IMPROVE
        """
        groups_dir = os.path.join(project_root, 'review', 'groups')
        group_file_path = os.path.join(groups_dir, "{}.metadata".format(self.group_name))
        with open(group_file_path) as group_file:
            print group_file.read()


class PotentialReceiver(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return '"{}" <{}>'.format(self.name, self.email)