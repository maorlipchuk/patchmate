#!/usr/bin/env python
# -*- coding: utf-8 -*-

from git_adapter import GitAdapter
from blame_script import original_line_numbers
from add_potential_reviewers.interface import HeuristicInterface


class BlameHeuristic(HeuristicInterface):
    def __init__(self, repo_path, youngest_commit, oldest_commit):
        self.git_adapter = GitAdapter(repo_path)
        self.youngest_commit = youngest_commit
        self.oldest_commit = oldest_commit

    def get_reviewers(self):
        potential_reviewers = set([])
        commits_list = self.git_adapter.get_commits_from_range(self.youngest_commit, self.oldest_commit)
        for index, commit_hash in enumerate(commits_list):
            if index == 0:
                continue
            for changed_file in self.git_adapter.get_changed_files_in_commit(commit_hash):
                commit_info = self.git_adapter.get_concrete_file_commit_info(commit_hash, changed_file)
                for line in original_line_numbers(commit_info):
                    potential_reviewers.add(self.git_adapter.get_line_author(commits_list[index - 1], changed_file, line))

        return potential_reviewers






