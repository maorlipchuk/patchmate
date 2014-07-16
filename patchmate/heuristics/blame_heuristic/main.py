#!/usr/bin/env python
# -*- coding: utf-8 -*-

from patchmate.helpers.git_adapter.git_adapter import GitAdapter
from blame_script import original_line_numbers
from patchmate.interface import HeuristicInterface


class BlameHeuristic(HeuristicInterface):
    def __init__(self, repo_path, youngest_commit, oldest_commit):
        self.git_adapter = GitAdapter(repo_path)
        self.youngest_commit = youngest_commit
        self.oldest_commit = oldest_commit

    def get_reviewers(self):
        current_user_email = self.git_adapter.get_current_user_email()
        potential_reviewers = set([])
        commits_list = self.git_adapter.get_commits_from_range(self.youngest_commit, self.oldest_commit)
        for index, commit_hash in enumerate(commits_list):
            commit_before = self.git_adapter.get_first_commit_hash_before_patch(self.oldest_commit) if index == 0 else commits_list[index - 1]
            for changed_file in self.git_adapter.get_changed_files_in_commit(commit_hash):
                commit_info = self.git_adapter.get_concrete_file_commit_info(commit_hash, changed_file)
                for line in original_line_numbers(commit_info):
                    potential_reviewers.add(self.git_adapter.get_line_author_email(commit_before, changed_file, line))

        if current_user_email in potential_reviewers:
            potential_reviewers.remove(current_user_email)

        return potential_reviewers
