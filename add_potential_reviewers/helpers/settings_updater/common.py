#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
from add_potential_reviewers.helpers.logger import logger
from .converters import StrToFloatConverter, StrToBoolConverter, StrToListConverter, StrToIntConverter, StrToStrConverter


SUPPORT_FORMATS_DICT = {str: StrToStrConverter,
                        int: StrToIntConverter,
                        list: StrToListConverter,
                        bool: StrToBoolConverter,
                        float: StrToFloatConverter}


class SettingsUpdaterException(Exception):
    pass


class SettingsUpdater(object):
    def __init__(self, parser, settings_path):
        self.parser = parser
        self.settings_path = settings_path

    def update_single_module_settings(self, section_name):
        module = importlib.import_module("{settings}.{name}_settings".format(name=section_name, settings=self.settings_path))
        for argument, value in self.parser.items(section_name):
            param_type = type(getattr(module, argument, ""))
            if not param_type in SUPPORT_FORMATS_DICT:
                exception_message = "Type {type} is not supported".format(type=param_type)
                logger.error(exception_message)
                raise SettingsUpdaterException(exception_message)
            setattr(module, argument, SUPPORT_FORMATS_DICT[param_type]().convert(value))

    def update_settings(self):
        raise NotImplementedError()