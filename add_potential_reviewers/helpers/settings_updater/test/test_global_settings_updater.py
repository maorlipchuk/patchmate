#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from mock import MagicMock
from add_potential_reviewers.helpers.settings_updater.global_settings_updater import GlobalsSettingsUpdater


class TestHeuristicSettingsUpdater(unittest.TestCase):
    def setUp(self):
        self.parser = MagicMock()
        self.settings_updater = GlobalsSettingsUpdater(self.parser)

    def test_if_attributes_were_passed_correctly(self):
        self.assertEquals(self.settings_updater.parser, self.parser)
        self.assertIsInstance(self.settings_updater, GlobalsSettingsUpdater)

    def test_if_settings_updater_raise_error_when_param_in_settings_is_not_supported_type(self):
        self.settings_updater.update_single_module_settings = MagicMock()
        self.settings_updater.update_settings()
        self.settings_updater.update_single_module_settings.assert_called_once_with("global")


if __name__ == "__main__":
    unittest.main()
