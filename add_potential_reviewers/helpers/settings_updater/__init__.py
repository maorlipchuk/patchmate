#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
from .global_settings_updater import GlobalsSettingsUpdater
from .heuristics_settings_updater import HeuristicsSettingsUpdater


def update_settings(config_file_path=None, settings_path="add_potential_reviewers.settings"):
    if not config_file_path:
        return

    parser = ConfigParser()
    parser.read(config_file_path)
    GlobalsSettingsUpdater(parser, settings_path).update_settings()
    HeuristicsSettingsUpdater(parser, settings_path).update_settings()