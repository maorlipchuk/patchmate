#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import subprocess
from blame_heuristic_settings import git_log_command, get_changed_files_in_commit, get_email_command
from blame_heuristic_settings import get_concrete_file_commit_info, git_blame_command, get_first_commit_before_patch


class GitAdapter(object):
    def __init__(self, repository_path):
        self.repository_path = repository_path
        print self.repository_path

    def _execute_command(self, command):
        return subprocess.check_output(command, cwd=self.repository_path, shell=True)

    def get_current_user_email(self):
        return self._execute_command(get_email_command).strip()

    def get_commits_from_range(self, youngest_commit, oldest_commit):
        all_commits = self._execute_command(git_log_command.format(since=oldest_commit, until=youngest_commit)).splitlines()
        all_commits.append(oldest_commit)
        all_commits = all_commits[::-1]
        return all_commits

    def get_changed_files_in_commit(self, commit_id):
        return self._execute_command(get_changed_files_in_commit.format(commit_id=commit_id)).splitlines()

    def get_concrete_file_commit_info(self, commit_id, file_path):
        return self._execute_command(get_concrete_file_commit_info.format(commit_id=commit_id, file_path=file_path))

    def get_line_author_email(self, commit_id, file_path, line):
        line = self._execute_command(git_blame_command.format(commit_id=commit_id, file_path=file_path, line=line))
        return re.match(r".* \(<(?P<email>.*@.*)>.*".format(commit_id), line.strip()).group('email')

    def get_first_commit_hash_before_patch(self, oldest_commit):
        return self._execute_command(get_first_commit_before_patch.format(since=oldest_commit)).strip()
