#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main part of script
"""
import os
import argparse
from patchmate.helpers.git_adapter.git_adapter import GitAdapter
from patchmate.helpers.settings_updater import update_settings
from patchmate.heuristics import BlameHeuristic, OwnerFilesHeuristic


def verify_commits(repo_path, commit_hash1, commit_hash2):
    git_adapter = GitAdapter(repo_path)
    git_adapter.verify_commits_number(commit_hash1)
    git_adapter.verify_commits_number(commit_hash2)


def main(args):
    verify_commits(args.repo_path, args.youngest_commit, args.oldest_commit)
    update_settings(args.config)
    blame_result = BlameHeuristic(args.repo_path, args.youngest_commit, args.oldest_commit).get_reviewers()
    owner_result = OwnerFilesHeuristic(args.repo_path, args.youngest_commit, args.oldest_commit).get_reviewers()

    print "Send an email"
    print "Update reviewers"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--youngest_commit", "-y", help="The youngest commit from patch", required=True)
    parser.add_argument("--oldest_commit", "-o", help="The oldest commit from patch", required=True)
    parser.add_argument("--repo_path", "-rp", help="Ini configuration files path", default=os.getcwd())
    parser.add_argument("--config", "-c", help="Ini configuration files path", default=None)
    args = parser.parse_args()
    main(args)
