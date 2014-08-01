#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
from patchmate.common.logger import logger
from .converters import StrToFloatConverter, StrToBoolConverter, StrToListConverter, StrToIntConverter, StrToStrConverter


SUPPORT_FORMATS_DICT = {str: StrToStrConverter,
                        int: StrToIntConverter,
                        list: StrToListConverter,
                        bool: StrToBoolConverter,
                        float: StrToFloatConverter}


class SettingsUpdaterException(Exception):
    pass


class SettingsUpdater(object):
    def __init__(self, parser, directory_path):
        self.parser = parser
        self.directory_path = directory_path

    def update_single_module_settings(self, section_name):
        module = importlib.import_module("{directory}.{name}.{name}_settings".format(name=section_name,
                                                                                     directory=self.directory_path))
        for argument, value in self.parser.items(section_name):
            param_type = type(getattr(module, argument, ""))
            if not param_type in SUPPORT_FORMATS_DICT:
                exception_message = "Type {type} is not supported".format(type=param_type)
                logger.error(exception_message)
                raise SettingsUpdaterException(exception_message)
            setattr(module, argument, SUPPORT_FORMATS_DICT[param_type]().convert(value))

    def update_settings(self):
        raise NotImplementedError()
