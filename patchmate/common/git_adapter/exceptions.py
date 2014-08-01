#!/usr/bin/env python
# -*- coding: utf-8 -*-


class GitAdapterException(Exception):
    """
    Base Git adapter exception
    """
    pass


class GitAdapterNotValidCommitHash(GitAdapterException):
    """
    Git adapter exception signalizing about not valid commit hash
    """
    pass
