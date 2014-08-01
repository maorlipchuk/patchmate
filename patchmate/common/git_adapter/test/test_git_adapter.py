#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

from mock import patch

from patchmate.common.git_adapter.git_adapter import GitAdapter
import patchmate.common.git_adapter.blame_heuristic_settings as commands_set


@patch("add_potential_reviewers.heuristics.blame_heuristic.git_adapter.subprocess.check_output")
class TestGitAdapter(unittest.TestCase):
    def setUp(self):
        self.repository_path = os.path.join('path', 'to', 'repository')
        self.git_adapter = GitAdapter(self.repository_path)

    def test_if_get_current_user_email(self, check_output_mock):
        command_output = "email@email.com\n"
        expected_email = command_output.strip()
        check_output_mock.return_value = command_output
        value = self.git_adapter.get_current_user_email()
        check_output_mock.assert_called_once_with(commands_set.get_email_command, cwd=self.repository_path)
        self.assertEqual(value, expected_email)

    def test_get_commits_from_range(self, check_output_mock):
        youngest_commit = 'commit10hash'
        oldest_commit = 'commit13hash'
        command_output = "{youngest}\ncommit11hash\ncommit12hash\n{oldest}\n".format(youngest=youngest_commit, oldest=oldest_commit)
        check_output_mock.return_value = command_output
        expected_value = command_output.splitlines()[::-1]
        value = self.git_adapter.get_commits_from_range(youngest_commit, oldest_commit)
        check_output_mock.assert_called_once_with(commands_set.git_log_command.format(since=oldest_commit, until=youngest_commit), cwd=self.repository_path)
        self.assertEqual(value, expected_value)

    def test_get_changed_files_in_commit(self, check_output_mock):
        command_output = "file1\nfile2\nfile3\n"
        commit_id = 'commit_id'
        expected_value = command_output.splitlines()
        check_output_mock.return_value = command_output
        value = self.git_adapter.get_changed_files_in_commit(commit_id)
        check_output_mock.assert_called_once_with(commands_set.get_changed_files_in_commit.format(commit_id=commit_id), cwd=self.repository_path)
        self.assertEqual(value, expected_value)

    def test_get_concrete_file_commit_info(self, check_output_mock):
        commit_id = "commit_id"
        file_path = os.path.join('path', 'to', 'file')
        command_output = "Fake Commit Info"
        check_output_mock.return_value = command_output
        value = self.git_adapter.get_concrete_file_commit_info(commit_id, file_path)
        check_output_mock.assert_called_once_with(commands_set.get_concrete_file_commit_info.format(commit_id=commit_id, file_path=file_path), cwd=self.repository_path)
        self.assertEqual(value, command_output)

    def test_get_line_author_email(self, check_output_mock):
        commit_id = "commit_id"
        file_path = os.path.join('path', 'to', 'file')
        line_number = 1
        expected_email = "email@emial.com"
        command_output = "{commit_id} (<{email}> 2008-07-01 15:10:51 +0000 1)\n".format(commit_id=commit_id, email=expected_email)
        check_output_mock.return_value = command_output
        value = self.git_adapter.get_line_author_email(commit_id, file_path, line_number)
        check_output_mock.assert_called_once_with(commands_set.git_blame_command.format(commit_id=commit_id, file_path=file_path, line=line_number), cwd=self.repository_path)
        self.assertEqual(value, expected_email)

    def test_get_first_commit_hash_before_patch(self, check_output_mock):
        oldest_commit = 'commit_id'
        command_output = "first_before_oldes_commit"
        check_output_mock.return_value = command_output
        value = self.git_adapter.get_first_commit_hash_before_patch(oldest_commit)
        check_output_mock.assert_called_once_with(commands_set.get_first_commit_before_patch.format(since=oldest_commit), cwd=self.repository_path)
        self.assertEqual(value, command_output)


if __name__ == "__main__":
    unittest.main()
