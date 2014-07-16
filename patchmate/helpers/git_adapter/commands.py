#!/usr/bin/env python
# -*- coding: utf-8 -*-

git_log_command = "git log {since}..{until} --format=%h"
get_changed_files_in_commit = 'git diff-tree --no-commit-id --name-only -r {commit_id}'
get_concrete_file_commit_info = 'git show -U0 {commit_id} {file_path}'
git_blame_command = "git blame {commit_id} {file_path} -L{line},{line} -e"
get_email_command = "git config user.email"
get_first_commit_before_patch = "git log {since}^ -n 1 --format=%h"
