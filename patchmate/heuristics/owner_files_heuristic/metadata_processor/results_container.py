#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ReceiversAndGroupsContainer(object):
    def __init__(self):
        self.receivers = []
        self.groups = []

    def __iadd__(self, other):
        self.receivers += other.receivers
        self.groups += other.receivers
        return self


class ResultsContainer(object):
    def __init__(self):
        self.maintainers = ReceiversAndGroupsContainer()
        self.cc = ReceiversAndGroupsContainer()
        self._recursive = 0

    def __iadd__(self, other):
        self.maintainers += other.maintainers
        self.cc += other.cc
        #self._recursive = other.recursive
        return self

    @property
    def recursive(self):
        return self._recursive

    @recursive.setter
    def recursive(self, value):
        self._recursive = bool(int(value))


