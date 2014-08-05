#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main part of script
"""
import os
import argparse
from patchmate.common.git_adapter.git_adapter import GitAdapter
from patchmate.common.settings_updater import update_settings
from patchmate.heuristics import ReviewersGetter
from patchmate.common.gerrit_adapter import add_reviewers_to_gerrit


def _verify_commits(repo_path, commit_hash1, commit_hash2):
    git_adapter = GitAdapter(repo_path)
    git_adapter.verify_commit_hash(commit_hash1)
    git_adapter.verify_commit_hash(commit_hash2)


def main(args):
    _verify_commits(args.repo_path, args.youngest_commit, args.oldest_commit)
    update_settings(args.config)
    add_reviewers_to_gerrit(args.username, args.password, args.url, args.change_id, ReviewersGetter.result['maintainers'])
    add_reviewers_to_gerrit(args.username, args.password, args.url, args.change_id, ReviewersGetter.result['cc'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--youngest-commit", "-y", help="The youngest commit from patch", required=True)
    parser.add_argument("--oldest-commit", "-o", help="The oldest commit from patch", required=True)
    parser.add_argument("--repo-path", "-rp", help="Git repository path", default=os.getcwd())
    parser.add_argument("--gerrit-username", "-gu", help="Gerrit username", required=True)
    parser.add_argument("--gerrit-password", "-gp", help="Gerrit password", required=True)
    parser.add_argument("--gerrit-url", "-gurl", help="Gerrit url", required=True)
    parser.add_argument("--change-id", "-ci", help="Gerrit change_id", required=True)
    parser.add_argument("--config", "-c", help="Ini configuration files path", default=None)
    args = parser.parse_args()
    main(args)
