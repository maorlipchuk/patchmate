#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ReceiversAndGroupsContainer(object):
    def __init__(self):
        self.receivers = set([])
        self.groups = set([])

    def __iadd__(self, other):
        self.receivers = self.receivers.union(other.receivers)
        self.groups = self.groups.union(other.groups)
        return self

    def __iter__(self):
        return iter([self.receivers, self.groups])


class ResultsContainer(object):
    def __init__(self):
        self.maintainers = ReceiversAndGroupsContainer()
        self.cc = ReceiversAndGroupsContainer()
        self._recursive = False

    def __iadd__(self, other):
        self.maintainers += other.maintainers
        self.cc += other.cc
        self._recursive = other.recursive
        return self

    def __iter__(self):
        return iter([self.maintainers.receivers, self.cc.receivers])

    def __getitem__(self, item):
        if item == 'maintainers':
            return self.maintainers.receivers
        elif item == 'cc':
            return self.cc.receivers
        else:
            raise KeyError("Key: {} does not exist in ResultContainer".format(item))

    @property
    def recursive(self):
        return self._recursive

    @recursive.setter
    def recursive(self, value):
        self._recursive = bool(int(value))
