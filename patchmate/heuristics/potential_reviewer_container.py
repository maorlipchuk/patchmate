#!/usr/bin/env python
# -*- coding: utf-8 -*-


class PotentialReviewer(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return '"{}" <{}>'.format(self.name, self.email)
