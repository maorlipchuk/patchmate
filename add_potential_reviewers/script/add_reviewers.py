#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main part of script
"""
from add_potential_reviewers.helpers.settings_updater import update_settings
import argparse


def main(config):
    update_settings(config)
    print "Get reviewers from heuristics"
    print "Send an email"
    print "Update reviewers"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help="Ini configuration files path", default=None)
    args = parser.parse_args()
    main(args.config)
