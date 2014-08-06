#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .blame_script import original_line_numbers
from ..interface import HeuristicInterface
from ..potential_reviewer_container import PotentialReviewer
from patchmate.common.git_adapter.git_adapter import GitAdapter


class BlameHeuristic(HeuristicInterface):
    def __init__(self, repository_path, youngest_commit, oldest_commit):
        """
        Constructor

        :param repository_path: Path to git repository
        :type repository_path: str

        :param youngest_commit: Youngest (the earliest done) commit hash
        :type youngest_commit: str

        :param oldest_commit: Oldest (the latest done) commit hash
        :type oldest_commit: str
        """
        self.git_adapter = GitAdapter(repository_path)
        self.youngest_commit = youngest_commit
        self.oldest_commit = oldest_commit
        self._potential_reviewers = []

    def get_reviewers(self):
        """
        Returns potential reviewers
        """
        current_user_email = self.git_adapter.get_current_user_email()
        commits_list = self.git_adapter.get_commits_from_range(self.youngest_commit, self.oldest_commit)

        for index, commit_hash in enumerate(commits_list):
            commit_before_current = self.git_adapter.get_first_commit_hash_before_given(self.oldest_commit) if index == 0 else commits_list[index - 1]
            self._get_potential_reviewers_for_specified_commit(commit_hash, commit_before_current)

        potential_reviewers = set(self._potential_reviewers)
        if current_user_email in potential_reviewers:
            potential_reviewers.remove(current_user_email)

        return list(potential_reviewers)

    def _add_potential_reviewers_for_specified_file(self, commit_info, commit_before_current, changed_file):
        for line in original_line_numbers(commit_info):
            email = self.git_adapter.get_line_author_email(commit_before_current, changed_file, line)
            name = email  # TEMPORARY
            self._potential_reviewers.append(PotentialReviewer(name, email))

    def _get_potential_reviewers_for_specified_commit(self, current_commit_hash, commit_before_current):
        for changed_file in self.git_adapter.get_changed_files_in_commit(current_commit_hash):
            commit_info = self.git_adapter.get_concrete_file_commit_info(current_commit_hash, changed_file)
            self._add_potential_reviewers_for_specified_file(commit_info, commit_before_current, changed_file)
