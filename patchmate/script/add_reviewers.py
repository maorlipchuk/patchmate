#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main part of script
"""
import os
import argparse
from patchmate.helpers.settings_updater import update_settings
from patchmate.heuristics import BlameHeuristic, OwnerFilesHeuristic


def _print_results(result):
    print "MAINTAINERS"
    for i in result.maintainers.receivers:
        print i

    print "CC"
    for i in result.cc.receivers:
        print i


def main(args):
    #update_settings(args.config)
    #reviewers = set([])
    #BlameHeuristic(args.repo_path, args.youngest_commit, args.oldest_commit).get_reviewers()
    #print "\n\n"
    result = OwnerFilesHeuristic(args.repo_path, args.youngest_commit, args.oldest_commit).get_reviewers()

    _print_results(result)

    #print "Send an email"
    #print "Update reviewers"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--youngest_commit", "-y", help="The youngest commit from patch", required=True)
    parser.add_argument("--oldest_commit", "-o", help="The oldest commit from patch", required=True)
    parser.add_argument("--repo_path", "-rp", help="Ini configuration files path", default=os.getcwd())
    parser.add_argument("--config", "-c", help="Ini configuration files path", default=None)
    args = parser.parse_args()
    main(args)
