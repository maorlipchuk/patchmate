#!/usr/bin/env python
# -*- coding: utf-8 -*-
from blame import BlameHeuristic
from owner_files import OwnerFilesHeuristic


class ReviewersGetter(object):
    HEURISTIC_LISTS = [BlameHeuristic,
                       OwnerFilesHeuristic]

    def __init__(self, repo_path, youngest_commit, oldest_commit, settings=None):
        self.repo_path = repo_path
        self.youngest_commit = youngest_commit
        self.oldest_commit = oldest_commit
        self.settings = settings
        self._result = {'maintainers': [],
                        'cc': [],
                        }

    @property
    def result(self):
        return self.get_reviwers()

    def _get_reviewers(self):
        self._result['maintainers'] += BlameHeuristic(self.repo_path, self.youngest_commit, self.oldest_commit).get_reviewers()
        owner_result = OwnerFilesHeuristic(self.repo_path, self.youngest_commit, self.oldest_commit).get_reviewers()
        self._result['maintainers'] += owner_result['maintainers']
        self._result['cc'] += owner_result['cc']
        return self._result
