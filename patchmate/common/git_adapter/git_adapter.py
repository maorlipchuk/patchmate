#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import subprocess
from commands import git_log_command, get_changed_files_in_commit, get_email_command, verify_commit
from commands import get_concrete_file_commit_info, git_blame_command, get_first_commit_before_patch
from exceptions import GitAdapterNotValidCommitHash


class GitAdapter(object):
    """
    Git adapter class
    """
    def __init__(self, repository_path):
        """
        Constructor

        :param repository_path: Path to git repository
        :type repository_path: str
        """
        self.repository_path = repository_path

    def _execute_command(self, command):
        return subprocess.check_output(command, cwd=self.repository_path, shell=True)

    def verify_commit_hash(self, commit_hash):
        """
        Verifies if commit hash is correct and unique and raises error if not

        :param commit_hash: Commit hash
        :type commit_hash: str
        """
        try:
            self._execute_command(verify_commit.format(commit_hash=commit_hash))
        except subprocess.CalledProcessError:
            raise GitAdapterNotValidCommitHash("Commit hash {} is not valid in your repository".format(commit_hash))

    def get_current_user_email(self):
        """
        Gets local git user email address
        """
        return self._execute_command(get_email_command).strip()

    def get_commits_from_range(self, youngest_commit, oldest_commit):
        """
        Gets all commits from range (since youngest_commit to oldest_commit) and returns commit in reverse order
        i.e from oldest commit to youngest

        :param youngest_commit: Youngest (the earliest done) commit hash
        :type youngest_commit: str

        :param oldest_commit: Oldest (the latest done) commit hash
        :type oldest_commit: str
        """
        all_commits = self._execute_command(git_log_command.format(since=oldest_commit, until=youngest_commit)).splitlines()
        all_commits += [oldest_commit] if oldest_commit not in all_commits else all_commits
        all_commits = all_commits[::-1]
        return all_commits

    def get_changed_files_in_commit(self, commit_hash):
        """
        Gets all changed files in specified by parameter commit

        :param commit_hash: Commit hash
        :type commit_hash: str
        """
        output = self._execute_command(get_changed_files_in_commit.format(commit_id=commit_hash))
        return re.match(r"(?P<content>.*)\ncommit {}".format(commit_hash), output, re.DOTALL).group('content').splitlines()

    def get_concrete_file_commit_info(self, commit_hash, file_path):
        """
        Gets info about specified file from specified commit

        :param commit_hash: Commit hash
        :type commit_hash: str

        :param file_path: Path to file
        :type file_path: str
        """
        return self._execute_command(get_concrete_file_commit_info.format(commit_id=commit_hash, file_path=file_path))

    def get_line_author_email(self, commit_hash, file_path, line):
        """
        Gets email address of person who made specified line in specified file in specified commit

        :param commit_hash: Commit hash
        :type commit_hash: str

        :param file_path: Path to file
        :type file_path: str

        :param line: Line number
        :type line: int
        """
        line = self._execute_command(git_blame_command.format(commit_id=commit_hash, file_path=file_path, line=line))
        return re.match(r".* \(<(?P<email>.*@.*)>.*".format(commit_hash), line.strip()).group('email')

    def get_first_commit_hash_before_given(self, commit_hash):
        """
        Gets first commit hash after given commit
        e.g
        Git log:
        commit1
        commit2
        commit3

        get_first_commit_hash_before_given("commit2") -> "commit3"

        :param commit_hash: Commit hash
        :type commit_hash: str
        """
        return self._execute_command(get_first_commit_before_patch.format(since=commit_hash)).strip()
