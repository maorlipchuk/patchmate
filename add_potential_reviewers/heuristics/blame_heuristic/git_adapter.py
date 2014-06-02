#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import subprocess
from blame_heuristic_settings import git_log_command, get_author_command, get_changed_files_in_commit
from blame_heuristic_settings import get_concrete_file_commit_info, git_blame_command


class GitAdapter(object):
    def __init__(self, repository_path):
        self.repository_path = repository_path

    def _execute_command(self, command):
        return subprocess.check_output(command.split(), cwd=self.repository_path)

    def _get_author(self):
        return self._execute_command(get_author_command).strip()

    def get_last_author_commits(self, author):
        """
        Returns commit hashes list
        """
        results_commits_hashes = []
        all_commits = self._execute_command(git_log_command)
        for commit in all_commits.splitlines():
            commit_hash, commit_author = commit.split(',')
            if commit_author != author:
                break
            results_commits_hashes.append(commit_hash)
        return results_commits_hashes[::-1]

    def get_commits_from_range(self, youngest_commit, oldest_commit):
        """
        TO IMPROVE
        """
        results_commits_hashes = []
        all_commits = self._execute_command(git_log_command).splitlines()
        for index, commit in enumerate(all_commits):
            commit_hash, _ = commit.split(',')
            if len(results_commits_hashes) > 0:
                results_commits_hashes.append(commit_hash)
            elif commit_hash == youngest_commit:
                results_commits_hashes.append(commit_hash)

            if commit_hash == oldest_commit:
                results_commits_hashes.append(all_commits[index + 1].split(',')[0])
                return results_commits_hashes[::-1]

    def get_changed_files_in_commit(self, commit_id):
        changed_files = self._execute_command(get_changed_files_in_commit.format(commit_id=commit_id))
        return changed_files.splitlines()

    def get_concrete_file_commit_info(self, commit_id, file_path):
        return self._execute_command(get_concrete_file_commit_info.format(commit_id=commit_id, file_path=file_path))

    def get_line_author(self, commit_id, file_path, line):
        line = self._execute_command(git_blame_command.format(commit_id=commit_id, file_path=file_path, line=line))
        return re.match(r".* \(<(?P<email>.*@.*)>.*".format(commit_id), line.strip()).group('email')
