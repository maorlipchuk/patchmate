#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import importlib
from mock import MagicMock, patch
from add_potential_reviewers.helpers.settings_updater.common import SettingsUpdaterException
from add_potential_reviewers.helpers.settings_updater.common import SettingsUpdater


class TestGlobalsSettingsUpdater(unittest.TestCase):
    def setUp(self):
        self.parser = MagicMock()
        self.settings_updater = SettingsUpdater(self.parser)
        self.test_settings_module_path = "add_potential_reviewers.helpers.settings_updater.test.common_settings_updater_test_data.settings"
        self.section_name = "global"

    def test_if_attributes_were_passed_correctly(self):
        self.assertEquals(self.settings_updater.parser, self.parser)
        self.assertIsInstance(self.settings_updater, SettingsUpdater)

    @patch("add_potential_reviewers.helpers.settings_updater.common.importlib")
    def test_update_settings_in_test_settings_module(self, importlib_mock):
        settings_module = importlib.import_module(self.test_settings_module_path)
        importlib_mock.import_module.return_value = settings_module
        string_setting = "Changed"
        number_setting = "10"
        float_setting = "1.0"
        bool_setting = "False"
        list_setting = "[changed1, changed2]"
        setting_without_update = "Test"
        items_list = [("string_setting", string_setting),
                      ("number_setting", number_setting),
                      ("float_setting", float_setting)]

        expected_type_dict = {"string_setting": str,
                              "number_setting": int,
                              "float_setting": float}

        self.parser.items.return_value = items_list + [("bool_setting", bool_setting), ("list_setting", list_setting)]
        self.settings_updater.update_single_module_settings(self.section_name)

        importlib_mock.import_module.assert_called_once_with("add_potential_reviewers.settings.global_settings")
        self.parser.items.assert_called_once_with(self.section_name)
        for argument, value in items_list:
            value = expected_type_dict[argument](value)
            module_value = getattr(settings_module, argument)
            self.assertEquals(module_value, value)
            self.assertIsInstance(value, expected_type_dict[argument])

        module_value_setting_without_update = getattr(settings_module, "setting_without_update")
        module_value_bool_setting = getattr(settings_module, "bool_setting")
        module_value_list_setting = getattr(settings_module, "list_setting")

        self.assertEquals(module_value_setting_without_update, setting_without_update)
        self.assertIsInstance(module_value_setting_without_update, str)
        self.assertEquals(module_value_bool_setting, False)
        self.assertIsInstance(module_value_bool_setting, bool)
        self.assertEquals(module_value_list_setting, ["changed1", "changed2"])
        self.assertIsInstance(module_value_list_setting, list)

    @patch("add_potential_reviewers.helpers.settings_updater.common.importlib")
    def test_if_settings_updater_raise_error_when_param_in_settings_is_not_supported_type(self, importlib_mock):
        settings_module = importlib.import_module(self.test_settings_module_path)
        importlib_mock.import_module.return_value = settings_module
        not_supported_type = "(test, test2)"
        self.parser.items.return_value = [("not_supported_type", not_supported_type)]
        with self.assertRaises(SettingsUpdaterException):
            self.settings_updater.update_single_module_settings(self.section_name)


if __name__ == "__main__":
    unittest.main()
