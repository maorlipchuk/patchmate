#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pkg_resources
from common import SettingsUpdater


class HeuristicsSettingsUpdater(SettingsUpdater):
    @staticmethod
    def _get_heuristics_list():
        heuristics_path = pkg_resources.resource_filename("add_potential_reviewers", "heuristics")
        return [directory for directory in os.listdir(heuristics_path) if os.path.isdir(os.path.join(heuristics_path, directory))]

    def update_settings(self):
        heuristic_list = self._get_heuristics_list()
        for heuristic_name in heuristic_list:
            self.update_single_module_settings(heuristic_name)
