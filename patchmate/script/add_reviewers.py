#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main part of script
"""
import os
import argparse
from patchmate.helpers.settings_updater import update_settings
from patchmate.heuristics import BlameHeuristic



def main(args):
    update_settings(args.config)

    BlameHeuristic(args.repo_path, args.youngest_commit, args.oldest_commit).get_reviewers()
    print "Get reviewers from heuristics"
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
