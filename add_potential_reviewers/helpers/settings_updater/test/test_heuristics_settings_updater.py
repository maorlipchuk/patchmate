#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from mock import MagicMock, patch
from add_potential_reviewers.helpers.settings_updater.heuristics_settings_updater import HeuristicsSettingsUpdater


class TestHeuristicSettingsUpdater(unittest.TestCase):
    def setUp(self):
        self.fake_dir = "fake_directory"
        self.parser = MagicMock()
        self.settings_updater = HeuristicsSettingsUpdater(self.parser, self.fake_dir)
        self.settings_updater.update_single_module_settings = MagicMock()

    def test_if_attributes_were_passed_correctly(self):
        self.assertEquals(self.settings_updater.parser, self.parser)
        self.assertIsInstance(self.settings_updater, HeuristicsSettingsUpdater)

    @patch("add_potential_reviewers.helpers.settings_updater.heuristics_settings_updater.os")
    def test_update_settings_will_execute_method_with_correct_arguments(self, os_mock):
        heuristic_names = ['heuristic1', 'heuristic2']
        file_names = ["__init__.py"]
        os_mock.listdir.return_value = file_names + heuristic_names
        os_mock.isdir.side_effect = tuple([False] * len(file_names) + [True] * len(heuristic_names))
        self.settings_updater.update_settings()
        for heuristic_name in heuristic_names:
            self.settings_updater.update_single_module_settings.assert_any_call_with(heuristic_name)


if __name__ == "__main__":
    unittest.main()
