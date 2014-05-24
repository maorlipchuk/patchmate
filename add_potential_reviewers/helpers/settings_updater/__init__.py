#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
from .heuristics_settings_updater import HeuristicsSettingsUpdater


def update_settings(config_file_path=None, heuristics_path="add_potential_reviewers.heuristics"):
    if not config_file_path:
        return

    parser = ConfigParser()
    parser.read(config_file_path)
    HeuristicsSettingsUpdater(parser, heuristics_path).update_settings()
