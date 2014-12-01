#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gerrit_adapter import GerritAdapter


def add_reviewers_to_gerrit(username, password, url, change_id, reviewers):
    gerrit_adapter_object = GerritAdapter(url, username, password)
    for reviewer in reviewers:
        by_email_passed = gerrit_adapter_object.add_reviewer(change_id, reviewer.email)
        if not by_email_passed:
            gerrit_adapter_object.add_reviewer(change_id, reviewer.name)
