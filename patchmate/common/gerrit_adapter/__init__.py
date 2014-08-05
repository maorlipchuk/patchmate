#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gerrit_adapter import GerritAdapter


def add_reviewers_to_gerrit(username, password, url, change_id, reviewers):
    ga = GerritAdapter(url, username, password)
    for reviewer in reviewers:
        ga.add_reviewer(change_id, reviewer.email)
