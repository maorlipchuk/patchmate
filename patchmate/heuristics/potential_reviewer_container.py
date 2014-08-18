#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PotentialReviewer(object):
    def __init__(self, name, email, files=[]):
        self.name = name
        self.email = email
        self.files = files

    def __str__(self):
        return '"{}" <{}>'.format(self.name, self.email)
