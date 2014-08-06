#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from patchmate.heuristics.owner_files import OwnerFilesHeuristic
from exception import RegressionTestError
from test_data import REPO_PATH, YOUNGEST_COMMIT, OLDEST_COMMIT
from expected_test_results import EXPECTED_EMAILS, UNEXPECTED_EMAILS


result = OwnerFilesHeuristic(REPO_PATH, YOUNGEST_COMMIT, OLDEST_COMMIT).get_reviewers()
emails_only = [receiver.email for receiver in result.maintainers.receivers + result.cc.receivers]

for expected_email in EXPECTED_EMAILS:
    if expected_email not in emails_only:
        raise RegressionTestError("Email {} should be on the list".format(expected_email))


for unexpected_email in UNEXPECTED_EMAILS:
    if unexpected_email in emails_only:
        raise RegressionTestError("Email {} should not be on the list".format(unexpected_email))
